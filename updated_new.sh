#!/bin/bash

file=/home/sigmoid/scripting-assingment/sig.conf

if [ "$1" == 'Auction' ]; then
	ab='vdopiasample'
	temp='vdopiasample-bid'
	ln=$(cat $file | grep -iwn $ab | grep -v $temp | grep -w $2| awk -F ':' '{print $1}')

elif [ "$1" == 'Bid' ]; then
	ab='bid'
	temp='vdopiasample'
	ln=$(cat $file | grep -iwn $ab | grep -w $2| awk -F ':' '{print $1}')

else 
	echo "Invalid Input"
fi


ln="${ln}s"
echo "$ln"
if [ "$3" == 'LOW' ] || [ "$3" == 'MID' ] || [ "$3" == 'HIGH' ]; then
        sed -i "$ln/LOW/$3/; $ln/MID/$3/; $ln/HIGH/$3/" $file
else
        echo "ERROR"
fi

if [ $4 -ge 0 ] && [ $4 -le 9 ]; then
        sed -i "$ln/vdopia-etl=.*/vdopia-etl=$4/" $file
else
        echo "ERROR"
fi

cat $file

