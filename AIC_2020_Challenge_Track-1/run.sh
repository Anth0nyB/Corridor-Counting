#!/bin/bash 
# 
#SBATCH --job-name=counting
#SBATCH --output=console.out 
# 
#SBATCH --partition=gpu
#SBATCH --nodes=1 
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=08:00:00 
#
#SBATCH --mail-user=<user_email>
#SBATCH --mail-type=END

source venv/bin/activate
python inference.py 1 31
deactivate
