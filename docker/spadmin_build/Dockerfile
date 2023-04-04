
FROM ubuntu:22.04

LABEL "ubuntu"="22.04" "Spectrum Protect"="8.1.17" "openssh"="8.9p1"

RUN --mount=type=bind,source=./,target=/mnt /mnt/dockerfile_setup.sh 

EXPOSE 22/tcp
