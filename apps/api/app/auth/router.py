"""Auth endpoints: register, login (local), login/google, refresh, me."""

from __future__ import annotations

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError

from .deps import get_current_user
from .providers import AuthError, verify_google, verify_local
from .repo import AuthRepo
from .schemas import (
    GoogleLoginIn,
    LoginIn,
    RefreshIn,
    RegisterIn,
    TokenPair,
    UserOut,
)
from .security import decode_token, hash_password, make_access_token, make_refresh_token
from .lifecycle import AccountLifecycle, rate_limit
from .schemas import EmailIn, VerifyIn, ResetIn, ProfileIn

router = APIRouter(prefix="/auth", tags=["auth"])

_engine: Engine | None = None


def init_auth(engine: Engine) -> None:
    global _engine
    _engine = engine


def get_repo() -> AuthRepo:
    if _engine is None:
        raise HTTPException(503, "Auth repo chưa khởi tạo")
    return AuthRepo(_engine)


def _tokens(user_id: int, role: str) -> TokenPair:
    user = get_repo().get_user(user_id)
    return TokenPair(**AccountLifecycle(_engine).tokens(user))


@router.post("/register", status_code=202)
def register(body: RegisterIn, repo: AuthRepo = Depends(get_repo)):
    email = str(body.email).lower()
    if repo.email_exists(email):
        raise HTTPException(409, "Email đã đăng ký")
    AccountLifecycle(repo.engine).challenge(
        email,
        "register",
        {"name": body.name, "password_hash": hash_password(body.password)},
    )
    return {"verification_required": True, "email": email}


@router.post("/login", response_model=TokenPair)
def login(body: LoginIn, request: Request, repo: AuthRepo = Depends(get_repo)):
    rate_limit(
        repo.engine, f"login:{request.client.host if request.client else 'unknown'}", 60
    )
    lifecycle = AccountLifecycle(repo.engine)
    return lifecycle.tokens(lifecycle.login(str(body.email).lower(), body.password))


@router.post("/login/google", response_model=TokenPair)
async def login_google(body: GoogleLoginIn, repo: AuthRepo = Depends(get_repo)):
    try:
        vi = await verify_google(body.id_token)
    except AuthError as e:
        raise HTTPException(401, str(e))

    identity = repo.find_identity("google", vi.provider_user_id)
    if identity is not None:
        return _tokens(identity["user_id"], identity["role"])

    # lần đầu: tạo user + google identity (secret_hash NULL)
    if repo.email_exists(vi.email):
        raise HTTPException(409, "Email đã dùng cho phương thức đăng nhập khác")
    try:
        created = repo.create_user_with_identity(
            email=vi.email,
            name=vi.name,
            provider="google",
            provider_user_id=vi.provider_user_id,
            secret_hash=None,
            avatar_url=vi.avatar_url,
            email_verified=vi.email_verified,
        )
    except IntegrityError:
        # email đã tồn tại (đăng ký local trước) — chặn để tránh chiếm tài khoản
        raise HTTPException(409, "Email đã dùng cho phương thức đăng nhập khác")
    return _tokens(created["user_id"], created["role"])


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshIn, repo: AuthRepo = Depends(get_repo)):
    try:
        payload = decode_token(body.refresh_token, "refresh")
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Refresh token hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Refresh token không hợp lệ")

    user = repo.get_user(int(payload["sub"]))
    if user is None:
        raise HTTPException(401, "User không tồn tại")
    return AccountLifecycle(repo.engine).tokens(user, previous=body.refresh_token)


@router.get("/me", response_model=UserOut)
def me(user: UserOut = Depends(get_current_user)):
    return user


@router.post("/verify-email", response_model=TokenPair)
def verify_email(body: VerifyIn, repo: AuthRepo = Depends(get_repo)):
    lifecycle = AccountLifecycle(repo.engine)
    try:
        user = lifecycle.consume(str(body.email).lower(), "register", body.code)
    except IntegrityError:
        raise HTTPException(409, "Email đã đăng ký")
    return lifecycle.tokens(user)


@router.post("/resend-otp")
def resend(body: EmailIn, repo: AuthRepo = Depends(get_repo)):
    AccountLifecycle(repo.engine).challenge(str(body.email).lower(), "register")
    return {"ok": True}


@router.post("/forgot-password")
def forgot(body: EmailIn, repo: AuthRepo = Depends(get_repo)):
    AccountLifecycle(repo.engine).challenge(str(body.email).lower(), "reset", {})
    return {"detail": "Nếu email đã đăng ký, hướng dẫn đặt lại mật khẩu sẽ được gửi."}


@router.post("/reset-password")
def reset(body: ResetIn, repo: AuthRepo = Depends(get_repo)):
    return AccountLifecycle(repo.engine).consume(
        str(body.email).lower(), "reset", body.token, body.password
    )


@router.post("/logout")
def logout(body: RefreshIn, repo: AuthRepo = Depends(get_repo)):
    AccountLifecycle(repo.engine).logout(body.refresh_token)
    return {"ok": True}


@router.patch("/me", response_model=UserOut)
def profile(
    body: ProfileIn,
    user: UserOut = Depends(get_current_user),
    repo: AuthRepo = Depends(get_repo),
):
    with repo.engine.begin() as conn:
        conn.execute(
            text("UPDATE users SET name=:name WHERE id=:id"),
            {"name": body.name.strip(), "id": user.id},
        )
    return repo.get_user(user.id)
