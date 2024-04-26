# Corridor Counting

By _Anthony Bryson, Vincent Zhou, Amy Ha_

## Setup

In `AIC_2020_Challenge_Track-1/run.sh` and `AICITY2022_Track1_TAG/run.sh` replace _<user_email>_ with your email.

Make use of `virtualenv` to set up the environments for each module.

```
pip install virtualenv
```

### MTMCT Module

To set up the mtmct module use the following commands.

```
cd AICITY2022_Track1_TAG
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r detector/yolov5/requirements.txt
deactivate
```

Follow the instructions in `AICITY2022_Track1_TAG/README.md` to download the already trained ReID models and the detection model _yolov5x.pt_.
NOTE: Don't download any datasets and you don't need to run `bash gen_det.sh aic.yml`.

## Running our solution

You can either run the full pipeline, or if some results have already been generated you can run the appropritate components.

### Run the full pipeline

```
sbatch run.sh
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

## Evaluating the results

We use the normalized weighted root mean squared error (nwRMSE) as described by the [2020 AI City Challenge Track 1](https://www.aicitychallenge.org/2020-data-and-evaluation/) to calculate an effectiveness score. For this we split the videos into k=50 segments.

Our evaluation script can be run as follows:

```
cd Corridor_Counting
python evaluate.py
```

NOTE: This requires the ground truth be properly formatted. In `Corridor_Counting/ground_truth` we provide a script that formatted `ccd.csv` into `gt_sequence.txt` as an example.
