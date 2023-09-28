while :; do

 > ~/spadmin/log/spadmin.log 

 git pull

 ./spadmin.py --nowelcome -a 'deb; sp show log; cls'

 if [ $? -ne 0 ] 
   then
     exit 1 
 fi

 echo "Press ctrl+c to exit!"
 sleep 2

done
