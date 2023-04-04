# Build Docker image
To build Ubuntu 22.04 based image use the next steps:
1. Clone `spadmin_build` folder to Linux server local disk.
2. `cd spadmin_build`
3. `docker build  --tag doffy2023/dsmadmc:20230404 --rm --compress .`
4. `docker push doffy2023/dsmadmc:20230404`

The tag value `20230404` must be changed.