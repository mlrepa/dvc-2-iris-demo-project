Directory Structure
--------------------

    .
    ├── README.md
    ├── models  <- compiled model .pkl or HDFS or .pb format
    ├── config  <- any configuration files
    ├── data
    │   ├── external <- external data
    │   ├── interim <- data in intermediate processing stage
    │   ├── processed <- data after all preprocessing has been done
    │   └── raw <- original unmodified data acting as source of truth and provenance
    ├── docs  <- usage documentation or reference papers
    ├── notebooks <- jupyter notebooks for exploratory analysis and explanation 
    ├── docker <- docker image(s) for running project inside container(s)
    └── src
        ├── data <- data prepare and/or preprocess
        ├── evaluate <- evaluating model stage code 
        ├── pipelines <- scripts of pipelines
        ├── report <- visualization (often used in notebooks)
        ├── train <- train model stage code
        ├── transforms <- transformations data code (e.g., augmentation) 
        └── utils.py <- auxiliary functions and classes
        

# Preparation

### 1. Clone this repository

```bash
git clone https://gitlab.com/7labs.ru/tutorials-dvc/dvc-2-iris-demo-project.git
```

cd dvc-2-iris-demo-project

### 2. Get data

Download iris.csv

```bash
wget -P data/raw/ -nc https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv
```         

It may not work for Windows. So, use the [this link](https://raw.githubusercontent.com/uiuc-cse/data-fa14/gh-pages/data/iris.csv) 
to load data into `data/raw/` folder


### 3. Initialize DVC init 

__1) Install DVC__ 
`pip install dvc`

[Link for installation instructions](https://dvc.org/doc/get-started/install)

__2) Initialize DVC init__
ONLY if you build the project from scratch. For projects clonned from GitHub it's already initialized.

Initialize DVC 
```bash
dvc init
```

Commit dvc init

```bash
git commit -m "Initialize DVC"
``` 

__3) Add remote storage for DVC (any local folder)__
```bash
dvc init
dvc config cache.type copy
dvc remote add -d default_storage /tmp/dvc-storage
```

### 4. Create .env file in `config/` folder 
```bash
GIT_CONFIG_USER_NAME=<git user>
GIT_CONFIG_EMAIL=<git email>
```
   
example

```bash
GIT_CONFIG_USER_NAME=mnrozhkov
GIT_CONFIG_EMAIL=mnrozhkov@gmail.com
```
    
### Setup docker tools and build docker image 
Tutorial should work beyond docker container BUT not tested. 

__1) Install Docker and docker-compose tools__  
Links may help:

* [Link to Docker installation instructions](https://docs.docker.com/install/)
* [Link to docker-compose instructions](https://docs.docker.com/compose/install/)

__2) Build docker image__

    ln -sf config/.env && docker-compose build
  
# Run     
    
Run docker container via docker-compose  

    docker-compose up

# Tutorial 
    
### Step 1: All in Junyter Notebooks 
- run all in Jupyter Notebooks

### Step 2: Move code to .py modules
- i.e. main funcitons and classes 


### Step 3: Add pipelines (stages) on Python modules

Pipeline (python) scripts location: `src/pipelines`

Main stages:

* __prepare_configs.py__: load config/pipeline_config.yml and split it into configs specific for next stages

* __featurize.py__: create new features

* __split_train_test.py__: split source dataset into train/test

* __train.py__: train classifier 

* __evaluate.py__: evaluate model and create metrics file

    
### Step 4: Automate pipelines (DAG) execution  
- add pipelines dependencies under DVC control
- add models/data/congis under DVC control

__1) Prepare configs__

Run stage:
```bash
dvc run -f stage_prepare_configs.dvc \
        -d src/pipelines/prepare_configs.py \
        -d config/pipeline_config.yml \
        -o experiments/split_train_test_config.yml \
        -o experiments/featurize_config.yml \
        -o experiments/train_config.yml \
        -o experiments/evaluate_config.yml \
        python src/pipelines/prepare_configs.py \ 
            --config=config/pipeline_config.yml
```

Reproduce stage: `dvc repro pipeline_prepare_configs.dvc`


__2) Features extraction__

```bash
dvc run -f stage_featurize.dvc \
    -d src/pipelines/featurize.py \
    -d experiments/featurize_config.yml \
    -d data/raw/iris.csv \
    -o data/interim/featured_iris.csv \
    python src/pipelines/featurize.py \
        --config=experiments/featurize_config.yml
```


this pipeline:
1) creates new dataset with new features (`data/interim/featured_iris.csv`)
2) generates stage file `pipeline_featurize.dvc`

Reproduce stage: `dvc repro pipeline_featurize.dvc`

        
__3) Split train/test datasets__

Run stage:

```bash
dvc run -f stage_split_train_test.dvc \
    -d src/pipelines/split_train_test.py \
    -d experiments/split_train_test_config.yml \
    -d data/interim/featured_iris.csv \
    -o data/processed/train_iris.csv \
    -o data/processed/test_iris.csv \
    python src/pipelines/split_train_test.py \
        --config=experiments/split_train_test_config.yml \
        --base_config=config/pipeline_config.yml
```

this stage:

1) creates csv files `train_iris.csv` and `test_iris.csv` in folder `data/processed`
2) generates stage file `pipeline_split_train_test.dvc`        

Reproduce stage: `dvc repro pipeline_split_train_test.dvc`


__4) Train model__ 

Run stage:
```bash
dvc run -f stage_train.dvc \
    -d src/pipelines/train.py \
    -d experiments/train_config.yml \
    -d data/processed/train_iris.csv \
    -o models/model.joblib \
    python src/pipelines/train.py \
        --config=experiments/train_config.yml \
        --base_config=config/pipeline_config.yml
```


this stage:

1) trains and save model
2) generates stage file `pipeline_train.dvc`        

Reproduce stage: `dvc repro pipeline_train.dvc`


__5) Evaluate model__

Run stage:
```bash
dvc run -f stage_evaluate.dvc \
    -d src/pipelines/evaluate.py \
    -d experiments/evaluate_config.yml \
    -d models/model.joblib \
    -m experiments/eval.txt \
    python src/pipelines/evaluate.py \
        --config=experiments/evaluate_config.yml \
        --base_config=config/pipeline_config.yml
```    
    

this stage:

1) evaluate model
2) save evaluating report (metrics file `experiments/eval.txt`)
3) generate stage file `pipeline_evaluate.dvc`

Reproduce stage: `dvc repro pipeline_evaluate.dvc`



# References used for this tutorial

1) [DVC tutorial](https://dvc.org/doc/tutorial) 
2) [100 - Logistic Regression with IRIS and pytorch](https://www.xavierdupre.fr/app/ensae_teaching_cs/helpsphinx/notebooks/100_Logistic_IRIS.html) 