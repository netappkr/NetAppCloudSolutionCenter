Write-Host ""
Write-Host "Simulating ransomware..."
Write-Host ""
$files="I:/"
$i=1
while ($i -le 2000) {
add-content -path $files$i.txt -value "somthing word"
$i++
}
Write-Host ""
Write-Host "--- Process complete ---"
Write-Host ""
Write-Host ""
$dummy = Read-Host "Press any key to close window..."