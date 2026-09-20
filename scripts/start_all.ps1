[CmdletBinding()]
param(
    [switch]$SkipBuild,
    [switch]$SkipSeed,
    [switch]$IndexLegal
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$previousCrawlerEnabled = $env:CRAWLER_ENABLED

function Invoke-Compose {
    param([Parameter(Mandatory = $true)][string[]]$ComposeArgs)

    & docker compose @ComposeArgs
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose $($ComposeArgs -join ' ') failed with exit code $LASTEXITCODE"
    }
}

Push-Location $projectRoot
try {
    # The research/demo stack uses controlled synthetic data. Crawling is owned by
    # another team and must only be enabled explicitly outside this launcher.
    $env:CRAWLER_ENABLED = "false"

    $infraArgs = @("up", "-d")
    if (-not $SkipBuild) {
        $infraArgs += "--build"
    }
    $infraArgs += @("db", "redis")
    Invoke-Compose -ComposeArgs $infraArgs

    $dbReady = $false
    foreach ($attempt in 1..30) {
        & docker compose exec -T db sh -ec 'pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"' *> $null
        if ($LASTEXITCODE -eq 0) {
            $dbReady = $true
            break
        }
        Start-Sleep -Seconds 1
    }
    if (-not $dbReady) {
        throw "PostgreSQL did not become ready within 30 seconds"
    }

    $migrations = @(
        "90-chatbot.sql",
        "91-room-service-risk.sql",
        "92-reports-moderation.sql",
        "93-ai-product-features.sql",
        "94-legal-knowledge.sql",
        "95-fr-delivery.sql",
        "96-reviews-sentiment.sql",
        "97-response-performance.sql",
        "98-legal-quality.sql"
    )
    foreach ($migration in $migrations) {
        $sql = 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "/docker-entrypoint-initdb.d/{0}"' -f $migration
        Invoke-Compose -ComposeArgs @("exec", "-T", "db", "sh", "-ec", $sql)
    }

    if (-not $SkipSeed) {
        $seedPath = Join-Path $projectRoot "infra\db\seeds\dev_chatbot.sql"
        if (-not (Test-Path -LiteralPath $seedPath)) {
            throw "Missing synthetic seed: $seedPath. Run scripts/generate_fake_listings.py first."
        }
        Invoke-Compose -ComposeArgs @("cp", $seedPath, "db:/tmp/dev_chatbot.sql")
        $seedSql = 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /tmp/dev_chatbot.sql'
        Invoke-Compose -ComposeArgs @("exec", "-T", "db", "sh", "-ec", $seedSql)
    }

    if ($IndexLegal) {
        Write-Host "Indexing OCR/legal corpus from Data/..."
        Invoke-Compose -ComposeArgs @("--profile", "tools", "run", "--rm", "legal-indexer")
    }

    $appArgs = @("up", "-d")
    if (-not $SkipBuild) {
        $appArgs += "--build"
    }
    $appArgs += @("api", "web")
    Invoke-Compose -ComposeArgs $appArgs

    $apiReady = $false
    foreach ($attempt in 1..45) {
        try {
            $health = Invoke-RestMethod -Uri "http://localhost:8000/health/deps" -TimeoutSec 3
            if ($health.postgres -eq "ok" -and $health.redis -eq "ok" -and $health.pgvector -eq "ok") {
                $apiReady = $true
                break
            }
        }
        catch {
            # The API container can still be starting; retry below.
        }
        Start-Sleep -Seconds 1
    }
    if (-not $apiReady) {
        Invoke-Compose -ComposeArgs @("logs", "--tail=80", "api", "web")
        throw "API dependency health check did not pass within 45 seconds"
    }

    $listingResult = Invoke-RestMethod -Uri "http://localhost:8000/listings?page=1&size=1" -TimeoutSec 10
    Invoke-Compose -ComposeArgs @("ps")
    Write-Host ""
    Write-Host "System is ready; crawler scheduler is disabled."
    Write-Host "Listings available: $($listingResult.total)"
    Write-Host "Web:      http://localhost:3000"
    Write-Host "Chatbot:  http://localhost:3000/chat"
    Write-Host "Risk/Admin: http://localhost:3000/admin/ai"
    Write-Host "API docs: http://localhost:8000/docs"
}
finally {
    if ($null -eq $previousCrawlerEnabled) {
        Remove-Item Env:\CRAWLER_ENABLED -ErrorAction SilentlyContinue
    }
    else {
        $env:CRAWLER_ENABLED = $previousCrawlerEnabled
    }
    Pop-Location
}
