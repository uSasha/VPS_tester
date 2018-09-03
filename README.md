## Test CPU performance of virtual servers.

Test script performs a lot of matrix multiplications on randomly generated ~150MB sparse matrices.

You start test on any computer executing:
`docker run usasha/vps_test`  
Output is\ number of seconds multiplications took, less is better.


You can also create, delete and test virtual servers on Hetzner using `vps_tester.HetznerTester`

Check examples in `examples.ipynb`
