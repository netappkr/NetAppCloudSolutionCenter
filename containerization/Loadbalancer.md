이번 Task는 K8S Cluster내의 Container를 외부에서 접속할 수 있는 S/W Load balancer Pod를 설치 합니다.

**사전 준비사항** 
 - [ ] [K8s Cluster 접속 환경 셋업](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/K8s_on_MultiCloud/OnPremNKS.md)    

## Step 1. MetalLB manifest  적용 

1. 이미 설치된  K8S Cluster에 접속합니다.
2.  Metallb yaml 파일을 다운 받아 Cluster 내에서 적용합니다. ([metallb.yaml](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/files/metallb.yaml))
   ` # kubectl apply -f metallb.yaml`

3.  MetalLB POD 정상 동작 동작을 확인합니다.

   `# kubectl get pods -n metallb-system`
 
4.  Metallb configmap 파일을 다운 받아 address 부분에 사전에 배정된 IP을 기입합니다. ([metallb_configmap.yaml](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/containerization/files/metallbconfigmap.yaml))
  <pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined">apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: my-ip-space
      protocol: layer2
      addresses:
      - xx.xx.xx.xx </code></pre>
      
## Step 2. External-IP Service  생성

1. Service 생성될 ghost라는 namespace를 생성합니다.

     `# kubectl create namespace ghost`
    
     
3. 생성된 ghost namespace를 확인합니다. 

    # kubectl get namespaces`
    
4.  Service yaml 파일을 다운 받아 ghost namesapce에 Service를 생성합니다.([ghost_service.yaml](https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/file/ghost_service.yaml))

    `# kubectl apply -f ghost_service.yaml -n ghost` 
       
5.  생성된 Service와 당 External IP를 확인합니다.
<pre class=" language-undefined"><code class="prism language-&quot;NotActions&quot;: language-undefined"># kubectl get svc -n ghost
NAME    TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)        AGE
ghost   LoadBalancer   10.255.100.23   115.144.174.247   80:31435/TCP   4h36</code></pre> 

> **해당 Service는 향후 Task 2 POD 배포시 사용될 예정** 

[메인 메뉴로 이동](https://github.com/netappkr/NDX_Handsonworkshop-/)
   
   


<!--stackedit_data:
eyJoaXN0b3J5IjpbOTQ4MDg5NTUsLTE0MzgzODM4MDgsLTE1MT
MxMzUyLDE4NjM0NjE2MzIsMTY1OTUxNzg5NCwxNjY4Nzk1NjE0
LDM3ODU0Nzc1MywtMTQ4MDg2OTEzLDg2NzY5NDg4NV19
-->
