# Papers Name [link]

#TODO: Discussing the paper and the the figure

## Datasets

All the datasets used in the experiment, except CER-E, are open and can be downloaded from this [link](https://mega.nz/folder/qwwG3Qba#c6qFTeT7apmZKKyEunCzSg). The CER-E dataset can be obtained free of charge for research purposes following the instructions at this [link](https://www.ucd.ie/issda/data/commissionforenergyregulationcer/). We recommend storing the downloaded datasets in a folder named `datasets` inside this directory.

## How to Run and Replicate the Result
To run the code, you first need to set up the Python environment. This can be done using the `env.yml` file provided. Follow these steps to install and activate the environment using Conda:

- Install the environment:
   ```bash
   conda env create -f env.yml
   conda activate grin


Once the environment is set up, you can proceed with the benchmarks using the four datasets provided. Each dataset has its respective command for training and evaluation:

- AQI:
  ```bash
   python ss

- AQI36:
  ```bash
   python ss

- PEMSBAY
  ```bash
    python ss

- METRLA
  ```bash
    python ss

After training and evaluation, the results will be stored in directories named after each dataset:
  ```
  /path/to/results/aqi
  /path/to/results/aqi36
  /path/to/results/pemsbay
  /path/to/results/metrla


  ```


