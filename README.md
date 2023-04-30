# Book_Crossing_RecSys

Environment setup
```
conda create -n books python=3.9
conda activate books
pip3 install poetry
poetry install --with dev
```

Edit files:
* ```.env``` - create from ```.env.example```
* ```.src\database\pgadmin_config.json``` - "Username" should be same as $POSTGRES_USER

Get raw data and create data folders
```
bash src/data/get_data.sh
```

Run snakemake
```
snakemake -c2 all
```

Create external volume
```
docker volume create book_postgres_volume
```

Run docker-compose
```
docker compose up
```

Update features database
```
python3 src/database/rewrite_postgres_table_with_csv.py
```
--------------

## Database 

pgadmin for postgres databse: `localhost:5050`

