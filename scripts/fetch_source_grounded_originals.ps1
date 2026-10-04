# Native originals linked by the primary publisher; Windows validates its TLS chain.
$ErrorActionPreference='Stop'
$workspaceRoot=Split-Path -Parent $PSScriptRoot
$outputRoot=Join-Path $workspaceRoot 'docs/source_grounded_originals_20261004'
New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null
$sources=@(
  @{Key='procedure17';Url='https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-17-vbhn-vpqh-468961.htm';Suffix='docx';Expected=1},
  @{Key='criminal135';Url='https://congbao.chinhphu.vn/van-ban/van-ban-hop-nhat-so-135-vbhn-vpqh-46165/58894.htm';Suffix='doc';Expected=4}
)
foreach($source in $sources){
  $page=Invoke-WebRequest -Uri $source.Url
  $links=@($page.Links|Where-Object{$_.href -like "*file_name=*.$($source.Suffix)"})
  if($links.Count -ne $source.Expected){throw "Unexpected original attachment count: $($source.Key)"}
  $metadata=@();$part=0
  foreach($link in $links){
    $part++
    $url=[System.Net.WebUtility]::HtmlDecode($link.href)
    if(([Uri]$url).Scheme -ne 'https' -or ([Uri]$url).Host -ne 'g7.cdnchinhphu.vn'){throw 'Unexpected attachment host'}
    $key=if($source.Expected -eq 1){$source.Key}else{"$($source.Key)-$part"}
    $relative="docs/source_grounded_originals_20261004/$key.$($source.Suffix)"
    $path=Join-Path $workspaceRoot $relative
    Invoke-WebRequest -Uri $url -OutFile $path
    $metadata+=@{id=$key;source_url=$source.Url;download_url=$url;path=$relative;
      sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower();
      retrieved_at_utc=[DateTime]::UtcNow.ToString('o');tls_verified=$true}
  }
  ConvertTo-Json -InputObject $metadata -Depth 5 | Set-Content -LiteralPath (Join-Path $outputRoot "$($source.Key).download.json") -Encoding utf8
}
