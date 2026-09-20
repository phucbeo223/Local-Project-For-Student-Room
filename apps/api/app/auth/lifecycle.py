"""Persistent, transactional account lifecycle. No OTP/token appears in logs."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import smtplib
from email.message import EmailMessage

from fastapi import HTTPException
from sqlalchemy import text

from ..config import settings
from .security import (
    hash_password,
    verify_password,
    make_access_token,
    make_refresh_token,
)


def digest(value: str) -> str:
    return hmac.new(
        settings.jwt_secret.encode(), value.encode(), hashlib.sha256
    ).hexdigest()


def send_email(email: str, subject: str, content: str) -> None:
    if not settings.smtp_host:
        raise HTTPException(503, "Chưa cấu hình SMTP để gửi email xác thực")
    message = EmailMessage()
    message["From"], message["To"], message["Subject"] = (
        settings.smtp_from,
        email,
        subject,
    )
    message.set_content(content)
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as smtp:
            if settings.smtp_starttls:
                smtp.starttls()
            if settings.smtp_user:
                smtp.login(settings.smtp_user, settings.smtp_password)
            smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as exc:
        raise HTTPException(503, "Không gửi được email, vui lòng thử lại") from exc


def rate_limit(engine, key: str, limit: int, seconds: int = 60) -> None:
    with engine.begin() as conn:
        count = conn.execute(
            text("""
            INSERT INTO request_buckets(key, count, expires_at)
            VALUES (:key, 1, now() + make_interval(secs => :seconds))
            ON CONFLICT (key) DO UPDATE SET
              count = CASE WHEN request_buckets.expires_at <= now() THEN 1 ELSE request_buckets.count + 1 END,
              expires_at = CASE WHEN request_buckets.expires_at <= now()
                THEN now() + make_interval(secs => :seconds) ELSE request_buckets.expires_at END
            RETURNING count
        """),
            {"key": digest(key), "seconds": seconds},
        ).scalar_one()
    if count > limit:
        raise HTTPException(
            429,
            "Quá nhiều yêu cầu, vui lòng thử lại sau",
            headers={"Retry-After": str(seconds)},
        )


class AccountLifecycle:
    def __init__(self, engine):
        self.engine = engine

    def challenge(self, email: str, purpose: str, payload: dict | None = None):
        rate_limit(self.engine, f"mail:{purpose}:{email}", 1)
        code = (
            f"{secrets.randbelow(1000000):06d}"
            if purpose == "register"
            else secrets.token_urlsafe(32)
        )
        with self.engine.begin() as conn:
            if (
                purpose == "reset"
                and not conn.execute(
                    text(
                        "SELECT 1 FROM user_identities WHERE provider = 'local' AND lower(provider_user_id) = :email"
                    ),
                    {"email": email},
                ).first()
            ):
                return
            if payload is None:
                payload = conn.execute(
                    text(
                        "SELECT payload FROM auth_challenges WHERE email=:email AND purpose=:purpose"
                    ),
                    {"email": email, "purpose": purpose},
                ).scalar()
                if payload is None:
                    return
            conn.execute(
                text("""
                INSERT INTO auth_challenges(email,purpose,digest,payload,expires_at)
                VALUES (:email,:purpose,:digest,CAST(:payload AS jsonb),now()+make_interval(mins => :minutes))
                ON CONFLICT(email,purpose) DO UPDATE SET digest=excluded.digest,payload=excluded.payload,
                  attempts=0,expires_at=excluded.expires_at,sent_at=now()
            """),
                {
                    "email": email,
                    "purpose": purpose,
                    "digest": digest(code),
                    "payload": json.dumps(payload),
                    "minutes": 5 if purpose == "register" else 30,
                },
            )
            content = f"Mã xác thực: {code}. Hết hạn sau 5 phút. Không chia sẻ mã này."
            if purpose == "reset":
                from urllib.parse import urlencode

                content = (
                    settings.web_public_url.rstrip("/")
                    + "/reset-password?"
                    + urlencode({"email": email, "token": code})
                )
            send_email(email, "TimTroSV - Xác thực tài khoản", content)

    def consume(self, email: str, purpose: str, code: str, password: str | None = None):
        result = None
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        "SELECT *, expires_at > now() AS valid FROM auth_challenges WHERE email=:email AND purpose=:purpose FOR UPDATE"
                    ),
                    {"email": email, "purpose": purpose},
                )
                .mappings()
                .first()
            )
            if row and row["valid"] and row["attempts"] < 3:
                if not hmac.compare_digest(row["digest"], digest(code)):
                    conn.execute(
                        text(
                            "UPDATE auth_challenges SET attempts=attempts+1 WHERE email=:email AND purpose=:purpose"
                        ),
                        {"email": email, "purpose": purpose},
                    )
                else:
                    if purpose == "register":
                        data = row["payload"]
                        user = (
                            conn.execute(
                                text(
                                    "INSERT INTO users(email,name,email_verified) VALUES (:email,:name,true) RETURNING id,role,auth_version"
                                ),
                                {"email": email, "name": data.get("name")},
                            )
                            .mappings()
                            .one()
                        )
                        conn.execute(
                            text(
                                "INSERT INTO user_identities(user_id,provider,provider_user_id,secret_hash) VALUES (:id,'local',:email,:hash)"
                            ),
                            {
                                "id": user["id"],
                                "email": email,
                                "hash": data["password_hash"],
                            },
                        )
                        result = dict(user)
                    else:
                        uid = conn.execute(
                            text(
                                "UPDATE user_identities SET secret_hash=:hash,failed_attempts=0,locked_until=NULL WHERE provider='local' AND lower(provider_user_id)=:email RETURNING user_id"
                            ),
                            {"hash": hash_password(password), "email": email},
                        ).scalar_one()
                        conn.execute(
                            text(
                                "UPDATE users SET auth_version=auth_version+1 WHERE id=:id"
                            ),
                            {"id": uid},
                        )
                        conn.execute(
                            text(
                                "UPDATE auth_sessions SET revoked=true WHERE user_id=:id"
                            ),
                            {"id": uid},
                        )
                        result = {"ok": True}
                    conn.execute(
                        text(
                            "DELETE FROM auth_challenges WHERE email=:email AND purpose=:purpose"
                        ),
                        {"email": email, "purpose": purpose},
                    )
        if result is None:
            raise HTTPException(
                400, "Mã sai, hết hạn hoặc đã sử dụng (tối đa 3 lần thử)"
            )
        return result

    def login(self, email: str, password: str):
        user, locked = None, False
        with self.engine.begin() as conn:
            row = (
                conn.execute(
                    text(
                        "SELECT i.*,u.role,u.auth_version, (i.locked_until > now()) AS locked FROM user_identities i JOIN users u ON u.id=i.user_id WHERE provider='local' AND lower(provider_user_id)=:email FOR UPDATE OF i"
                    ),
                    {"email": email},
                )
                .mappings()
                .first()
            )
            if row:
                locked = bool(row["locked"])
                if not locked and verify_password(password, row["secret_hash"]):
                    conn.execute(
                        text(
                            "UPDATE user_identities SET failed_attempts=0,locked_until=NULL WHERE id=:id"
                        ),
                        {"id": row["id"]},
                    )
                    user = {
                        "id": row["user_id"],
                        "role": row["role"],
                        "auth_version": row["auth_version"],
                    }
                elif not locked:
                    conn.execute(
                        text("""UPDATE user_identities SET
                        failed_attempts=CASE WHEN locked_until IS NOT NULL THEN 1 ELSE failed_attempts+1 END,
                        locked_until=CASE WHEN locked_until IS NULL AND failed_attempts>=4 THEN now()+interval '15 minutes' ELSE NULL END
                        WHERE id=:id"""),
                        {"id": row["id"]},
                    )
        if locked:
            raise HTTPException(
                429, "Tài khoản tạm khóa 15 phút do đăng nhập sai nhiều lần"
            )
        if user is None:
            raise HTTPException(401, "Email hoặc mật khẩu sai")
        return user

    def tokens(self, user: dict, previous: str | None = None):
        refresh = make_refresh_token(user["id"])
        with self.engine.begin() as conn:
            version = conn.execute(
                text("SELECT auth_version FROM users WHERE id=:id FOR UPDATE"),
                {"id": user["id"]},
            ).scalar_one()
            if version != user.get("auth_version", 0):
                raise HTTPException(
                    401, "Tài khoản vừa đổi thông tin xác thực, vui lòng đăng nhập lại"
                )
            if previous:
                used = conn.execute(
                    text(
                        "UPDATE auth_sessions SET revoked=true WHERE digest=:digest AND user_id=:id AND NOT revoked AND expires_at>now() RETURNING digest"
                    ),
                    {"digest": digest(previous), "id": user["id"]},
                ).first()
                if not used:
                    raise HTTPException(401, "Refresh token đã sử dụng hoặc bị thu hồi")
            conn.execute(
                text(
                    "INSERT INTO auth_sessions(digest,user_id,expires_at) VALUES (:digest,:id,now()+make_interval(days => :days))"
                ),
                {
                    "digest": digest(refresh),
                    "id": user["id"],
                    "days": settings.refresh_token_ttl_days,
                },
            )
        return {
            "access_token": make_access_token(
                user["id"], user["role"], user.get("auth_version", 0)
            ),
            "refresh_token": refresh,
            "token_type": "bearer",
        }

    def logout(self, refresh: str):
        with self.engine.begin() as conn:
            conn.execute(
                text("UPDATE auth_sessions SET revoked=true WHERE digest=:digest"),
                {"digest": digest(refresh)},
            )
