import sys
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'eval'))
from report_priority7_36 import label


def result(raw, statuses, audited=True):
    return dict(quote_audit_passed=audited,
                comparison=dict(agreement=raw,points=[dict(status=s) for s in statuses]))


def test_high_model_label_cannot_hide_all_six_different_main_points():
    assert label(result('high',['different']*6)) == 'low'


def test_full_paraphrase_matches_use_a_consistent_high_label():
    assert label(result('partial',['matched']*3)) == 'high'


def test_mixed_missing_and_matched_main_points_need_review():
    assert label(result('high',['matched','missing','different'])) == 'partial'


def test_failed_quote_audit_does_not_produce_a_grade():
    assert label(result('high',['matched']*3,audited=False)) == 'unscored'
