---


---

<p>이번 Task는 Azure CVO에서 Tiering이 적용된 NFS 볼륨을 생성합니다. 동일 Subnet내의 Linux VM에 마운트 후 해당 NFS 볼륨에 데이터를 생성하여 Tiering  동적 여부를 확인합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/tiering_cvo.png?raw=true" alt="enter image description here"></p>
<h2 id="step-1.-tiering이-적용된-신규-nfs-볼륨-생성">Step 1. Tiering이 적용된 신규 NFS 볼륨 생성</h2>
<ol>
<li>
<p>Volumes GUI에서 Add New Volume을 클릭합니다</p>
</li>
<li>
<p>Details &amp; Protection는 아래와 같이 입력 후 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Volumes Name: Tiering_Vol</li>
<li>Size: 1</li>
<li>Snapshot Policy: default</li>
<li>Protocol: NFS</li>
<li>Access Control: Custom export policy</li>
<li>Custom export policy:  10.10.0.0/16</li>
</ul>
</li>
<li>
<p>Usage Profile, Disk Type &amp; Tiering Policy는 아래와 같이 입력 후 ‘Go’ 버튼을 클릭합니다.</p>
<ul>
<li>Storage Efficiency 선택</li>
<li>Storage Type: Standard SSD</li>
<li>Volume Tiering Policy: Auto</li>
</ul>
</li>
<li>
<p>볼륨이 정상적으로 생성된 것을 확인합니다.</p>
</li>
</ol>
<h2 id="step-2.-tiering-policy-변경">Step 2. Tiering Policy 변경</h2>
<ol>
<li>Tiering이 즉시 동작하기 위해서는 CVO의 System Manager에 접속하여 Policy를 변경해야 합니다.</li>
<li>Azure Portal에서 CVO VM에 Public IP를 할당합니다.
<ul>
<li>CVO VM의 Networking -&gt; Network Interface-&gt; IP configurations</li>
<li>Cluster-Management-Interface-Ip에서 Public IP address Enabled</li>
</ul>
</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/cvo_public_ip.PNG?raw=true" alt="enter image description here"></p>
<ol start="3">
<li>생성된 Public IP address를 이용해 웹 브라우저에서 CVO의 System Manager로 접속
<ul>
<li>URL: <a href="https://Public">https://Public</a> IP</li>
<li>Username: admin</li>
<li>Password: Netapp123!</li>
</ul>
</li>
<li>Volumes에서 해당 볼륨을 찾은 후 마우스 오른쪽 버튼을 눌러 Change Tiering Policy를 선택합니다.</li>
<li>Tiering Policy를 All로 선택 후 'Save’합니다.</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/tiering_policy.PNG?raw=true" alt="enter image description here"></p>
<ol start="7">
<li>Cloud Manager GUI에서 해당 볼륨의 Tiering Policy가 All로 변경된 것을 확인합니다.</li>
</ol>
<h2 id="step-3.-tiering-적용된-볼륨에-데이터-저장">Step 3. Tiering 적용된 볼륨에 데이터 저장</h2>
<ol>
<li>해당 볼륨의 ‘mount command’를 클릭합니다.</li>
<li>Mount command를 copy합니다.</li>
<li>해당 VNet내에 구성된 Linux VM에서 해당 볼륨을 마운트합니다.</li>
</ol>
<pre><code> mkdir /mnt/tiering 
 mount 10.10.1.8:/Tiering_Vol /mnt/tiering
</code></pre>
<ol start="4">
<li>해당 볼륨에 Centos Linux ISO 파일을 다운로드합니다.</li>
</ol>
<pre><code> cd /mnt/tiering 
 wget http://mirrors.huaweicloud.com/centos-altarch/7.6.1810/isos/aarch64/CentOS-7-aarch64-Minimal-1810.iso
</code></pre>
<ol start="5">
<li>다운로드 완료 후 Cloud Manager GUI에서 해당 볼륨에서 Azure Blob으로 tiering된 데이터 용량을 확인합니다.</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/blob.PNG?raw=true" alt="enter image description here"></p>

