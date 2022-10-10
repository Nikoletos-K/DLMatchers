#!/bin/bash
pythonPATH=$(pwd)

cecho(){
    RED="\033[0;31m"
    GREEN="\033[0;32m"
    YELLOW="\033[1;33m"
    # ... ADD MORE COLORS
    NC="\033[0m" # No Color

    printf "${!1}${2} ${NC}\n"
}

SEED=22

'
: '

model_types=('roberta' 'bert' )
model_names=('roberta-base' 'bert-base-uncased')

data_dirs=('dirty_amazon_itunes' 'abt_buy' 'dirty_walmart_amazon' 'dirty_dblp_acm' 'dirty_dblp_scholar')
max_lengths=(180 265 150 180 128)

for j in "${!model_types[@]}"; do
        for i in "${!data_dirs[@]}"; do
                cecho "YELLOW" "Start ${data_dirs[i]} ${model_types[j]}"
                python3 ./src/run_all.py --model_type=${model_types[j]} --model_name_or_path=${model_names[j]} --data_processor=DeepMatcherProcessor --data_dir=${data_dirs[i]} --train_batch_size=16 --eval_batch_size=16 --max_seq_length=${max_lengths[i]} --num_epochs=15.0 --seed=${SEED}
        done
        #break
done
