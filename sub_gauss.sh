#!/bin/sh

cd /gpfs/data/yqi27/cgu13/CHEM1560Q/Gaussian
pwd
for dir in */
do
    cd $dir
    pwd
    cp ../job_gauss.sh .
    sbatch job_gauss.sh
    cd ..
done

