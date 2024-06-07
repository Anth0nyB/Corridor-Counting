#!/bin/bash
#
#SBATCH --job-name=corridor_counting
#SBATCH --output=console.out
#
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:2
#SBATCH --mem-per-cpu=4G
#SBATCH --time=2-00:00:00
#
#SBATCH --mail-user=abryson@scu.edu
#SBATCH --mail-type=END

### Load the environment ###
cd ../AICITY2022_Track1_TAG
source venv/bin/activate
module load Python
module load GCC

### Extract frames from videos ###
cd detector
python gen_images_aic.py aic.yml

### Perform vehcile detection ###
cd yolov5
bash gen_det.sh aic.yml

### Feature Extraction ###
cd ../../reid_bidir
python extract_image_feat.py "aic_reid1.yml"
python extract_image_feat.py "aic_reid2.yml"
python extract_image_feat.py "aic_reid3.yml"
python merge_reid_feat.py "aic.yml"

### MOT ###
cd ../tracker/MOTBaseline
sh run_aic.sh "aic.yml"
cd ../../reid_bidir/reid-matching/tools
python trajectory_fusion.py "aic.yml"

### MOVEMENT MATCHING ###
cd ../../../../Corridor_Counting
python assign_movements.py

### MTMCT ###
cd ../AICITY2022_Track1_TAG/reid_bidir/reid-matching/tools
python sub_cluster.py "aic.yml"
python gen_res.py "aic.yml"

### Counting ###
cd ../../../../Corridor_Counting
python prediction_counting.py -s -f

deactivate