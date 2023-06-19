Start-Transcript "c:\users\administrator\deploylogs.txt"
    
    #ユーザーの作成
    $i = 1
    While($i -le 5){
    $i2 = "{0:D2}" -f $i
    New-ADUser -SamAccountName cshandson-$i2 -Name cshandson-$i2 -DisplayName cshandson-$i2 -GivenName cshandson-$i2 -AccountPassword(ConvertTo-SecureString -AsPlainText "Netapp1!" -Force) -PasswordNeverExpires $true -Enabled $True
    Add-ADGroupMember -Identity "Domain Admins" -Members cshandson-$i2
    write "user cshandson-$i2 is created."
    $i +=1
    }
    write "5 users are created. Please check Active Directory"
    sleep 5
    Stop-Transcript