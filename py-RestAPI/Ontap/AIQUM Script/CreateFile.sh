#!/bin/bash
echo "target_directory = $1"
target_directory=$1
i=0
while [ true ]
do
   if [ -f "$target_directory/$i.txt" ]; then
      echo "create stop last file is $target_directory/$i.txt"
      break;
   else
      touch "$target_directory/$i.txt"
      if [ -f "$target_directory/$i.txt" ]; then
         break;
      fi
      i=$((i+1))
   fi
done

#sleep 300
i=0
while [ true ]
do
   if [ -f "$target_directory/$i.txt" ]; then
      rm -f "$target_directory/$i.txt"
      i=$((i+1))
   else
      echo "Delete Stop last file is $target_directory/$i.txt"
      break;
   fi
done
