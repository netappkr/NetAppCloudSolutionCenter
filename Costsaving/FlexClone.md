---


---

<p>이번 Task는 Azure CVO내의 데이터가 저장된 NFS 볼륨에 대해 볼륨 복제 시 용량을 크게 줄여 줄 수 있는 Clone을 수행합니다.</p>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/flexclone.png?raw=true" alt="enter image description here"></p>
<h2 id="step-1.-기존-nfs-볼륨의-clone-수행">Step 1. 기존 NFS 볼륨의 Clone 수행</h2>
<ol>
<li>
<p>Task 1에서 생성한 No_Efficiency_Vol을 선택 후 'Clone’을 클릭합니다.</p>
</li>
<li>
<p>Clone 볼륨의 이름을 아래와 같이 입력 후 'Clone’을 클릭합니다.</p>
</li>
<li>
<p>Clone 볼륨 생성 완료 후 실제 사용된 용량을 확인합니다.</p>
</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/data_clone.PNG?raw=true" alt="enter image description here"></p>
<h2 id="step-2.-clone-볼륨에-데이터-생성">Step 2. Clone 볼륨에 데이터 생성</h2>
<ol>
<li>Clone 볼륨의 ‘mount command’를 클릭합니다.</li>
<li>Mount command를 copy합니다.</li>
<li>해당 VNet내에 구성된 Linux VM에서 해당 볼륨을 마운트합니다.</li>
</ol>
<pre><code> mkdir /mnt/no-efficiency-vol-clone
 mount 10.10.1.8:/No_Efficiency_Vol_Clone /mnt/no-efficiency-vol-clone
</code></pre>
<ol start="4">
<li>아래 명령어를 사용하여 해당 볼륨에 신규 데이터를 생성합니다.</li>
</ol>
<pre><code> dd if=/dev/zero bs=64K count=1000 of=/mnt/no-efficiency-vol-clone/write64KB
</code></pre>
<ol start="5">
<li>신규 데이터 생성 완료 후 해당 볼륨의 Disk Used에서 늘어난 용량을 확인합니다.</li>
</ol>
<p><img src="https://github.com/netappkr/NDX_Handsonworkshop-/blob/master/Costsaving/Images/cloneafterwrite.PNG?raw=true" alt="enter image description here"></p>

