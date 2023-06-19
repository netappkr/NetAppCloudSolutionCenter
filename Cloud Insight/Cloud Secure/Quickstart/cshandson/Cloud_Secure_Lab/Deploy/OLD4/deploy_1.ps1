Start-Transcript "c:\users\administrator\deploylogs.txt"
    
    #ユーザーの作成
    $d = Get-Date -Format "MMdd"
    New-ADUser -SamAccountName cshandson$d-01 -Name cshandson$d-01 -DisplayName cshandson$d-01 -GivenName cshandson$d-01 -AccountPassword(ConvertTo-SecureString -AsPlainText "Netapp1!" -Force) -PasswordNeverExpires $true -Enabled $True
    New-ADUser -SamAccountName cshandson$d-02 -Name cshandson$d-02 -DisplayName cshandson$d-02 -GivenName cshandson$d-02 -AccountPassword(ConvertTo-SecureString -AsPlainText "Netapp1!" -Force) -PasswordNeverExpires $true -Enabled $True
    Add-ADGroupMember -Identity "Domain Admins" -Members cshandson$d-01, cshandson$d-02

    write "2 users are created. Please check Active Directory"
    sleep 5
    Stop-Transcript