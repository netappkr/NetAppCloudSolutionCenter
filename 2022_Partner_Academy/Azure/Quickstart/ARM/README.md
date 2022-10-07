# Azure Resouce Manager Temaplate
Azure 솔루션의 코드형 인프라를 구현하려면 ARM 템플릿(Azure Resource Manager 템플릿)을 사용하세요. /<br>
해당 템플릿은 프로젝트에 대한 인프라 및 구성을 정의하는 JSON(JavaScript Object Notation) 파일입니다.</br>
이 템플릿은 대상을 만들기 위한 프로그래밍 명령 시퀀스를 작성하지 않고도 배포하려는 대상을 설명할 수 있는 선언적 구문입니다. 배포할 리소스와 해당 리소스의 속성을 템플릿에서 지정합니다.


## Visual Studio Code를 사용하여 ARM 템플릿 만들기
Visual Studio Code용 Azure Resource Manager 도구를 사용하여 탬플릿을 생성 합니다.
### 전제조건
[Azure Resource Manager 도구 확장](https://marketplace.visualstudio.com/items?itemName=msazurermtools.azurerm-vscode-tools)이 설치된 Visual Studio Code가 필요합니다. 또한 Azure CLI 또는 Azure PowerShell 모듈이 설치 및 인증되어 있어야 합니다.

1. arm!
- Azure 리소스 그룹 배포로 범위가 지정된 템플릿을 만들려면 arm!를 선택합니다.
![example](https://docs.microsoft.com/ko-kr/azure/azure-resource-manager/templates/media/quickstart-create-templates-use-visual-studio-code/1.png)
- 이 코드 조각은 ARM 템플릿의 기본 구성 요소를 만듭니다.
![example2](https://docs.microsoft.com/ko-kr/azure/azure-resource-manager/templates/media/quickstart-create-templates-use-visual-studio-code/2.png)
- Visual Studio Code 언어 모드가 JSON에서 Azure Resource Manager 템플릿으로 변경되었습니다. 이 확장에는 ARM 템플릿별 유효성 검사, 완성 및 기타 언어 서비스를 제공하는 ARM 템플릿과 관련된 언어 서버가 포함됩니다.
![example3](https://docs.microsoft.com/ko-kr/azure/azure-resource-manager/templates/media/quickstart-create-templates-use-visual-studio-code/3.png)

# 참조
- [Azure Doc ARM QuickStart](https://docs.microsoft.com/ko-kr/azure/azure-resource-manager/templates/quickstart-create-templates-use-visual-studio-code?tabs=CLI)
- [Azure Doc ARM 배포 순서 정의](https://learn.microsoft.com/ko-kr/azure/azure-resource-manager/templates/resource-dependency)
