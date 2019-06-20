# Comparison of sieve program for x86_64, arm, and qemu-arm on x86_64

## Compilation

The program *sieve.c* is compiled into *sieve* with the local gcc (gcc (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0).
The arm executable *sieve-arm* is made using the *armv7-eabihf-glibc-stable-2018.11-1* toolchain provided by [bootlin]( https://toolchains.bootlin.com/).

## Tests
The executables are ran in three different configurations:
1) **x86_64:** ./sieve 7000000 
2) **raspberry pi2:** ./sieve-arm 7000000
3) **qemu-arm on x86_64**: qemu-arm -L /home/user/armv7-eabihf--glibc--stable-2018.11-1/arm-buildroot-linux-gnueabihf/sysroot/ sieve-arm 7000000

All tests are timed and repeated 100 times. In a separate shell ps is ran to collect memory usage information.
This is done by using the following commands:
* for i in $(seq 0 99); do time **command 1, 2, or 3 **; done > sieve.txt 2> sieve_times.txt
* while true; do  ps u -q  \`pgrep **sieve, sieve-arm or qemu-arm**\` 2>/dev/null; sleep 0.2; done | tee sieve_mem.txt

## Results
For the three different configurations this results in:
1) sieve_native_times.txt and sieve_native_mem.txt
2) sieve_arm_times.txt and sieve_arm_mem.txt
3) sieve_qemu_times.txt and sieve_qemu_mem.txt
