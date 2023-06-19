
Write-Host ""
Write-Host "Simulating ransomware..."
Write-Host ""
$strDir = "I:/"
GCI $strDir | Remove-Item -Confirm:$false -Force -Recurse
1..2000 | % { $strPath = $strDir + $_ + ".txt"; "something" | Out-File $strPath | Out-Null }

Write-Host ""
Write-Host "--- Process complete ---"
Write-Host ""
Write-Host ""
$dummy = Read-Host "Press any key to close window..."