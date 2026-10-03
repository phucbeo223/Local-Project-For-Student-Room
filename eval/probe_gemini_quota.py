"""Read model inventory and one quota error without logging credentials or project IDs."""
import json
import httpx
from app.config import settings

headers = {"x-goog-api-key": settings.configured_gemini_keys[0]}
base = settings.gemini_base_url
models = httpx.get(base + "/models", headers=headers, timeout=30)
if models.is_success:
    print("Available models:", [m["name"] for m in models.json().get("models", [])
                               if "generateContent" in m.get("supportedGenerationMethods", [])])
response = httpx.post(base + f"/models/{settings.gemini_model}:generateContent", headers=headers,
    json={"contents": [{"parts": [{"text": "Return OK"}]}],
          "generationConfig": {"maxOutputTokens": 64, "thinkingConfig": {"thinkingLevel": "low"}}}, timeout=60)
print("HTTP status:", response.status_code)
if response.is_error:
    for detail in response.json().get("error", {}).get("details", []):
        if "QuotaFailure" in detail.get("@type", ""):
            for v in detail.get("violations", []):
                print(json.dumps({k: v.get(k) for k in ("quotaMetric", "quotaId", "quotaValue")}, ensure_ascii=False))
        if "RetryInfo" in detail.get("@type", ""):
            print("Retry delay:", detail.get("retryDelay"))
