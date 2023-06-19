
Write-Host ""
Write-Host "Simulating ransomware..."
Write-Host ""
$strDir = "I:/"
GCI $strDir | Remove-Item -Confirm:$false -Force -Recurse
1..6000 | % { $strPath = $strDir + $_ + ".txt"; "something" | Out-File $strPath | Out-Null }
1..6000 | % { $strPath = $strDir + $_ + ".txt"; $strNewPath = $strPath + ".chng"; "changed" | Out-File -Append $strPath; Rename-Item -Path $strPath -NewName $strNewPath }

Write-Host ""
Write-Host "--- Process complete ---"
Write-Host ""
Write-LogSuccess "Your files have been encrypted by my secret process with a key that only I have.  Unless you submit payment to me at the following digital currency wallet – 0x570234ab2398423 – within 14 days of this notification, I will delete the key and your data will forever be inaccessible.  Do not contact the authorities!  They cannot help you anyway."
Write-Host ""
$dummy = Read-Host "Press any key to close window..."