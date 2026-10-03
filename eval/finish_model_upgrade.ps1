param([switch]$WaitForCollection, [switch]$WaitForBaseline)
$ErrorActionPreference = 'Stop'
$taskComposeFiles = @('-f','docker-compose.yml','-f','docker-compose.override.yml','-f','docker-compose.ragas.yml')
if ($WaitForCollection) {
    $taskCollectionExit = docker wait nckh-upgrade-collect
    if ($LASTEXITCODE -ne 0 -or $taskCollectionExit -ne '0') { throw 'Collection did not finish successfully' }
}
if ($WaitForBaseline) {
    $taskBaselineExit = docker wait nckh-final-score-before
    if ($LASTEXITCODE -ne 0 -or $taskBaselineExit -ne '0') { throw 'Baseline scoring did not finish successfully' }
}
docker compose @taskComposeFiles run --rm --no-deps --name nckh-upgrade-score-after ragas-eval --phase score --output /eval/reports/legal_model_upgrade_after_2026-10-02.json --judge-provider gemini --judge-model gemini-3.1-flash-lite --judge-max-output-tokens 8192 --score-workers 4 --score-abstentions
if ($LASTEXITCODE -ne 0) { throw 'After scoring failed' }
docker compose @taskComposeFiles run --rm --no-deps --entrypoint python ragas-eval /eval/compare_model_upgrade.py --before /eval/reports/legal_upgrade_before_common_judge_2026-10-02.json --after /eval/reports/legal_model_upgrade_after_2026-10-02.json --audit /eval/reports/legal_corpus_upgrade_2026-10-02.json --output /eval/ragas_reports/legal_model_upgrade_comparison_2026-10-02.md
if ($LASTEXITCODE -ne 0) { throw 'Comparison rendering failed' }
docker compose @taskComposeFiles run --rm --no-deps --entrypoint python ragas-eval /eval/stamp_model_upgrade.py --before /eval/reports/legal_upgrade_before_common_judge_2026-10-02.json --after /eval/reports/legal_model_upgrade_after_2026-10-02.json --output /eval/reports/legal_model_upgrade_manifest_2026-10-02.json
if ($LASTEXITCODE -ne 0) { throw 'Manifest failed' }
