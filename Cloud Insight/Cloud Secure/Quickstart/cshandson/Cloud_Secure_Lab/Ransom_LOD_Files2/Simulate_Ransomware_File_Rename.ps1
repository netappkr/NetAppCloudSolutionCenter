
Write-Host ""
Write-Host "Simulating ransomware..."
Write-Host ""
$strDir = "I:/"
GCI $strDir | Remove-Item -Confirm:$false -Force -Recurse
1..5000 | % { $strPath = $strDir + $_ + ".txt"; $strNewPath = $strPath + ".chng"; "changed" | Out-File -Append $strPath; Rename-Item -Path $strPath -NewName $strNewPath }

Write-Host ""
Write-Host "--- Process complete ---"
Write-Host ""
$dummy = Read-Host "Press any key to close window..."