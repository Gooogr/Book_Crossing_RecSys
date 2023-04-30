#! /bin/bash

wget http://www2.informatik.uni-freiburg.de/~cziegler/BX/BX-CSV-Dump.zip -O "data/raw/dataset_dump.zip"
unzip data/raw/dataset_dump.zip -d data/raw/
rm data/raw/dataset_dump.zip
