#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
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

# run Gaussian09 of the 6 different with-Li cases
# excute serially to avoid too many number of jobs
for subdir in */; do
    cd $subdir
    pwd
    date
    g09 < inp.txt > out.txt
    date
    cd ..
done
wait

echo "#Free energy of the original molecule:" > free_e.txt
grep "Sum of electronic and thermal Free Energies" inp0/out.txt >> free_e.txt

echo "#Free energy of the original complex:" >> free_e.txt
# find the lowest-energy configuration and create the reduced-state input
cp ../../create_best_li.py .
python3 create_best_li.py 'inp0' 'inp1' 'inp2' 'inp3' 'inp4' 'inp5' 'inp6'
rm create_best_li.py

# run Gaussian for the reduced complex
cd opt_inp
pwd
date
g09 < inp.txt > out.txt
date
cd ..

echo "#Free energy of the reduced complex:" >> free_e.txt
grep "Sum of electronic and thermal Free Energies" opt_inp/out.txt >> free_e.txt

end=$(date +%s)
date -d@$((end-start)) -u +"%j %T"
date