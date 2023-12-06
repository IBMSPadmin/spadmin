# Build Docker image
## Linux and Mac 
To build Ubuntu 22.04 based image use the next steps:
1. Clone `spadmin_build` folder to Linux server local disk.
2. `cd spadmin_build`
3. Add execution rights to dockerfile_setup.sh: `chmod +x dockerfile_setup.sh`
4. `docker build --tag doffy2023/dsmadmc:20231206 --rm --compress .` vagy log file miatt `docker build --tag doffy2023/dsmadmc:20231206 --rm --compress . 2>&1 | tee build.log`
5. If you have docker hub account push the image into it: `docker push doffy2023/dsmadmc:20231204`

The tag value `20231204` must be changed not to conflict the existing one.
