# Installation steps
## 1. Install Docker
Install the Dcoker Engine as described here: https://docs.docker.com/engine/install/
or here: https://www.upwork.com/resources/install-docker-engine

## 2. Create custom Docker image

#### 2.1 Create a local directory like `spadmin_build` and copy into the `spadmin_build` folder contents.
#### 2.2 Change directory to newly created:
`cd spadmin_build`
#### 2.3 Run command to build new image (internet connection required!):
`docker build  --tag ubuntu/dsmc:20230401 --rm .`

## 3. Start container with Dcoker Composer

