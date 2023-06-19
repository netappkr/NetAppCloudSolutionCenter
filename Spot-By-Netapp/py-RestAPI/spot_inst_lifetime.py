import pandas as pandas
import glob
import os
import json
import re
launch_ec2_dt = pandas.DataFrame()
detach_ec2_dt = pandas.DataFrame()
for filename in glob.glob('*.json'):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        jsondata=json.load(f)
    jsondata=jsondata['response']['items']
    for data in jsondata:
        ec2_launched_date = None
        ec2_detached_date = None
        Reason = None
        is_launched=re.findall('have been launched',data['message'])
        if is_launched:
            ec2_launched_date = data['createdAt']
        is_detached=re.findall('have been detached',data['message'])
        if is_detached: 
            ec2_detached_date = data['createdAt']
        Reason = str(data['message'])
        if Reason.find("Reason") != -1:
            Reason = Reason[Reason.find("Reason"):]
        else:
            Reason = None

        # instaance ID 추출 정규식 i-[a-z0-9]{17}
        ec2_ids=re.findall('i-[a-z0-9]{17}',data['message'])
        if ec2_ids:
            if  ec2_launched_date:
                for ec2_id in ec2_ids:
                    ec2_id_value=ec2_id
                    add=pandas.DataFrame.from_records([{
                        'InstanceId': ec2_id,
                        'lanch_at': ec2_launched_date
                    }])
                    launch_ec2_dt=launch_ec2_dt.append(add,ignore_index = True)
            elif ec2_detached_date:
                for ec2_id in ec2_ids:
                    ec2_id_value=ec2_id
                    add=pandas.DataFrame.from_records([{
                        'InstanceId': ec2_id,
                        'detach_at': ec2_detached_date,
                        'message' : Reason
                    }])
                    detach_ec2_dt=detach_ec2_dt.append(add,ignore_index = True)

df_OUTER_JOIN = pandas.merge(launch_ec2_dt,detach_ec2_dt,left_on='InstanceId',right_on='InstanceId',how='outer')

with pandas.ExcelWriter('instance_lifetime_history.xlsx') as writer: 
    df_OUTER_JOIN.to_excel(writer,sheet_name='instance_lifetime_history', index=False)
