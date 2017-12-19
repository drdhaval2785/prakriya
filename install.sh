#!/usr/bin/bash
mkdir data/json
cd data
read -p "Downloading the data. It will take 70 MBs or so. Press Enter to continue. Press Ctrl+C to exit." -n 1 -s
wget https://github.com/drdhaval2785/prakriya/releases/download/v0.0.2/derivation_v003.tar.gz
tar -zxvf derivation_v003.tar.gz
