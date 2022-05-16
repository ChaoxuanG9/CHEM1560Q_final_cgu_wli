#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=2G
#SBATCH -J additives
#SBATCH -o slurm-%j.out
#SBATCH -e slurm-%j.err
# SBATCH -A yqi27-condo

date

# Load required modules
module load gaussian/g09-D01
module load python/3.9.0

start=$(date +%s)

# create Gaussian inputs for molecule and molecule with Li+
python3 create_input.py 

# run Gaussian
cd Gaussian
pwd
jobID=()
for dir in */
do
    cd $dir
    pwd
    cp ../../job_gauss.sh .
    sed -i "s@additives@${dir}@g" job_gauss.sh
    jid=$(sbatch job_gauss.sh | cut -f 4 -d' ')
    # echo $jid
    jobID+="${jid},"
    sleep 2
    cd ..
done

echo "waiting for the last job to finish"
while true
do
    # wait for last job to finish use the state of sacct for that
    sleep 1m
    # sacct shows your jobs
    sacct -j ${jobID} |grep -q 'RUNNING\|PENDING' #your job name indicator
    # check the status code of grep (1 if nothing found)
    if [ "$?" == "1" ];
    then
    echo "all jobs are completed"
    sacct -j ${jobID}
    break;
    fi
done
wait

# calculate the results
cd ..
python3 calc_result.py

end=$(date +%s)
date -d@$((end-start)) -u +"%j %T"
date