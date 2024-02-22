#!/bin/bash
#
#SBATCH --job-name=TAG_test
#SBATCH --output=console.out
#
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:2
#SBATCH --mem-per-cpu=4G
#SBATCH --time=1-00:00:00
#
#SBATCH --mail-user=abryson@scu.edu
#SBATCH --mail-type=END

source venv/bin/activate
module load Python
module load GCC/12.3.0

cd detector
python gen_images_aic.py aic.yml

cd yolov5
bash gen_det.sh aic.yml

cd ../..
bash MCMVT.sh

deactivate
