"use client";
import Script from "next/script";
import { useRef, useState } from "react";
type GIS = {
  accounts: {
    id: {
      initialize: (options: {
        client_id: string;
        callback: (r: { credential: string }) => void;
      }) => void;
      renderButton: (el: HTMLElement, options: object) => void;
    };
  };
};
export default function GoogleLogin() {
  const el = useRef<HTMLDivElement>(null);
  const [error, setError] = useState("");
  const id = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;
  if (!id) return null;
  return (
    <div>
      <Script
        src="https://accounts.google.com/gsi/client"
        onReady={() => {
          const google = (window as unknown as { google: GIS }).google;
          google.accounts.id.initialize({
            client_id: id,
            callback: async ({ credential }) => {
              try {
                const r = await fetch("/api/auth/google", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ id_token: credential }),
                });
                const b = await r.json();
                if (r.ok) window.location.assign("/onboarding");
                else setError(b.detail);
              } catch {
                setError("Không kết nối được máy chủ");
              }
            },
          });
          if (el.current)
            google.accounts.id.renderButton(el.current, {
              theme: "outline",
              size: "large",
            });
        }}
      />
      <div ref={el} />
      <p role="alert">{error}</p>
    </div>
  );
}
