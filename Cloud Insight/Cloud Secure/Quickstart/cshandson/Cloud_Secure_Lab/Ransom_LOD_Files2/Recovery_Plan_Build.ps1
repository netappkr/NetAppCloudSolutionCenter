# created 2020-01-12 - yaron@netapp.com
#
# updated 2020-04-17 smith@netapp.com
#
# PowerShell script to create a Ransomware recovery plan using NetApp's RESTful API
# Recovery plan (Ansible playbook) includes the following:
#   - Identify and remove all CIFS shares (in case of NAS)
#   - Dismount volume from global namespace (in case of NAS)
#   - Disable all LUNs (in case of SAN)
#   - Unmap LUNs from initiator groups (in case of SAN)
#   - Clone volume based on identified Snapshot
#   - Map cloned LUNs to initiator groups (in case of SAN)
#   - Mount cloned volume (in case of NAS)
#   - Create a CIFS share for cloned volume (in case of NAS)
#   - Split cloned volume
#   - Rehost compromised volume to quarantined SVM
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
# Revision History
# 1.0 - Initial release using RESTful API instead of WFA.    2020-01-12
#

# Loading PowerShell assemblies

Import-Module WriteLog | Out-Null

##### Editable script control variables #####
$json_input_file = "C:\Users\Administrator.DEMO\Desktop\LOD\remediation_input.json"                         # source JSON file with volume information
$yaml_output_file = "C:\Users\administrator.DEMO\Desktop\ransomware_remediation_plan.yml" # output location for remediation plan document
$ransomware_svm_quarantine_name = "quarantine"                                            # name of quarantined SVM to move compromised workload to
$ad_username = 'administrator'
$ad_password = 'Netapp1!'
$maxtries = 10                                                                            # Maxmimum number of attempts to query job status before timeout

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


#################################################
### Gathering information and creating a plan ###
#################################################
Write-LogTitle "Gathering information about compromised workload and creating a remediation plan"
Write-LogInfo ""
### Get details about compromised volume from JSON file
Write-LogInfo "Getting workload details from input JSON file...`n"
$ransomware_volume_details = Get-Content -Raw -Path $json_input_file | ConvertFrom-Json
$ransomware_cluster_name = $ransomware_volume_details.cluster_name
$ransomware_svm_name = $ransomware_volume_details.svm_name
$ransomware_volume_name = $ransomware_volume_details.volume_name
$ransomware_detection_time = $ransomware_volume_details.detection_time

$nas_workload = $false
$san_workload = $false
$clusterurl = "https://$ransomware_cluster_name" # base URL for ONTAP REST API calls to the specified cluster

$yaml = "netapp_hostname: $ransomware_cluster_name" + "`n"
$yaml = $yaml + "netapp_account: admin`n"
$yaml = $yaml + "netapp_password: Netapp1!`n`n"

### Get the uuid of the compromised volume.
# Construct the URI for the method
$methodtype = "GET"
$methodpath = "/api/storage/volumes"
$parameters = "?name=" + $ransomware_volume_name + "&fields=*&return_records=true&return_timeout=15"
$uri = $clusterurl + $methodpath + $parameters

Write-LogSuccess "--------------------------"
Write-LogInfo ""
Write-LogInfo "Now the script has taken as input your JSON file with details about the attack. The next step is three API calls that gather information about the infected volume and SVM."
Read-Host "Press ENTER to continue...`n"
Write-LogInfo ""
Write-LogInfo "Getting UUID of compromised volume."
Write-LogInfo "Executing RESP API: $uri...`n"
# Invoke the method to get the volume uuid
try {
  $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri
} catch {
  $apierror = $_ | ConvertFrom-json
  throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
$ransomware_volume_uuid = $response.records.uuid  # uuid of source volume


### Get the global namespace path of the compromised volume.
# Construct the URI for the method
$methodtype = "GET"
$methodpath = "/api/storage/volumes/$ransomware_volume_uuid"
$parameters = "?fields=nas.path"
$uri = $clusterurl + $methodpath + $parameters
Write-LogInfo "Getting global namespace path of compromised volume."
Write-LogInfo "Executing REST API: $uri...`n"
# Invoke the method to get the volume snapshots sorted by create_time
try {
  $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri
} catch {
  $apierror = $_ | ConvertFrom-json
  throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
$ransomware_volume_path = $response.nas.path


##### Get the uuid of the svm.
# Construct the URI for the method
$methodtype = "GET"
$methodpath = "/api/svm/svms"
$parameters = "?name=" + $ransomware_svm_name + "&return_records=true&return_timeout=15"
$uri = $clusterurl + $methodpath + $parameters
Write-LogInfo "Getting UUID of SVM hosting compromised volume."
Write-LogInfo "Executing REST API: $uri...`n"
# Invoke the method to get the svm uuid
try {
  $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri
} catch {
  $apierror = $_ | ConvertFrom-json
  throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
$ransomware_svm_uuid = $response.records.uuid  # uuid of source volume


##### Find the most suitable Snapshot for the recovery efforts.
# Construct the URI for the method
$methodtype = "GET"
$methodpath = "/api/storage/volumes/$ransomware_volume_uuid/snapshots"
$parameters = "?return_records=true&return_timeout=15&order_by=create_time%20desc"
$uri = $clusterurl + $methodpath + $parameters
Write-LogSuccess "--------------------------"
Write-LogInfo ""
Write-LogInfo "The next API call determines the most recent snapshot taken before the attack time. This snapshot will be used for recovery."
Read-Host "Press ENTER to continue...`n"
Write-LogInfo ""
Write-LogInfo "Executing REST API: $uri..."
# Invoke the method to get the volume snapshots sorted by create_time
try {
  $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri
} catch {
  $apierror = $_ | ConvertFrom-json
  throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
if ($response.num_records -gt 0){
    $ransomware_snapshot_name = ($response.records | ?{[datetime]($_.create_time) -lt [datetime]($ransomware_detection_time)} | select -First 1).name
    $ransomware_snapshot_uuid = ($response.records | ?{[datetime]($_.create_time) -lt [datetime]($ransomware_detection_time)} | select -First 1).uuid
    $ransomware_volume_clone_name = $ransomware_volume_name+"_"+$ransomware_snapshot_uuid.Replace('-','_')
} else {
    throw "no valid snapshot was found."
}


### Find all CIFS shares associated with compromised volume.
# Construct the URI for the method
$methodtype = "GET"
$methodpath = "/api/protocols/cifs/shares"
$parameters = "?volume.uuid=" + $ransomware_volume_uuid + "&fields=*&return_records=true&return_timeout=15"
$uri = $clusterurl + $methodpath + $parameters
Write-LogInfo ""

Write-LogSuccess "--------------------------"

Write-LogInfo ""

Write-LogInfo "The last two API calls look for shares and LUNs of the volume so the remediation process can take those into account."

Read-Host "Press ENTER to continue...`n"

Write-LogInfo ""
Write-LogInfo "Getting NAS information for compromised volume."
Write-LogInfo "Executing REST API: $uri...`n"
# Invoke the method to get the volume snapshots sorted by create_time
try {
  $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri
} catch {
  $apierror = $_ | ConvertFrom-json
  throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
if ($response.num_records -gt 0){
    $nas_workload = $true
    $share_list = @()    
    $yaml = $yaml + "cifs_shares_unmount:`n"
    foreach ($item in $response.records){
        $share_name = $item.name
        $share_path = $item.path
        $yaml = $yaml + "  - { share_name: $share_name, svm_name: $ransomware_svm_name, share_path: $share_path }`n"
        $share_list += $share_name
    }
    $yaml = $yaml + "`n"
    $yaml = $yaml + "volume_unmount_namespace:`n  - { volume_name: $ransomware_volume_name, svm_name: $ransomware_svm_name, volume_junction_path: $ransomware_volume_path }`n`n"
    $yaml = $yaml + "clone_volume:`n  - { source_volume: $ransomware_volume_name, source_svm: $ransomware_svm_name, snapshot_name: $ransomware_snapshot_name, clone_name: $ransomware_volume_clone_name, clone_junction_path: $ransomware_volume_path }`n`n"
    $yaml = $yaml + "cifs_shares_mount:`n"
    foreach ($item in $response.records){
        $share_name = $item.name
        $share_path = $item.path
        $yaml = $yaml + "  - { share_name: $share_name, svm_name: $ransomware_svm_name, share_path: $ransomware_volume_path }`n"
    }
    $yaml = $yaml + "`n"
} else {
    $yaml = $yaml + "cifs_shares_unmount:`n`nvolume_unmount_namespace:`n`n"
    $yaml = $yaml + "clone_volume:`n  - { source_volume: $ransomware_volume_name, source_svm: $ransomware_svm_name, snapshot_name: $ransomware_snapshot_name, clone_name: $ransomware_volume_clone_name, clone_junction_path: $ransomware_volume_path }`n`n"
    $yaml = $yaml + "cifs_shares_mount:`n`n"
}


### Find all LUNs in the compromised volume.
# Construct the URI for the method
$methodtype = "GET"
$methodpath = "/api/storage/luns"
$parameters = "?svm.name=" + $ransomware_svm_name + "&location.volume.name=" + $ransomware_volume_name + "&fields=*,lun_maps.igroup.name,lun_maps.igroup.uuid,lun_maps.logical_unit_number&return_records=true&return_timeout=15"
$uri = $clusterurl + $methodpath + $parameters
Write-LogInfo "Getting SAN information for compromised volume."
Write-LogInfo "Executing REST API: $uri..."
# Invoke the method to get the volume snapshots sorted by create_time
try {
  $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri
} catch {
  $apierror = $_ | ConvertFrom-json
  throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
if ($response.num_records -gt 0){
    $san_workload = $true
    $lun_list = @()
    $yaml = $yaml + "san_unmap_luns:`n"
    foreach ($item in $response.records){
        $lun_name = $item.location.logical_unit 
        $lun_path = $item.name # In the form of /vol/vol_name/lun_name or /vol/vol_name/qtree_name/lun_name
        $lun_uuid = $item.uuid
        $lun_mapnum = $item.lun_maps.logical_unit_number
        $lun_mapig = $item.lun_maps.igroup.name
        $lun_mapiguuid = $item.lun_maps.igroup.uuid
        $lun_list += ,($lun_name,$lun_path,$lun_uuid,$lun_mapig,$lun_mapnum,$lun_mapiguuid)
        # Extract qtree/lun name for YAML file
        $lun_path_split = $lun_path.split('/')
        if ($lun_path_split.Length -eq 4) {
            # No qtree
            $lun_name_yaml = $lun_name
        } else {
            # There is a qtree
            $lun_name_yaml = $lun_path_split[3] + '/' + $lun_name
        }
        $yaml = $yaml + "  - { volume_name: $ransomware_volume_name, svm_name: $ransomware_svm_name, lun_name: $lun_name_yaml, lun_ig: $lun_mapig }`n"
    }
    $yaml = $yaml + "`n"
    $yaml = $yaml + "san_offline_luns:`n"
    foreach ($item in $response.records){
        $lun_name = $item.location.logical_unit 
        $lun_path = $item.name # In the form of /vol/vol_name/lun_name or /vol/vol_name/qtree_name/lun_name
        $lun_uuid = $item.uuid
        $lun_mapnum = $item.lun_maps.logical_unit_number
        $lun_mapig = $item.lun_maps.igroup.name
        $lun_mapiguuid = $item.lun_maps.igroup.uuid
        # Extract qtree/lun name for YAML file
        $lun_path_split = $lun_path.split('/')
        if ($lun_path_split.Length -eq 4) {
            # No qtree
            $lun_name_yaml = $lun_name
        } else {
            # There is a qtree
            $lun_name_yaml = $lun_path_split[3] + '/' + $lun_name
        }
        $yaml = $yaml + "  - { volume_name: $ransomware_volume_name, svm_name: $ransomware_svm_name, lun_name: $lun_name_yaml }`n"
    }
    $yaml = $yaml + "`n"
    $yaml = $yaml + "san_map_luns:`n"
    foreach ($item in $response.records){
        $lun_name = $item.location.logical_unit 
        $lun_path = $item.name # In the form of /vol/vol_name/lun_name or /vol/vol_name/qtree_name/lun_name
        $lun_mapnum = $item.lun_maps.logical_unit_number
        $lun_mapig = $item.lun_maps.igroup.name
        # Extract qtree/lun name for YAML file
        $lun_path_split = $lun_path.split('/')
        if ($lun_path_split.Length -eq 4) {
            # No qtree
            $lun_name_yaml = $lun_name
        } else {
            # There is a qtree
            $lun_name_yaml = $lun_path_split[3] + '/' + $lun_name
        }
        $yaml = $yaml + "  - { volume_name: $ransomware_volume_clone_name, svm_name: $ransomware_svm_name, lun_name: $lun_name_yaml, lun_ig: $lun_mapig, lun_mapid: $lun_mapnum }`n"
    }
    $yaml = $yaml + "`n"
} else {
    $yaml = $yaml + "san_unmap_luns:`n`nsan_offline_luns:`n`nsan_map_luns:`n`n"
}
$yaml = $yaml + "volume_svm_rehost:`n  - { volume_name: $ransomware_volume_name, source_svm: $ransomware_svm_name, destination_svm: $ransomware_svm_quarantine_name }`n"


### write YAML data to file
Write-LogInfo ""

Write-LogSuccess "--------------------------"

Write-LogInfo ""

Write-LogInfo "Finally the script writes the gathered information to a properly formatted YAML file that is used by the remediation playbook."

Read-Host "Press ENTER to continue...`n"

Write-LogInfo ""
Write-LogInfo "Writing remediation plan to output YAML file...`n"
$yaml | Out-File -FilePath $yaml_output_file -Encoding ascii -Force | Out-Null
Write-Host "*********************************"
Write-LogInfo ""
Write-LogSuccess "Done"
Write-LogInfo ""
# Prep completed

Write-Host "Ransomware remediation plan ready ($yaml_output_file).`n"

Read-Host "Press ENTER to continue...`n"
