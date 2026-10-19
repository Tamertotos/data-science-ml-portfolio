# spaceflights

[![Powered by Kedro](https://img.shields.io/badge/powered_by-kedro-ffc900?logo=kedro)](https://kedro.org)

## Screenshot
![alt text](<kedro-pipeline.png>)


## Overview
The project is about predicting the space flight price tags according to some data from companies,
reviews, shuttles data (csv, xlsx).

As seen in the kedro viz screenshot shuttle and companies data are cleaned and put from data/01_raw to
data/02_intermediate. Moreover,  reviews data is cleaned and then all three of them merged into model_input_table
and moved into data/03_primary to be used in the linear regression and evaluation of the model.

After applying Linear regression to merged data, r2_score is evaluated with two different type of pipeline -First is 
active_modelling_pipeline with more parameters than candidate_modelling_pipeline to see the difference in between
how accurately they fit to the data.


## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a data engineering convention
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, 'session', `catalog`, and `pipelines`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```
