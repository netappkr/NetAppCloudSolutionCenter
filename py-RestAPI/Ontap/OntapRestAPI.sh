#!/bin/bash
# 참조 : https://aws.amazon.com/ko/premiumsupport/knowledge-center/fsx-ontap-rest-apis/
# 참조 : https://library.netapp.com/ecmdocs/ECMLP2882307/html/index.html#/ 
CRED=admin:"Netapp1!"
ONTAP="172.30.0.186"

IFS=$'\n' field_aggr=(
    files
    files-used,
    files-maximum-possible
)

for field in ${field_aggr[@]}
do
 fields="$fields$field,"
done

i=${#fields}-1
fields=${fields:0:$i}
curl -X GET -u ${CRED} -k https://${ONTAP}/api/private/cli/volume?fields=$fields
