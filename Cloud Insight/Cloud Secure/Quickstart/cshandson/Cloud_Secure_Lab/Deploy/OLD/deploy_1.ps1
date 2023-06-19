Start-Transcript "c:\users\administrator\deploylogs.txt"
#生徒の番号を入力
$number = Read-Host "Input Student Number"
Write-Host "Your Student Number is" $number

#YN分岐
$input = Read-Host "Your Student Number is OK? and Start Deploy?(y/n)"
switch($input){
"y"{
    #番号をもとにdemoXX.netapp.comを変数へ格納
    $dns = "demo" + $number + ".netapp.com"
    
    #ユーザーの作成
    New-ADUser -SamAccountName cshandson$number-01 -Name cshandson$number-01 -DisplayName cshandson$number-01 -GivenName cshanson$number-01 -AccountPassword(ConvertTo-SecureString -AsPlainText "Netapp1!" -Force) -PasswordNeverExpires $true -Enabled $True
    New-ADUser -SamAccountName cshandson$number-02 -Name cshandson$number-02 -DisplayName cshandson$number-02 -GivenName cshanson$number-02 -AccountPassword(ConvertTo-SecureString -AsPlainText "Netapp1!" -Force) -PasswordNeverExpires $true -Enabled $True
    
    #Phase2の準備
    $filecontents = $(Get-Content "C:\Users\Administrator\deploy_2.ps1") -replace "demoXX","demo$number"
    $filecontents > "C:\Users\Administrator\deploy_2.ps1"
    $regRunOnceKey = "HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce"
    $powerShell = (Join-Path $env:windir "system32\WindowsPowerShell\v1.0\powershell.exe")
    $script = "c:\users\administrator\deploy_2.ps1"
    $restartKey = "Restart-And-RunOnce"

    Set-ItemProperty -path $regRunOnceKey -name $restartKey -value "$powerShell $script"
    Sleep 3
    #Zoneの追加
    Add-DnsServerPrimaryZone -Name $dns -ZoneFile $dns -DynamicUpdate NonsecureAndSecure -PassThru
    Start-Sleep 5
    #rendom /listの実行
    rendom /list
    #Domainlist.xmlの編集
    $filecontents = $(Get-Content "C:\Users\Administrator\Domainlist.xml") -replace "demo","demo$number"
    $filecontents > "C:\Users\Administrator\Domainlist.xml"
    #rendom /showforestの実行
    rendom /showforest
    #rendom /uploadの実行
    rendom /upload
    #rendom /prepareの実行
    rendom /prepare
    #rendom /executeの実行
    rendom /execute
    #Phase2の準備

    write "Deploy Phase 1 is Complete. Reboot Automatically and Please re-login. Then Deploy Phase 2 will Start Automatically."
    Stop-Transcript
    }

"n"{
    write "Deploy is Aborted. Please Re-run Deploy Script."
    sleep 3
    exit
    }
default{
    write "Please input y or n... \(;_;)/ Please Re-run Deploy Script."
    sleep 3    
    exit
    } 
}