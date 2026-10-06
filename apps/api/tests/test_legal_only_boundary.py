import sys
from pathlib import Path
from types import SimpleNamespace
import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'eval'))
from legal_only_boundary import assert_legal_cases, install
from test_agent_workflow import QUESTION, rows
from app.room_service.chatbot.schemas import ChatAskRequest


class Connection:
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def execute(self,*args): return self
    def tuples(self): return [(1,11),(2,22)]


def boundary():
    calls=[]
    service=SimpleNamespace(repo=SimpleNamespace(retrieve_legal=lambda *a,**k:rows()),
        ask=lambda body:calls.append('ask'),
        generator=SimpleNamespace(writer=SimpleNamespace(synthesize=lambda *a,**k:calls.append('write')),
            verifier=SimpleNamespace(check_legal_evidence=lambda *a,**k:calls.append('verify'))))
    report=install(service,SimpleNamespace(connect=lambda:Connection()),
        [dict(category='housing_contract',question=QUESTION)],'legal_test')
    return service,calls,report


def test_non_legal_question_is_blocked_before_any_model_call():
    with pytest.raises(ValueError): assert_legal_cases([dict(category='find_listing',question='Tìm phòng dưới 2 triệu.')])
    service,calls,_=boundary()
    with pytest.raises(ValueError): service.ask(ChatAskRequest(message='Nhà trọ riêng ở địa chỉ của tôi có giá điện bao nhiêu?'))
    with pytest.raises(ValueError): service.repo.retrieve('housing query')
    assert calls==[]


def test_listing_fields_and_forged_legal_identity_are_blocked_at_cloud_boundary():
    service,calls,report=boundary()
    for bad in (dict(rows()[0],address='PRIVATE ADDRESS'),dict(rows()[0],document_id=999),dict(rows()[0],category='find_listing')):
        with pytest.raises(ValueError): service.generator.writer.synthesize(QUESTION,SimpleNamespace(selected_evidence=[bad]))
        with pytest.raises(ValueError): service.generator.verifier.check_legal_evidence(QUESTION,'answer',[bad])
    assert calls==[] and report['listing_retrieval_disabled']


def test_allowed_legal_sources_still_reach_public_legal_writer_and_verifier():
    service,calls,_=boundary()
    service.generator.writer.synthesize(QUESTION,SimpleNamespace(selected_evidence=rows()))
    service.generator.verifier.check_legal_evidence(QUESTION,'answer',rows())
    assert calls==['write','verify']
