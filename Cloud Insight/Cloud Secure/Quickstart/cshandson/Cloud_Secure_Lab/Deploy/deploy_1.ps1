Start-Transcript "c:\users\administrator\deploylogs.txt"
    
    #Create User
    $photo= [byte[]](Get-Content C:\Users\Administrator\Desktop\frowny.jpg -Encoding byte)
    $i = 1
    While($i -le 5){
    $i2 = "{0:D2}" -f $i
    New-ADUser -SamAccountName cshandson-$i2 -Name cshandson-$i2 -DisplayName cshandson-$i2 -GivenName cshandson-$i2 -AccountPassword(ConvertTo-SecureString -AsPlainText "Netapp1!" -Force) -PasswordNeverExpires $true -Enabled $True -EmailAddress "cshandson@netappdemo.com" -Title "Security Administrator" -Manager "Administrator" -Department "Data Security" -Country "JP"
    Add-ADGroupMember -Identity "Domain Admins" -Members cshandson-$i2
    write "user cshandson-$i2 is created."
    Set-ADUser cshandson-$i2 -Replace @{thumbnailPhoto=$photo}
    Set-ADUser cshandson-$i2 -OfficePhone '012-3456-7890'
    $i +=1
    }
    write "5 users are created. Please check Active Directory"
    sleep 5
    Stop-Transcript