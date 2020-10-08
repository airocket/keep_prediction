# keep_prediction
Disclaimer: for entertainment only, do not use for trading decisions.

## Installation

Start docker Postgres + timescale
```sh
docker-compose up -d --build
```

install requirements

```sh
pip3 install -r requirements.txt
```

or conda
```sh
sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
bash Anaconda3-2020.02-Linux-x86_64.sh
conda env create -f conda_env\environment.yml
conda activate keep
```

Start

```sh
python3 main.py
```

## Usage

Finished models are located in the model directory. Model building studies are in * .ipynb files.
The app tries to predict the KEEP-ETH price using market data and data from the eth.

## Plans for the future

Сollect more historical data and create new models based on them.
