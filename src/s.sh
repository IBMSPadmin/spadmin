> ~/spadmin/log/spadmin.log 

while :; do

 git pull

 ./spadmin.py

 if [ $? -ne 0 ] 
   then
     exit 1 
 fi

 echo "Press ctrl+c to exit!"
 sleep 2

done