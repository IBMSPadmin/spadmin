#! /usr/bin/bash

#-----------------------------------------------------------------------------------
# TSM - SP

apt-get update && apt-get install -y --no-install-recommends curl openssh-server

SP_dir=/tmp/SP_kits
mkdir $SP_dir
cd $SP_dir
SP_path=https://www3.software.ibm.com/storage/tivoli-storage-management/maintenance/client/v8r1/Linux/LinuxX86_DEB/BA/v8120/
SP_file=8.1.20.0-TIV-TSMBAC-LinuxX86_DEB.tar
curl -LOk $SP_path$SP_file
apt-get remove -y curl
tar xf $SP_file
apt-get install $SP_dir/gskcrypt64_8.0-55.*.linux.x86_64.deb \
  $SP_dir/gskssl64_8.0-55.*.linux.x86_64.deb \
  $SP_dir/tivsm-api64.amd64.deb \
  $SP_dir/tivsm-ba.amd64.deb \
  && apt-get clean && apt-get -y autoremove
rm -Rf $SP_dir
rm -rf /var/lib/apt/lists/*

rm -Rf /opt/tivoli/tsm/license

rm -Rf /opt/tivoli/tsm/client/ba/README.htm
rm -Rf /opt/tivoli/tsm/client/ba/swidtag/
rm -Rf /opt/tivoli/tsm/client/ba/client_message.chg
rm -Rf /opt/tivoli/tsm/client/ba/README.htm
rm -Rf /opt/tivoli/tsm/client/ba/bin/{CS_CZ,DE_DE,ES_ES,FR_FR,HU_HU,IT_IT,JA_JP}
rm -Rf /opt/tivoli/tsm/client/ba/bin/{KO_KR,PL_PL,PT_BR,RU_RU,ZH_CN,ZH_TW}
rm -Rf /opt/tivoli/tsm/client/ba/bin/{images,plugins,vmscan,vmtsmvss}
rm -Rf /opt/tivoli/tsm/client/ba/bin/libTsmViSdkAPI.so
find /opt/tivoli/tsm/client/ba/bin/ -type f \( -iname "*" ! -iname "dsmadmc" ! -name "dsmclientV3.cat" \) -exec rm -f {} \;

rm -Rf /opt/tivoli/tsm/client/api/bin64/{CS_CZ,DE_DE,ES_ES,FR_FR,HU_HU,IT_IT,JA_JP}
rm -Rf /opt/tivoli/tsm/client/api/bin64/{KO_KR,PL_PL,PT_BR,RU_RU,ZH_CN,ZH_TW,sample}
rm -Rf /opt/tivoli/tsm/client/api/bin64/dsmcert
rm -Rf /opt/tivoli/tsm/client/api/bin64/libTsmViSdk.so
rm -Rf /opt/tivoli/tsm/client/api/bin64/libTsmViSdkAPI.so
rm -Rf /opt/tivoli/tsm/client/api/bin64/libVMcrypto.so
rm -Rf /opt/tivoli/tsm/client/api/bin64/libVMssl.so
rm -Rf /opt/tivoli/tsm/client/api/bin64/libcrypto.so.1.0.2
rm -Rf /opt/tivoli/tsm/client/api/bin64/libssl.so.1.0.2
rm -Rf /opt/tivoli/tsm/client/api/swidtag
rm -Rf /opt/tivoli/tsm/client/api/README_api.htm

mv /usr/lib64/libgsk8* /usr/lib/

#-----------------------------------------------------------------------------------
# motd
rm -f /etc/update-motd.d/*
rm -f /etc/legal

#-----------------------------------------------------------------------------------
# ssh server
/usr/bin/ssh-keygen -A
sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
sed -i 's/#PrintLastLog yes/PrintLastLog no/g' /etc/ssh/sshd_config
sed -i 's/#Banner none/Banner none/g' /etc/ssh/sshd_config
mkdir /root/.ssh
chmod 700 /root/.ssh
mkdir /run/sshd
