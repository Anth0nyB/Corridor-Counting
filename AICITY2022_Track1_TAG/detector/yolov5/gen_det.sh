# Get the number of available GPUs
num_gpus=$(nvidia-smi --query-gpu=count --format=csv,noheader | wc -l)

seqs=(c041 c042 c043 c044 c045 c046) 

# Loop through sequence IDs
for ((i = 0; i < ${#seqs[@]}; i += num_gpus)); do
    # Loop through available GPUs
    for ((j = 0; j < num_gpus && i + j < ${#seqs[@]}; j++)); do
        idx=$((i + j))
        seq=${seqs[$idx]}
        CUDA_VISIBLE_DEVICES=$j python detect2img.py --name $seq --weights yolov5x.pt --conf 0.1 --agnostic --save-conf --img-size 640 --classes 2 5 7 --exist-ok --cfg_file $1 &
    done
    wait
done
