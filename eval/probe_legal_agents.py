"""Check the configured question-analysis role without logging keys or answers."""
import json
from pathlib import Path
from datetime import datetime,timezone
from sqlalchemy import create_engine
from app.config import settings
from app.room_service.chatbot.router import init_chatbot,get_service,close_chatbot

engine=create_engine(settings.database_url)
init_chatbot(engine)
service=get_service()
assert service.question_analyzer is not None
assert all(p.provider_name=='qwen-local' for p in service.generator.providers)
result=service.question_analyzer.analyze('Nếu chuyển sang phòng trọ khác, tôi cần cập nhật thông tin cư trú thế nào?')
report={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'corpus':service.repo.legal_schema,
        'analysis':result.step,'plan':result.plan.model_dump(mode='json'),'degraded_reasons':result.degraded_reasons,
        'answer_providers':[{'provider':p.provider_name,'model':p.model} for p in service.generator.providers]}
Path('/eval/reports/legal_agent_probe_2026-10-03.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False),flush=True)
close_chatbot();engine.dispose()
