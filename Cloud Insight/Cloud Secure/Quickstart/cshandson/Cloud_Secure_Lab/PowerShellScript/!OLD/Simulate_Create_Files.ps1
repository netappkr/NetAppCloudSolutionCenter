Write-Host ""
Write-Host "Simulating ransomware..."
Write-Host ""
$files="I:/"
1..2000 | foreach { new-item -path $files\$_.txt }
# write something to files or it wont "read"

Write-Host ""
Write-Host "--- Process complete ---"
Write-Host ""
Write-Host ""
$dummy = Read-Host "Press any key to close window..."