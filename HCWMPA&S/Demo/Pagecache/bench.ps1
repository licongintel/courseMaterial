param(
    [string]$Path = "./com.microsoft.office.officehub.apk",
    [ValidateRange(1, 100)]
    [int]$Passes = 5
)

$BufSizeMB = 4

if (-not $Path) {
    Write-Error "Usage: .\bench.ps1 -Path <file> [-Passes N]"
    exit 1
}
if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
    Write-Error "File not found: '$Path'"
    exit 1
}

$item = Get-Item -LiteralPath $Path
$totalBytes = $item.Length
$buf = New-Object byte[] ($BufSizeMB * 1MB)

""
"File : $($item.FullName) ($('{0:N1}' -f ($totalBytes / 1MB)) MB)"
"Mode : normal (page cache), $Passes pass(es), $BufSizeMB MB buffer"
""

$sw = [System.Diagnostics.Stopwatch]::new()
$firstRate = 0.0

for ($pass = 1; $pass -le $Passes; $pass++) {
    $fs = [IO.File]::OpenRead($item.FullName)
    try {
        [void]$fs.Seek(0, [IO.SeekOrigin]::Begin)
        $done = [long]0
        $sw.Restart()
        while (($n = $fs.Read($buf, 0, $buf.Length)) -gt 0) { $done += $n }
        $sw.Stop()
    }
    finally { $fs.Close() }

    if ($done -ne $totalBytes) {
        Write-Warning "Short read: $done of $totalBytes bytes"
    }

    $secs = $sw.Elapsed.TotalSeconds
    $rate = if ($secs -gt 0) { $done / 1MB / $secs } else { 0.0 }
    if ($pass -eq 1) {
        $firstRate = $rate
        "Pass 1 : {0,8:N0} MB/s  ({1:N2} s)" -f $rate, $secs
    }
    else {
        $x = if ($firstRate -gt 0) { $rate / $firstRate } else { 0.0 }
        "Pass $pass : {0,8:N0} MB/s  ({1:N2} s)  ({2:N1}x vs pass 1)" -f $rate, $secs, $x
    }
}

""
"Warm passes are served from RAM by the page cache."
"Run .\reset.ps1 first to make pass 1 a genuine cold read."
