# Installation steps
## 1. Install Docker
Install the Docker Engine as described here: https://docs.docker.com/engine/install/
or here: https://www.upwork.com/resources/install-docker-engine

## 2. Start container with Docker Composer
Clone `spadmin_runtime` folder to local disk and `cd spadmin_runtime`

#### 2.1 Change TSM - SP server connection data's by local environment
Change connection information in `spadmin_runtime/dsm.sys` file.

#### 2.2 Set SSH login authorized keys
Add public key of authorized user's in `authorized_keys` file to enable ssh connection to container.

#### 2.3 SPadmin setup
Copy SPadmin file to `spadmin_runtime` folder as `spadmin_latest` and `chmod +x spadmin_latest`.

#### 2.3 Start container
`docker compose up`

#### 2.4 Test container connection
`ssh -p 2222 root@<docker server DNS name or IP>`

Use `ctrl + c` to stop container.

## 3. Start container as daemon
...
