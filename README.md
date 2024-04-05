# Corridor Counting

By _Anthony Bryson, Vincent Zhou, Amy Ha_

## Setup

In `AIC_2020_Challenge_Track-1/run.sh` and `AICITY2022_Track1_TAG/run.sh` replace _<user_email>_ with your email.

Make use of `virtualenv` to set up the environments for each module.

```
pip install virtualenv
```

### Counting Module (likely to be replaced)

To set up the counting module use the following commands.

```
cd AIC_2020_Challenge_Track-1
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Follow the instructions in `AIC_2020_Challenge_Track-1/README.md` to download the inference model _best.pt_.
NOTE: Don't download any datasets.

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
source AICITY2022_Track1_TAG/venv/bin/activate
module load Python
module load GCC
```

Extract frames from the videos.

```
python AICITY2022_Track1_TAG/detector/gen_images_aic.py aic.yml
```

Perform detection on the extracted frames.

```
bash AICITY2022_Track1_TAG/detector/yolov5/gen_det.sh aic.yml
```

Run Multi Camera Multi Vehicle Tracking to get universal id's.

```
bash AICITY2022_Track1_TAG/MCMVT.sh
```

Get the vehicle movements and link them to the universal id's.
NOTE: You may need to deactivate the virtual environment. If so, use `deactivate`.

```
python Corridor_Counting/assign_movements.py
```
