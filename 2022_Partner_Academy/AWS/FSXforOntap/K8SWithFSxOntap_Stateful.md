# K8S와 AWS FSxontap 활용 예제
이번 활용예시에서는 redis를 stateful pod로 배포하고 메모리 백업 데이터를 FSXontap에 저장하는 방법에 대해 알아봅니다. 

## K8S Statefulset 이란?
replica 간에 영구 데이터가 필요한 데이터베이스와 같은 상태저장 어플리케이션을 K8S에 배포할 때 권장되는 set 입니다.</br>
반드시 Headress 서비스로 정의해야합니다. 클라이언트가 POD에 직접연결하며 새롭게 배포되더라도 동일한 DNS 및 IP를 유지하는것이 특징입니다.

## 전제조건
- k8s Cluster 
- AWS FSXontap : PV로 이용할 스토리지입니다. 
- trident : CSI로 FSXontap과 K8S간 연결을 지원합니다.
> ### Tips
> AWS FSx ontap 과 k8S 연결과정은 [Trident 설치](../Trident/intstall_Trident.md) 과정을 참고해주세요.
## 실습
1. redis 배포 </br>
- Namespace 생성
    ```bash
    kubectl create ns redis
    ```
- Headress 서비스 생성</br>
    vim redis-service.yaml
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: redis-service
      namespace: redis
      labels:
        app: redis
    spec:
      ports:
        - port: 6379
    clusterIP: None
      selector:
        app: redis
    ```
- configMap 생성</br>
    vim redis-configmap.yaml
    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: redis-ss-configuration
      namespace: redis
      labels:
        app: redis
    data:
      master.conf: |
        maxmemory 400mb
        maxmemory-policy allkeys-lru
        maxclients 20000
        timeout 300
        appendonly no
        dbfilename dump.rdb
        dir /data
      slave.conf: |
        slaveof redis-ss-0.redis-ss.redis 6379
        maxmemory 400mb
        maxmemory-policy allkeys-lru
        maxclients 20000
        timeout 300
        dir /data
    ```
- statefulset 생성</br>
    vim redis-statefulset.yml
    ```yaml
    apiVersion: apps/v1
    kind: StatefulSet
    metadata:
      name: redis-ss
      namespace: redis
    spec:
      serviceName: "redis-service"
      replicas: 2
      selector:
        matchLabels:
        app: redis
      template:
        metadata:
          labels:
            app: redis
        spec:
        initContainers:
        - name: init-redis
          image: redis:latest
          command:
          - bash
          - "-c"
          - |
            set -ex
            # Generate redis server-id from pod ordinal index.
            [[ `hostname` =~ -([0-9]+)$ ]] || exit 1
            ordinal=${BASH_REMATCH[1]}
            # Copy appropriate redis config files from config-map to respective directories.
            if [[ $ordinal -eq 0 ]]; then
              cp /mnt/master.conf /etc/redis-config.conf
            else
              cp /mnt/slave.conf /etc/redis-config.conf
            fi
          volumeMounts:
          - name: redis-claim
            mountPath: /etc
          - name: config-map
            mountPath: /mnt/
          containers:
          - name: redis
            image: redis:latest
            ports:
            - containerPort: 6379
            name: redis-ss
            command:
            - redis-server
            - "/etc/redis-config.conf"
            volumeMounts:
            - name: redis-data
            mountPath: /data
            - name: redis-claim
            mountPath: /etc
          volumes:
          - name: config-map
            configMap:
              name: redis-ss-configuration
      volumeClaimTemplates:
      - metadata:
          name: redis-claim
        spec:
          accessModes: [ "ReadWriteMany" ]
          resources:
            requests:
              storage: 1Gi
          storageClassName: fsxontap-nas
          # storageClassName: <your SC name>
      - metadata:
          name: redis-data
        spec:
          accessModes: [ "ReadWriteMany" ]
          resources:
            requests:
            storage: 1Gi
          storageClassName: fsxontap-nas
          # storageClassName: <your SC name>

    # default              
    # volumeClaimTemplates:
    # - metadata:
    #     name: redis-claim
    #     spec:
    #       accessModes: [ "ReadWriteOnce" ]
    #       resources:
    #         requests:
    #           storage: 1Gi
    # - metadata:
    #     name: redis-data
    #     spec:
    #       accessModes: [ "ReadWriteOnce" ]
    #       resources:
    #         requests:
    #           storage: 1Gi
    ```

2. redis 상태 확인</br>
- redis 내부에서 info 명령 사용하여 마스터 및 복제본의 상태를 파악합니다.
    ```bash
    kubectl exec -it redis-ss-1 -c redis -n redis -- /bin/bash
    bash-5.1# redis-cli
    127.0.0.1:6379> info replication
    # Replication
    role:slave
    master_host:redis-ss-0.redis-ss.redis
    master_port:6379
    master_link_status:up
    master_last_io_seconds_ago:5
    master_sync_in_progress:0
    slave_read_repl_offset:18970
    slave_repl_offset:18970
    slave_priority:100
    slave_read_only:1
    replica_announced:1
    connected_slaves:0
    master_failover_state:no-failover
    master_replid:2cfc7fdcdf3322c981250f854235ff0b92b39dfa
    master_replid2:0000000000000000000000000000000000000000
    master_repl_offset:18970
    second_repl_offset:-1
    repl_backlog_active:1
    repl_backlog_size:1048576
    repl_backlog_first_byte_offset:7519
    repl_backlog_histlen:11452
    127.0.0.1:6379>
    ```
- exit 명령으로 쉘에서 빠져나옵니다.
    ```bash
    127.0.0.1:6379> exit
    bash-5.1# exit
    exit
    ```
3. 상태가 저장되는지 확인</br>
redis는 인메모리 DB로 save를 하지 않으면 재부팅시 데이터가 날아갑니다.</br>
이번 실습에서는 fsxontap에 save 데이터를 저장하고 앱 종료시 IP,DNS pv를 유지된 상태로 다시 시작되는지 확인합니다.
    ```
    kubectl exec -it redis-ss-0 -c redis -n redis -- /bin/bash
    bash-5.1# redis-cli
    ```
- 마스터 노드로 접속되었는지 확인합니다.
    ```
    127.0.0.1:6379> info replication 
    # Replication
    role:master
    connected_slaves:0
    master_failover_state:no-failover
    master_replid:82de58ddabf0ee2f23a1d81bb901f02065a26b84
    master_replid2:0000000000000000000000000000000000000000
    master_repl_offset:0
    second_repl_offset:-1
    repl_backlog_active:0
    repl_backlog_size:1048576
    repl_backlog_first_byte_offset:0
    repl_backlog_histlen:0
    ```
- 데이터를 입력합니다.
    ```
    127.0.0.1:6379> set key1 value1
    OK
    127.0.0.1:6379> set key2 value2
    OK
    127.0.0.1:6379> set key3 value3
    OK
    127.0.0.1:6379> get key1
    "value1"
    127.0.0.1:6379> save
    OK
    ```
- backup 된 파일을 확인합니다.
    ```
    127.0.0.1:6379> exit
    bash-5.1# ls -al
    total 8
    drwxrwxrwx 2 99 99 4096 Sep 13 04:01 .
    drwxr-xr-x 1  0  0   42 Sep 13 03:58 ..
    -rw-r--r-- 1 99 99  138 Sep 13 04:01 dump.rdb
    bash-5.1# pwd
    /data
    bash-5.1# exit
    ```
- redis 앱을 종료 합니다.
    ```bash
    [root@ ~ redis]# k delete pod -n redis redis-ss-0
    pod "redis-ss-0" deleted
    ```
- 잠시후 redis 앱이 동일한 이름으로 재시작되면 데이터를 확인합니다.
    ```bash
    [root@ ~ redis]# k get pods -n redis
    NAME         READY   STATUS     RESTARTS   AGE
    redis-ss-0   0/1     Init:0/1   0          9s
    redis-ss-1   1/1     Running    0          27m
    [root@ip-172-31-0-48 redis]# k get pods -n redis
    NAME         READY   STATUS            RESTARTS   AGE
    redis-ss-0   0/1     PodInitializing   0          14s
    redis-ss-1   1/1     Running           0          27m
    [root@ip-172-31-0-48 redis]# k get pods -n redis
    NAME         READY   STATUS    RESTARTS   AGE
    redis-ss-0   1/1     Running   0          16s
    redis-ss-1   1/1     Running   0          27m

    [root@ ~ redis]# kubectl exec -it redis-ss-0 -c redis -n redis -- /bin/bash
    bash-5.1# redis-cli
    127.0.0.1:6379> get key1
    "value1"
    127.0.0.1:6379> 
    ```
#  결과
앱이 종료 재시작되는 상황에서도 데이터가 유지됩니다.

