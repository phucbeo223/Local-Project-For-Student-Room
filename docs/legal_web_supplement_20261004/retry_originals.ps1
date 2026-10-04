$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$workspaceRoot = Split-Path -Parent $taskRoot
$catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'sources.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($source in $catalog.sources) {
    if ($source.id -in @('housing79', 'broker06', 'electricity09', 'electricity25')) {
        $attachment = $source.discovered_attachments | Where-Object { $_.label -match '\.pdf$' }
        if ($source.id -eq 'electricity09') {
            $attachment = $attachment | Where-Object { $_.label -match '09-2023-TT-BCT' }
        }
        $attachment = $attachment | Select-Object -First 1
        if ($attachment) {
            try {
                $target = Join-Path $PSScriptRoot ('originals\' + $source.id + '.pdf')
                Invoke-WebRequest -Uri $attachment.url -OutFile $target -UseBasicParsing -TimeoutSec 45
                Write-Output ($source.id + ' downloaded using Windows TLS trust')
            } catch { Write-Output ($source.id + ' download failed: ' + $_.Exception.Message) }
        }
    }
}
try {
    $decisionUrl = 'https://moc.gov.vn/vn/Pages/ChiTietVanBan.aspx?TypeVB=1&vID=5019'
    $response = Invoke-WebRequest -Uri $decisionUrl -UseBasicParsing -TimeoutSec 45
    $decisionLinks = @($response.Links | Where-Object { $_.href -match '1074.*\.pdf' })
    foreach ($decisionLink in $decisionLinks) {
        $resolved = [uri]::new([uri]$decisionUrl, [string]$decisionLink.href).AbsoluteUri
        $fileName = if ($resolved -match '(?i)phuluc|phu_luc') { 'fire1074-annex.pdf' } else { 'fire1074.pdf' }
        Invoke-WebRequest -Uri $resolved -OutFile (Join-Path $PSScriptRoot ('originals\' + $fileName)) -UseBasicParsing -TimeoutSec 45
        Write-Output ($fileName + ' ' + $resolved)
    }
} catch { Write-Output ('fire1074 download failed: ' + $_.Exception.Message) }
