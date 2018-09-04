## Test CPU performance of virtual servers.

Test script performs a lot of matrix multiplications on randomly generated ~150MB sparse matrices.

You start test on any computer executing:
`docker run usasha/vps_test`  
Output is\ number of seconds multiplications took, less is better.


You can also create, delete and test virtual servers on Hetzner using `vps_tester.HetznerTester`.
For this you should set path to ssh key and hetzner API key ('Save keys' section of examples).
 
Check examples in `examples.ipynb`


**WARNING:**
Hetzner will charge for every virtual server creation (1h costs from 0.004 EUR for shared 1vCPU 
up to 0.48 EUR for 32 dedicated vCPUs).

It is just a weekend project and it's not guaranteed that server will be deleted after test, 
so it's a good idea to check your Hetzner cloud panel after tests just in case something went wrong.
