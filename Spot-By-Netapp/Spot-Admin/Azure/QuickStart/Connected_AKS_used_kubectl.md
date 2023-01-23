# Kubectl을 사용하여 AKS에 접속

Azure cli 와 Kubectl을 이용하여 AKS에 접속하는 방법에 대해 실습합니다.

## 전제 조건

- Azure CLI가 설치되어 있어야 합니다.
- AKS에 접근할 수 있는 권한이 있는 계정이 필요합니다.

## Kubectl을 사용하여 AKS에 접속

1. azure cli를 통해 Azure에 로그인 합니다.

```bash
az login
```

```
To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code S5ASZ297Y to authenticate.
```

2. 브라우저에 주소를 입력하고 코드입력란에 CLI에 표시된 코드를 입력합니다.
3. 로그인에 성공하면 브라우저 종료 안내 메세지와 함께 az cli 로그인이 성공합니다.
4. Cli의 기본값이 Hands on에 사용할 구독을 바라보고 있는지 확인합니다.

```bash
az account list --output table
```

```bash
Name               CloudName    SubscriptionId                        TenantId                              State    IsDefault
-----------------  -----------  ------------------------------------  ------------------------------------  -------  -----------
종량제             AzureCloud   e44f082a-6dbf-46e0-bdaa-7e485a9807ae  4949618e-15bd-4e73-8600-555f657fd9b1  Enabled  True
AzureCSP_NetAppKR  AzureCloud   3a49f80b-be29-4847-9d66-724a67d9f3d4  984e6d5f-7ea1-4394-8330-52e1f31b4097  Enabled  False
```

5. 맞지 않다면 기본값을 변경합니다.

```bash
az account set --subscription "<your subscribtion>"
```

6. az aks install-cli 명령을 사용하여 kubectl을 설치합니다.

```bash
az aks install-cli
```

7. aks 접속정보를 가져옵니다.

```bash
az aks get-credentials --resource-group NetappHandson-RG --name Handson-AKS
```

8. AKS서비스 조회 시 아래와 같은 결과가 출력됩니다.

```bash
wooyoung [ ~ ]$ kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.0.0.1     <none>        443/TCP   24h
wooyoung [ ~ ]$ 
```

# 참조

- [Connect an Existing AKS Cluster](https://docs.spot.io/ocean/getting-started/aks)
