from resume_legal_evaluation import completion_phase

METRICS=('faithfulness','answer_relevancy','context_utilization')

def case():return {'answer':'Observed response','contexts':['evidence'],'ragas':dict.fromkeys(METRICS,.8)}

def test_nan_and_partial_metrics_cannot_mark_job_complete():
    c=case();c['ragas']['faithfulness']=float('nan')
    assert completion_phase({'cases':[c]},1)=='complete_with_errors'
    c['ragas'].pop('faithfulness')
    assert completion_phase({'cases':[c]},1)=='complete_with_errors'

def test_missing_context_is_explicitly_unscorable_without_fake_zero():
    c={'answer':'No match','contexts':[],'unscorable_reason':'No retrieved evidence'}
    assert completion_phase({'cases':[case(),c]},2)=='complete_with_unscorable_cases'
    assert 'ragas' not in c
    c['contexts']=['now there is evidence']
    assert completion_phase({'cases':[case(),c]},2)=='complete_with_errors'

def test_expected_subset_and_execution_errors_are_checked():
    assert completion_phase({'cases':[case()]},12)=='complete_with_errors'
    assert completion_phase({'cases':[case()]},1)=='complete'
    c=case();c['error']='Runtime failure'
    assert completion_phase({'cases':[c]},1)=='complete_with_errors'
