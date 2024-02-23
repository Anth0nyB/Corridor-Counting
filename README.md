# Corridor Counting

By _Anthony Bryson, Vincent Zhou, Amy Ha_

In `AIC_2020_Challenge_Track-1/run.sh` and `AICITY2022/Track1/TAG/run.sh` replace _<user_email>_ with your email.

Make use of `virtualenv` to set up the environments for each module

```
pip install virtualenv
```

## Counting Module

To set up the counting module use the following commands.

```
cd AIC_2020_Challenge_Track-1
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Follow the instructions in `AIC_2020_Challenge_Track-1/README.md` to download the inference model _best.pt_. NOTE: Don't download any datasets.

## MTMCT Module

To set up the mtmct module use the following commands.

```
cd AICITY2022_Track1_TAG
virtualenv -p python3.6 venv
source venv/bin/activate
pip install -r detector/yolov5/requirements.txt
deactivate
```

Follow the instructions in `AICITY2022_Track1_TAG/README.md` to download the already trained ReID models and the detection model _yolov5x.pt_. NOTE: Don't download any datasets and you don't need to run `bash gen_det.sh aic.yml`

## Running our solution

To run the full pipeline **_WIP_**

```
export ROOT=$PWD
...
```
