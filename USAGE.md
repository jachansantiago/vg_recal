# USAGE
Instruction to runs this experiments.
More info about how works [click here](https://github.com/binarySequoia/vg_recal#characterizing-mapping-quality-recalibration-approaches-in-a-variant-graph-genomics-tool).

## TABLE OF CONTENTS
- [Getting Started](#getting-started)
    * [Dependecies](#dependecies)
    * [Install](#install)
    * [Get Data](#get-data)
- [Building a vg Graph](#building-a-vg-graph)
- [Reads Simulation](#reads-simulation)
    * [Data Generation](#training-and-testing-data-generation)
    * [Data Labeling](#label-training-and-testing-data)
- [Models](#models)
   * [Vowpal Wabbit Models](#vowpal-wabbit-model)
   * [other models](#other-models)
- [jupyter notebook](#notebooks)
- [py_scripts](#py_scripts)
- [scripts](#scripts)
   
           

## Getting Started
This repo contains three folders that are part of our tools for this project. 
- **notebooks** : are Jupyter notebooks with data processing pipeline, keras models, and analysis. 
- **py_scripts**: this python scripts contains training model pipeline, keras models, data generation, shell script generation and stats generation. 
- **scripts** : this contains useful automatize code, for data generation, data labeling, and models using vowpal_wabbit inside vg.


### Dependecies
* [vg](https://github.com/vgteam/vg)
* Jupyter Notebook
* SciPy
* Keras
* R 

### Install
```bash
git clone https://github.com/binarySequoia/vg_recal.git
```

### Get Data
```bash
cd vg_recal
wget -r -np -nH --cut-dirs=3 -R "index.html*" http://public.gi.ucsc.edu/~anovak/outbox/jeffrey/data/
```

## Building a vg graph
<pre><code>vg construct -r <i>[fasta file]</i> -v <i>[vcf file]</i> > vg_graph.vg</code></pre>
We are using vg graphs in xg/gcsa index pair format. To create this format run the following line.
```bash
# store the graph in the xg/gcsa index pair
vg index -x vg_graph.xg -g vg_graph.gcsa -k 16 vg_graph.vg
```

If you want to know more about vg functionalities, please go to [vg](https://github.com/vgteam/vg). 

***NOTE:  The data folder already contains the xg and gcsa files to work.***

## Reads Simulation
### Training and testing data generation

To generate data we are using _vg sim_.
<pre><code>vg sim -x <i>[xg file]</i> -n <i>[data size]</i> -l <i>[read size]</i> \
       -i [indel rate] --sub-rate <i>[base substitution rate]</i> --random-seed 1 -a > simulated.gam
</code></pre>

To create our training amd testing reads we run:
```bash
# Generate Training data
vg sim -x data/genome_data/snp1kg-CHR21.xg -n 1000000 -l 100 -i 0.001 --sub-rate 0.01 --random-seed 1 -a > train_sim_len100.gam
# Genearte Testing data
vg sim -x data/genome_data/snp1kg-CHR21.xg -n 1000000 -l 100 -i 0.001 --sub-rate 0.01 --random-seed 42 -a > test_sim_len100.gam
```
These scripts create a 1,000,000 reads for testing and training. Each read has 100 base pair with a error sample of 0.01.

### Label training and testing data
After run _vg sim_ we have simulated reads that are similar to some region in the genome graph but not the same. Now for label the read we are will try map those reads back to the same place in the graph. If a read is map in the same place we label that read as correct, if not we label that read as incorrect.

Now, for do that we need to use _vg map_ and _vg annotate_.

<pre><code>vg map -x <i>[xg file]</i> -g <i>[gcsa file]</i> -G simulated.gam | vg annotate -x <i>[xg file]</i>  -a - -p > mapped.gam</code></pre>


To Mapping our training amd testing reads we run:
```bash
# Mapping Training data
vg map -x data/genome_data/snp1kg-CHR21.xg -g data/genome_data/snp1kg-CHR21.gcsa 
     -G train_sim_len100.gam | vg annotate -x -x data/genome_data/snp1kg-CHR21.xg  -a - -p > train_mapped_len100.gam
# Mapping Testing data
vg map -x data/genome_data/snp1kg-CHR21.xg -g data/genome_data/snp1kg-CHR21.gcsa 
     -G test_sim_len100.gam | vg annotate -x -x data/genome_data/snp1kg-CHR21.xg  -a - -p > test_mapped_len100.gam
```
After have these mapping, now we can label them.
<pre><code>vg gamcompare -r <i>[distance threshold]</i> mapped.gam simulated.gam > labeled.gam</code></pre>

The distance threshold means distance within which to consider reads correct.

For label our data we run:
```bash
# Label Train reads
vg gamcompare -r 100 train_mapped_len100.gam train_sim_len100.gam > train_compared_len100.gam
# Label Test reads
vg gamcompare -r 100 test_mapped_len100.gam test_sim_len100.gam > test_compared_len100.gam
```

## Models
At the begining of this project we are using C++ to develop our models using vowpal-wabbit. But because we want to try more deep learning approaches we move to python for fast prototyping and when we got a good model load that model in a C++ framework. In this repo you can found implementation of sklearn and keras, but vowpal-wabbit implemetation you can found in this [special fork of vg](https://github.com/binarySequoia/vg).

| model         | framework     |
| ------------- |:-------------:|
| Logistic Regression with mappinq quality and metadata  | vowpal-wabbit     |
| Logistic Regression with Bag of words | vowpal-wabbit |
| Logistic Regression with mems     | vowpal-wabbit     |
| Logistic Regression with mems stats | vowpal-wabbit |
| Logistic Regression with mappinq quality| sklearn |
| Logistic Regression with mappinq quality and metadata | sklearn |
| Neural Network with mapping quality and metadata | keras |
| Neural Network with bag of words | keras |

### vowpal wabbit model
Vowpal Wabbit models are inside in my [special fork of vg](https://github.com/binarySequoia/vg). 

#### Train
```bash
vg recalibrate --model recal.model --train train_compared_len100.gam
```
#### Test
`vg recalibrate` has multiples options for choose a model.
```bash
# Prediction for training data
vg recalibrate --model recal.model train_mapped_len100.gam > train_recalibrated.gam
# Prediction for testing data
vg recalibrate --model recal.model test_mapped_len100.gam > test_recalibrated.gam
```
#### Evaluate
```bash
# Load recalibrated data
vg gamcompare -r 100 - simulated_len100.gam --tsv --aligner recal > stats_len100.tsv
# Load original data
vg gamcompare -r 100 mapped_len100.gam simulated_len100.gam --tsv --aligner orig | sed 1d >>stats_len100.tsv
```
#### Analyze Evaluation
```bash
Rscript vg/scripts/plot-qq.R stats_len100.tsv qq-plot_len100.svg
Rscript vg/scripts/plot-roc.R stats_len100.tsv roc-plot_len100.svg
```
### other models
Sklearn and keras models are in jupyter notebooks and py_script folders. We have pipeline to build `stats.tsv` for evaluate keras and sklearn models. After create the `stats.tsv` runs these [scripts](#analyze-evaluation) to analyze the performace of the models.

## Notebooks
We have jupyter notebooks, that are part of our pipeline. If you want know more about it go to [`notebooks`](https://github.com/binarySequoia/vg_recal/tree/master/notebooks#notebooks)


## py_scripts
We have python scripts that are part of our pipeline. Some of those script are the same as jupyter notebook but wrote as script to be able to run it as background job. If you want know more about it go to [`py_scripts`](https://github.com/binarySequoia/vg_recal/tree/master/py_scripts)

## scripts
We have shell scripts that are part of our pipeline. Here you can found scripts for data generation and data labeling using vg. Logistic regression using vowpal-wabbit were trained and testing using these scripts.  If you want know more about it go to [`scripts`](https://github.com/binarySequoia/vg_recal/tree/master/scripts)
