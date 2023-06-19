# smith@netapp.com
#
# PowerShell script that creates and enables an FPolicy designed to combat
# ransomware. Adapted from demo script created by Yaron Regev.
#
# (c) 2020 NetApp Inc., All Rights Reserved
#
# NetApp disclaims all warranties, excepting NetApp shall provide support
# of unmodified software pursuant to a valid, separate, purchased support
# agreement.  No distribution or modification of this software is permitted
# by NetApp, except under separate written agreement, which may be withheld
# at NetApp's sole discretion.
#
# THIS SOFTWARE IS PROVIDED BY NETAPP "AS IS" AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
# NO EVENT SHALL NETAPP BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#


# Loading PowerShell assemblies

Import-Module WriteLog | Out-Null


# response type and base64-encoded credentials data for -header parameter 
$header = @{"accept" = "application/hal+json"; "authorization" = "Basic YWRtaW46TmV0YXBwMSE=" }

################################################################################################
########## under normal conditions, no editing should be necessary beyond this point. ##########
################################################################################################

# Disable interactive prompt
$ErrorActionPreference = "stop"
$ConfirmPreference = 'None'

# Avoid certificate errors
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Add-Type @"
    using System;
    using System.Net;
    using System.Net.Security;
    using System.Security.Cryptography.X509Certificates;
    public class ServerCertificateValidationCallback
    {
        public static void Ignore()
        {
            ServicePointManager.ServerCertificateValidationCallback += 
                delegate
                (
                    Object obj, 
                    X509Certificate certificate, 
                    X509Chain chain, 
                    SslPolicyErrors errors
                )
                {
                    return true;
                };
        }
    }
"@
[ServerCertificateValidationCallback]::Ignore();



####################################################
### Create FPolicy protection against ransomware ###
####################################################
Write-LogTitle "Creating FPolicy protection against ransomware"

Write-LogInfo ""
Write-LogInfo "The first API call will gather informatiom about the target SVM..."
Read-Host "Press ENTER to continue...`n"
# Getting svm21 UUID
$resturi = "https://cluster2/api/svm/svms?name=svm21"
Write-LogInfo "Executing REST API: $resturi..."
try {
    $response = Invoke-RestMethod -header $header -method GET -uri $resturi
} catch {
    $apierror = $_ | ConvertFrom-json
    throw "method GET " + $resturi + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
$svm_uuid = $response.records.uuid

# Creating a CIFS FPolicy event
$resturi = "https://cluster2/api/protocols/fpolicy/$svm_uuid/events?return_records=true"
Write-LogInfo ""
Write-LogSuccess "--------------------------"
Write-LogInfo ""
Write-LogInfo "The next two API calls define the file operation types that will be used by the FPolicy."
Read-Host "Press ENTER to continue...`n"
Write-LogInfo ""
Write-LogInfo "Creating the CIFS FPolicy event that will be used to define the CIFS file operations that will trigger the FPolicy..."

Write-LogInfo "Executing REST API: $resturi..."
$payloadJSON = @"
{
"file_operations": { "create": true, "open": true, "read": true, "rename": true, "write": true},
"name": "cifs",
"protocol": "cifs",
"volume_monitoring": true
}
"@
try {
    $response = Invoke-RestMethod -header $header -method POST -uri $resturi -Body $payloadJSON
} catch {
    $apierror = $_ | ConvertFrom-json
    throw "method POST " + $resturi + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}

# Creating a NFS FPolicy event
$resturi = "https://cluster2/api/protocols/fpolicy/$svm_uuid/events?return_records=true"
Write-LogInfo ""
Write-LogInfo "Creating the NFS FPolicy event that will be used to define the NFS file operations that will trigger the FPolicy:"

Write-LogInfo "Executing REST API: $resturi..."
$payloadJSON = @"
{
"file_operations": { "create": true, "read": true, "rename": true, "write": true},
"name": "nfs",
"protocol": "nfsv3",
"volume_monitoring": true
}
"@
try {
    $response = Invoke-RestMethod -header $header -method POST -uri $resturi -Body $payloadJSON
} catch {
    $apierror = $_ | ConvertFrom-json
    throw "method POST " + $resturi + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}

# Creating a ransomware FPolicy policy
$resturi = "https://cluster2/api/protocols/fpolicy/$svm_uuid/policies?return_records=true"

Write-LogInfo ""
Write-LogSuccess "--------------------------"
Write-LogInfo ""
Write-LogInfo "The next API call creates the ransomware FPolicy using the two events, and the native engine. Included is the specified volume (vol1) and specified file extensions that will be blocked."
Read-Host "Press ENTER to continue...`n"
Write-LogInfo ""

Write-LogInfo "Executing REST API: $resturi..."
$payloadJSON = @"
{
"engine": { "name": "native" },
"events": [ "cifs", "nfs" ],
"mandatory": true,
"name": "FPolicy_policy_ransomware",
"scope": { "include_extension": [ "ecc", "ezz", "exx", "zzz", "xyz", "aaa", "WNCRY", "*cryp1", "abc", "ccc", "vvv", "*zepto", "xxx", "ttt", "micro", "encrypted", "locked", "crypto", "_crypt", "crinf", "r5a", "XRNT", "XTBL", "crypt", "R16M01D05", "pzdc", "good", "LOL!", "OMG!", "RDM", "RRK", "encryptedRSA", "crjoker", "EnCiPhErEd", "LeChiffre", "keybtc@inbox_com", "0x0", "bleep", "1999", "vault", "HA3", "toxcrypt", "magic", "SUPERCRYPT", "CTBL", "CTB2", "diablo6", "Lukitus", "locky" ],
           "include_volumes": [ "vol1" ]}
}
"@
try {
    $response = Invoke-RestMethod -header $header -method POST -uri $resturi -Body $payloadJSON
} catch {
    $apierror = $_ | ConvertFrom-json
    throw "method POST " + $resturi + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}

# Enabling the ransomware FPolicy policy
$resturi = "https://cluster2/api/protocols/fpolicy/$svm_uuid/policies/FPolicy_policy_ransomware"


Write-LogInfo ""
Write-LogSuccess "--------------------------"
Write-LogInfo ""
Write-LogInfo "The final API call enables the ransomware FPolicy that was just created:"
Read-Host "Press ENTER to continue...`n"
Write-LogInfo ""

Write-LogInfo "Executing REST API: $resturi..."
$payloadJSON = @"
{
"enabled": true,
"priority": 1
}
"@
try {
    $response = Invoke-RestMethod -header $header -method PATCH -uri $resturi -Body $payloadJSON
} catch {
    $apierror = $_ | ConvertFrom-json
    throw "method PATCH " + $resturi + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}



Write-LogInfo ""
Write-LogSuccess "--------------------------"
Write-LogInfo ""
Write-LogSuccess "The FPolicy is now enabled on vol1."
Write-LogInfo ""
pause


