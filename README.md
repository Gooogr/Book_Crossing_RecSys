# Book_Crossing_RecSys

Environment setup
```
conda create -n books python=3.9
conda activate books
pip3 install poetry
poetry install --with dev
```

Get raw data and create data folders
```
bash src/data/get_data.sh
```

Run snakemake
```
snakemake -c2 all
```

--------------

## Database 

Open MyPHPAdmin in `localhost:8080`:
* Login - root
* Password - pass
