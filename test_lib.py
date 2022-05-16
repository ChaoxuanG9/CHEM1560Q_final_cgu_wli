import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
import cirpy

from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import Descriptors
from rdkit.Chem import AllChem
from rdkit import DataStructs

#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=10:00:00
#SBATCH --mem-per-cpu=2G
#SBATCH -J 4427-96/
#SBATCH -o slurm-%j.out
#SBATCH -e slurm-%j.err
# SBATCH -A yqi27-condo