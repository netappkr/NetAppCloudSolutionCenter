Start-Transcript "c:\users\administrator\deploylogs.txt"
    
    #ユーザーの作成
    New-ADUser -SamAccountName cshandson-01 -Name cshandson-01 -DisplayName cshandson-01 -GivenName cshanson-01 -AccountPassword(ConvertTo-SecureString -AsPlainText "Netapp1!" -Force) -PasswordNeverExpires $true -Enabled $True
    New-ADUser -SamAccountName cshandson-02 -Name cshandson-02 -DisplayName cshandson-02 -GivenName cshanson-02 -AccountPassword(ConvertTo-SecureString -AsPlainText "Netapp1!" -Force) -PasswordNeverExpires $true -Enabled $True
    Add-ADGroupMember -Identity "Domain Admins" -Members cshandson-01, cshandson-02

    write "2 users are created. Please check Active Directory"
    sleep 5
    Stop-Transcript