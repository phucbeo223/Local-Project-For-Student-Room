# Fetch publisher-provided Word attachments only. Never convert or OCR a PDF.
$ErrorActionPreference='Stop'
$workspaceRoot=Split-Path -Parent $PSScriptRoot
$outputRoot=Join-Path $workspaceRoot 'Data/word_originals'
New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null
$sources=@(
  @{Id='civil91-word';Page='https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/';Direct='https://congan.daklak.gov.vn/laws/detail/Bo-luat-Dan-su-163/?download=1&id=0';Category='housing_contract'},
  @{Id='fire55-word';Page='https://congbao.chinhphu.vn/van-ban-dang-cong-bao/quoc-hoi-c31/trang-19.htm';Pattern='55-2024.*\.doc$';Category='fire_safety'},
  @{Id='residence68-word';Page='https://congbao.chinhphu.vn/van-ban/luat-so-68-2020-qh14-32684/33716.htm';Pattern='68-2020.*\.doc$';Category='residence'}
)
$metadata=@()
foreach($source in $sources){
  $url=$source.Direct
  if(!$url){
    $page=Invoke-WebRequest -Uri $source.Page -TimeoutSec 30
    $links=@($page.Links | Where-Object { $_.href -match $source.Pattern } | ForEach-Object { [System.Net.WebUtility]::HtmlDecode($_.href) } | Select-Object -Unique)
    if($links.Count -ne 1){throw "Expected one Word attachment: $($source.Id)"}
    $url=$links[0]
  }
  $uri=[Uri]$url
  if($uri.Scheme -ne 'https' -or $uri.Host -notin @('congan.daklak.gov.vn','g7.cdnchinhphu.vn')){throw 'Unexpected Word publisher host'}
  $path=Join-Path $outputRoot "$($source.Id).doc"
  Invoke-WebRequest -Uri $url -OutFile $path -TimeoutSec 60
  $payload=[System.IO.File]::ReadAllBytes($path)
  if([Convert]::ToHexString($payload[0..7]) -ne 'D0CF11E0A1B11AE1'){throw "Not a native Word binary: $($source.Id)"}
  $metadata+=@{id=$source.Id;source_url=$source.Page;download_url=$url;category=$source.Category;path="Data/word_originals/$($source.Id).doc";
    sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower();retrieved_at_utc=[DateTime]::UtcNow.ToString('o');tls_verified=$true}
  Write-Output "Fetched $($source.Id) as native Word"
}
ConvertTo-Json -InputObject $metadata -Depth 6 | Set-Content -LiteralPath (Join-Path $outputRoot 'sources.json') -Encoding utf8
