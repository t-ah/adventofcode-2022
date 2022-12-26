#!/bin/bash

if [ "$1" == "" ]; then
    echo "use: ./setup.sh START_DAY [FINAL_DAY]"
    exit 1
elif [ "$2" == "" ]; then
    TO=$1
else
    TO=$2
fi
FROM=$1

for (( i=$FROM; i<=$TO; i++ ))
do
    cp "template.py" "day${i}.py"
    sed -e "s/DAY-NR/${i}/g" -i "" "day${i}.py"
    touch "day${i}.txt"
done
