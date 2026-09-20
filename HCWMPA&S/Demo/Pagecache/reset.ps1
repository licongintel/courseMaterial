param(
    [double]$GB = 8,
    [string]$Source = 'C:\Windows\WinSxS',
    [int]$MinFileMB = 1
)

$target = [long]($GB * 1GB)
$sum = [long]0
$bufSize = 4MB
$buf = New-Object byte[] $bufSize

$files = Get-ChildItem $Source -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -gt ($MinFileMB * 1MB) } |
    Sort-Object Length -Descending

if (-not $files -or $files.Count -eq 0) {
    Write-Error "No files > ${MinFileMB} MB found under '$Source'."
    exit 1
}

$sw = [System.Diagnostics.Stopwatch]::StartNew()
foreach ($f in $files) {
    if ($sum -ge $target) { break }
    try {
        $fs = $f.OpenRead()
        while (($n = $fs.Read($buf, 0, $bufSize)) -gt 0) { }
        $fs.Close()
        $sum += $f.Length
        Write-Progress -Activity 'Flushing page cache (standby list)' `
            -Status ('{0:N2} / {1:N2} GB' -f ($sum / 1GB), ($target / 1GB)) `
            -PercentComplete ([math]::Min(100, $sum * 100 / $target))
    }
    catch { }
}
$sw.Stop()

Write-Progress -Activity 'Flushing page cache (standby list)' -Completed
'Cache flushed: streamed {0:N2} GB from ''{1}'' in {2:N0}s' -f ($sum / 1GB), $Source, $sw.Elapsed.TotalSeconds
