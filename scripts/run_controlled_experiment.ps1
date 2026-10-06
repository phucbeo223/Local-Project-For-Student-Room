param(
    [switch]$Pilot,
    [switch]$SkipV15,
    [string]$RunName = 'legal_selector_ab_36_v1_20261006'
)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    $taskCompose = @('-p','nckh','-f','docker-compose.yml','-f','docker-compose.override.yml',
        '-f','docker-compose.ragas.yml','-f','docker-compose.legal-refresh.yml',
        '-f','docker-compose.legal-review.yml')
    $gitCommit = (git rev-parse HEAD 2>$null)
    $taskArguments = @('run','--rm','--no-deps','--name',"nckh-$RunName",
        '-e',"GIT_COMMIT=$gitCommit",
        '--entrypoint','python',
        'ragas-eval','/workspace/eval/controlled_selector_experiment.py','--run-name',$RunName)
    if ($Pilot) { $taskArguments += '--pilot' }
    if ($SkipV15) { $taskArguments += '--skip-v15' }
    & docker compose @taskCompose @taskArguments
    if ($LASTEXITCODE -ne 0) { throw "Evaluation exited with code $LASTEXITCODE." }
} finally {
    Pop-Location
}
