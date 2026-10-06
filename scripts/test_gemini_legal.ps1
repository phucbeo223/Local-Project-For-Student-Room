param(
    [ValidateSet('combined', 'separate', 'qwen')][string]$Mode = 'combined',
    [Parameter(Mandatory=$true)][ValidatePattern('^[a-zA-Z0-9_-]+$')][string]$RunName,
    [int[]]$Ids = (@(19..38) + @(43..58)),
    [switch]$Preflight
)
$ErrorActionPreference = 'Stop'
Push-Location (Split-Path $PSScriptRoot -Parent)
try {
    # No graph-rag/source-grounded overlays: these mount the housing catalog.
    $taskCompose = @('-p','nckh','-f','docker-compose.yml','-f','docker-compose.override.yml',
        '-f','docker-compose.ragas.yml','-f','docker-compose.legal-refresh.yml',
        '-f','docker-compose.legal-review.yml')
    $taskProvider = if ($Mode -eq 'qwen') { 'qwen' } else { 'gemini' }
    $taskGeneration = if ($Mode -eq 'qwen') { 'separate' } else { $Mode }
    $taskArguments = @('run','--rm','--no-deps','--name',"nckh-$RunName",'--entrypoint','python',
        '-e',"CHATBOT_LEGAL_SELECTION_PROVIDER=$taskProvider",'-e',"CHATBOT_LEGAL_GENERATION_MODE=$taskGeneration",
        'ragas-eval','/eval/graph_rag_question_bank.py','--legal-only','--output',"/eval/reports/$RunName.json",'--ids') + $Ids
    if ($Preflight) { $taskArguments += '--preflight-only' }
    & docker compose @taskCompose @taskArguments
    if ($LASTEXITCODE -ne 0) { throw "Evaluation exited with code $LASTEXITCODE. Keep the checkpoint; do not overwrite it." }
} finally {
    Pop-Location
}
