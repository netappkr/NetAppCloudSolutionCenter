---


---

<p>이번 Task는 Azure CVO에서 Storage Efficiency가 적용된 NFS 볼륨을 생성합니다. 동일 Subnet내의 Linux VM에 마운트 후 해당 NFS 볼륨에 데이터를 생성하여 Storage Efficiency 동작 여부를 확인합니다.<br>
<img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/storage_efficiency.png?raw=true" alt="enter image description here"></p>
<h2 id="step-1.-no-storage-efficiency가-적용된-신규-nfs-볼륨에-데이터-생성">Step 1. No Storage Efficiency가 적용된 신규 NFS 볼륨에 데이터 생성</h2>
<ol>
<li>
<p>Volumes GUI에서 Add New Volume을 클릭합니다</p>
</li>
<li>
<p>Details &amp; Protection는 아래와 같이 입력 후 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Volumes Name: No_Efficiency_Vol</li>
<li>Size: 2</li>
<li>Snapshot Policy: default</li>
<li>Protocol: NFS</li>
<li>Access Control: Custom export policy</li>
<li>Custom export policy:  10.10.0.0/16</li>
</ul>
</li>
<li>
<p>Usage Profile, Disk Type &amp; Tiering Policy는 아래와 같이 입력 후 ‘Go’ 버튼을 클릭합니다.</p>
<ul>
<li>No Storage Efficiency 선택</li>
<li>Storage Type: Standard SSD</li>
<li>Volume Tiering Policy: Auto</li>
</ul>
</li>
<li>
<p>해당 볼륨의 ‘mount command’를 클릭합니다.</p>
</li>
<li>
<p>Mount command를 copy합니다.</p>
</li>
<li>
<p>해당 VNet내에 구성된 Linux VM에서 해당 볼륨을 마운트합니다.</p>
</li>
</ol>
<pre><code> mkdir /mnt/no-efficiency-vol
 mount 10.10.1.8:/No_Efficiency_Vol /mnt/no-efficiency-vol
</code></pre>
<ol start="7">
<li>아래 명령어를 사용하여 해당 볼륨에 신규 데이터를 생성합니다.</li>
</ol>
<pre><code> dd if=/dev/zero bs=16K count=100000 of=/mnt/no-efficiency-vol/write16KB
</code></pre>
<ol start="8">
<li>Cloud Manager에서 해당 볼륨의  info을 클릭하여 저장된 데이터 용량과 Storage Efficiency 정보를 확인합니다.</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/cvo_no_efficiency.PNG?raw=true" alt="enter image description here"></p>
<h2 id="step-2.-storage-efficiency가-적용된-신규-nfs-볼륨에-데이터-생성">Step 2. Storage Efficiency가 적용된 신규 NFS 볼륨에 데이터 생성</h2>
<ol>
<li>
<p>Volumes GUI에서 Add New Volume을 클릭합니다</p>
</li>
<li>
<p>Details &amp; Protection는 아래와 같이 입력 후 ‘Continue’ 버튼을 클릭합니다.</p>
<ul>
<li>Volumes Name: Efficiency_Vol</li>
<li>Size: 2</li>
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
<p>해당 볼륨의 ‘mount command’를 클릭합니다.</p>
</li>
<li>
<p>Mount command를 copy합니다.</p>
</li>
<li>
<p>해당 VNet내에 구성된 Linux VM에서 해당 볼륨을 마운트합니다.</p>
</li>
</ol>
<pre><code> mkdir /mnt/efficiency-vol
 mount 10.10.1.8:/Efficiency_Vol /mnt/efficiency-vol
</code></pre>
<ol start="7">
<li>아래 명령어를 사용하여 해당 볼륨에 신규 데이터를 생성합니다.</li>
</ol>
<pre><code> dd if=/dev/zero bs=16K count=100000 of=/mnt/efficiency-vol/write16KB
</code></pre>
<ol start="8">
<li>Cloud Manager에서 해당 볼륨의  info을 클릭하여 저장된 데이터 용량과 Storage Efficiency 정보를 확인합니다.</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/cvo_efficiency.PNG?raw=true" alt="enter image description here"></p>
<ol start="10">
<li>Step 1의 No_Efficiency_Vol 볼륨과 Step 2의 Efficiency_Vol 볼륨 사용량을 비교합니다.</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/comparison_vols.PNG?raw=true" alt="enter image description here"></p>

