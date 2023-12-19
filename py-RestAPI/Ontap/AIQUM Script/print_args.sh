#!/bin/bash
i=0
for argv in "$@"
do
  echo "argv[$i] :" $argv;
  i=$((i+1))
done

#Global Environment

addr="192.168.0.78"  #IP or Hostname입니다.
id="admin"  #c-mode 장비 로그인 id입니다.
vol="vol_src2"  #적용할 볼륨명입니다.
vserver="svm-src"  #해당 볼륨의 vserver입니다.
warn_per=80  #inode used percent가 몇% 이상일때 작동시킬지 정합니다. 현재는 80%기준입니다.
multi_val=1.66  #현재 inode used에 곱하여 볼륨의 max inode값을 설정합니다. 현재는 1.66x(80%→60%)입니다.

# Command
c_inode=`ssh -l $id $addr df -i $vol | grep $vol`
c_inode_used=`echo "$c_inode" | awk '{print $2}'`
# example
# CVO::> df -i vol
# Filesystem               iused      ifree  %iused  Mounted on                 Vserver
# /vol/vol/              3112959          0    100%  /vol                       svm_CVO
c_inode_used_per=`echo "$c_inode" | awk '{print $4}' | tr -d "%"`
c_inode_max=`ssh -l $id $addr vol show $vol -fields files | grep $vol | awk '{print $3}'`
if [ $c_inode_used_per -ge $warn_per ]
then

        t_inode_max=`echo "scale = 0; $c_inode_used * $multi_val" / 1 | bc`

        ssh -l $id $addr vol modify -vserver $vserver -volume $vol -files $t_inode_max

fi