# Corridor Counting

By _Anthony Bryson, Vincent Zhou, Amy Ha_

## Setup

In `Corridor_Counting/CC.sh` replace _<user_email>_ with your email.

Make use of `virtualenv` to set up the environments for each module.

```
pip install virtualenv
cd AICITY2022_Track1_TAG
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r detector/yolov5/requirements.txt
deactivate
```

### MTMCT Module

Pre-trained ReID models can be downloaded from [here](https://drive.google.com/drive/folders/1trYAwgsnB414IHcDfkqGSOTJzet0vkvx?usp=sharing). Put the ReID models into the folder `AICITY2022_Track1_TAG/reid_bidir/reid_model/`.

Download the [yolov5x model](https://github.com/ultralytics/yolov5/releases/download/v4.0/yolov5x.pt) (pretrained on COCO), and put it into the folder `AICITY2022_Track1_TAG/detector/yolov5/`.

### Dataset

Our results were on the dataset from track 1 of the 2022 AI City Challenge. The dataset should be put in `AICITY2022_Track1_TAG/datasets/`

You can create a symbolic link to this dataset.

```
cd AICITY2022_Track1_TAG
mkdir datasets
ln -s /WAVE/datasets/dmlab/aicity/aic22/track1 Dataset_A
```

Or you can download it from [here](https://www.aicitychallenge.org/2022-track1-download/).

## Running our solution

_NOTE: Running this pipeline will generate a large amount of intermediate results (up to ~50G at certain points) in `AICITY2022_Track1_TAG/datasets/`. Ensure this does not exceed your quota. This data can be removed afterwards with `AICITY2022_Track1_TAG/clean.sh`._

You can either run the full pipeline, or if some results have already been generated you can run the appropritate components.

The final corridor counts will be generated in `Corridor_Counting/predicted_counts.csv`

### Run the full pipeline

```
cd Corridor_Counting
sbatch CC.sh
```

### Run the components individually

_This assumes you have access to GPU's such as with an interactive job._

First load the environment.

```
cd AICITY2022_Track1_TAG
source venv/bin/activate
module load Python
module load GCC
```

Extract frames from the videos.

```
cd detector
python gen_images_aic.py aic.yml
```

Perform detection on the extracted frames.

```
cd yolov5
bash gen_det.sh aic.yml
```

Run Multi Camera Multi Vehicle Tracking to get universal id's and track vehicle movements.

```
cd ../..
bash MCMVT.sh
```

Count the vehicles that complete each corridor.

```
cd ../Corridor_Counting
python prediction_counting.py -s -f
```

Remove all intermediate data generated throughout the pipeline.

```
cd ../AICITY2022_Track1_TAG
bash clean.sh
```

## Evaluating the results

We use the normalized weighted root mean squared error (nwRMSE) as described by the [2020 AI City Challenge Track 1](https://www.aicitychallenge.org/2020-data-and-evaluation/) to calculate an effectiveness score. This metric divides the running corridor counts into k segments.

Our evaluation script can be run as follows:

```
cd Corridor_Counting
python evaluate.py <k>
```
