#!/bin/sh
N="30"
for i in `seq $N`; do
    while read -u 3 Row
    do
    	ExperimentName=$(echo $Row |cut -d',' -f1)
    	ExperimentPackage=$(echo $Row |cut -d',' -f2)
    	ExperimentApk=$(echo $Row |cut -d',' -f3)
    	ExperimentUITest=$(echo $Row |cut -d',' -f4)
	
    	echo "Running $Row"
	
    	sh ./run_experiment.sh $ExperimentName $ExperimentPackage $ExperimentApk $ExperimentUITest
    done 3< experiment_stack.csv
done

echo "" | mail -s 'Experiment stack has finished running EOM' 'luis.miranda.cruz@fe.up.pt'
