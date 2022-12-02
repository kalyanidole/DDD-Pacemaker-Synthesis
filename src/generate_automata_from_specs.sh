#!/bin/sh

for spec in `ls specs`
do
    for subspec in `ls specs/$spec/*.dc`
    do
        echo $subspec
        python src/spec_to_automata.py $subspec
    done
done