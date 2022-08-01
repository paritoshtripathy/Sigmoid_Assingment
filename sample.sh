#!/bin/bash

component=$1
view=$2
scale=$3
count=$4
log_file=/home/sigmoid/scripting-assingment/file.log
current_time=`date "+%Y-%m-%d %H:%M:%S"`

if [[ $component == "INGESTOR" || $component == "JOINER" || $component == "WRANGLER" || $component == "VALIDATOR" ]]; then
        : 
else
	echo "Time: '$current_time ' Wrong input value for component: '$component'" >> $log_file
        echo "Please enter valid input for component. INGESTOR/JOINER/WRANGLER/VALIDATOR"
	exit
fi


if  [[ $view == "BID" || $view == "AUCTION"  ]]; then
        :
else
	echo "Time: '$current_time ' Wrong input value for Auction/Bid: '$view'" >> $log_file
        echo "Please enter valid input. AUCTION/BID"
	exit
fi

if  [[ $scale == "MID" || $scale == "HIGH" || $scale == "LOW"  ]]; then
        : 
else
	echo "Time: '$current_time ' Wrong input value for scale: '$scale'" >> $log_file
        echo "Please enter valid input of scale. HIGH/MID/LOW"
        exit
fi

if  [[ "$count" =~ ^[1-9]$ ]]; then
       : 
else
	echo "Time: '$current_time' Wrong input value for count: '$count' " >> $log_file
        echo "Please enter valid input for count between 1-9" 
	exit
fi

if [[ $view == "BID" ]]; then
        input2="vdopiasample-bid"
else
        input2="vdopiasample"
fi




> temp

flag=0
for x in $(cat sig.conf); do
	if [[ $(echo $x | awk -F';' '{print $1}') == "$input2" && $(echo $x | awk -F';' '{print $3}') == "$component" ]]; then
	       	echo "$x" | sed  "s/[0-9]/$count/g; s/LOW/$scale/g; s/MID/$scale/g; s/HIGH/$scale/g" >> temp
		flag=1
	else 
		echo "$x" >> temp
	
	fi
done

if [[ $flag == 0 ]]; then
	echo "Error"
	echo "Time: '$current_time' Component: '$component' for '$view' not found in conf file. " >> $log_file
	exit
else	
	:
fi

mv temp sig.conf


cat sig.conf
