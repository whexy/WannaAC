#!/bin/bash

if [[ -z "$3" ]]; then
    echo -e '{\n    "returnVal": "-1",\n    "message": "Too few arguments!"\n}'
    exit -1
elif ! [[ $3 =~ ^[0-9]+$ ]]; then
    echo -e '{\n    "returnVal": "-1",\n    "message": "Invalid timeout!"\n}'
    exit -1
elif [ ! -d data/$2 ]; then
    echo -e '{\n    "returnVal": "-1",\n    "message": "Problem not found!"\n}'
    exit -1
fi

# Preprocess

file=$1
prob=$2
timeout=$3
serial=$(date +"%Y%m%d%H%M%S_%N")
prog=${file%%.*}
cases=100

if [[ ! -z "$4" && $4 =~ ^[0-9]+$ ]]; then
    cases=$(($4 + 0))
fi

if [[ $file == *.java ]]; then
    type='java'
elif [[ $file == *.cpp ]]; then
    type='cpp'
fi

# Compile & run

if [ ! -d run ]; then
    mkdir run/
fi

mkdir run/$serial/

if [ ! -f code/$file ]; then
    echo -e '{\n    "returnVal": "-1",\n    "message": "Source file not found!"\n}'
    exit -1
fi

cp code/$file run/$serial/
cd run/$serial/

if [ $type == 'cpp' ]; then
    g++ $file -o $prog -lm -std=c++17
elif [ $type == 'java' ]; then
    javac $file
fi

for ((i = 0; i < $cases && $? == 0; i++)); do
    ../../data/$prob/data.py > data.in
    ../../data/$prob/std < data.in > std.out
    if [ $type == 'cpp' ]; then
        timeout $timeout ./$prog < data.in > user.out
    elif [ $type == 'java' ]; then
        timeout $timeout java $prog < data.in > user.out
    fi
    diff -Bbwq std.out user.out > /dev/null 2>&1
done

# Output json

if [ $? == 0 ]; then
    echo "{"
    echo "    \"returnVal\": \"0\","
    echo "    \"message\": \"Test passed\","
    echo "    \"runtimeStatus\": \"0\","
    echo "    \"runtimeSerial\": \"${serial}\""
    echo "}"
else
    testInput=$(cat data.in)
    stdOutput=$(cat std.out)
    userOutput=$(cat user.out)

    echo "{"
    echo "    \"returnVal\": \"0\","
    echo "    \"message\": \"Test failed\","
    echo "    \"runtimeStatus\": \"1\","
    echo "    \"input\": \"${testInput}\","
    echo "    \"std\": \"${stdOutput}\","
    echo "    \"user\": \"${userOutput}\","
    echo "    \"runtimeSerial\": \"${serial}\""
    echo "}"
fi

