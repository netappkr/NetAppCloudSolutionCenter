Write-Host ""
Write-Host "Simulating ransomware..."
Write-Host ""
$files="I:/"
$i = 1
while ($i -le 2000) {
Invoke-Item -path $files$i.txt
Stop-Process -Force -Name "notepad"
add-content -path $files$i.txt -value "ransome"
Rename-Item -Path $files$i.txt -NewName "$i.txt.lol"
$i++
}
Write-Host ""
Write-Host "--- Process complete ---"
Write-Host ""
Write-Host ""
$dummy = Read-Host "Press any key to close window..."
