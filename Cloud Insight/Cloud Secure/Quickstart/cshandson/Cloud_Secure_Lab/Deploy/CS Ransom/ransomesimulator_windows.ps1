#STOP DSC
#下記 create files コマンドを実施する前に、必ずデータコレクタを止めてください

#create files
#ダミーファイルを作成します
$files="\\10.146.15.205\lewisV_share\xxx\"
1..500 | foreach { new-item -path $files$_.txt }
# write something to files or it wont "read"
$i = 1
while ($i -le 500) {
add-content -path $files$i.txt -value "ransom test"
$i++
}

#START DSC
#データコレクタを開始してください

#run Ransomware simulator
#ランサム攻撃のシミューレーションテストを実施します
 
Write-Host ""
Write-Host "Simulating Ransom attack..."
Write-Host ""
$i = 1
while ($i -le 500) {
Invoke-Item -path $files$i.txt
Stop-Process -Force -Name "notepad"
add-content -path $files$i.txt -value "ransome"
Rename-Item -Path $files$i.txt -NewName "$i.txt.lol"
$i++
}