# Simople spadmin.py starter

while :; do

 clear

 > ~/spadmin/log/spadmin.log 

 git pull

 ./spadmin.py --nowelcome --autoexec 'deb; sp show log'

 if [ $? -ne 0 ] 
   then
     exit 1 
 fi

 echo "Press ctrl+c to exit!"
 sleep 2

done