# Characterizing Mapping Quality Recalibration Approaches in a Variant Graph Genomics Tool
This is experiemt to measuare performance in vg recalibrate, testing different models. To know how re-run this code [click here](https://github.com/binarySequoia/VG_Recal/blob/master/USAGE.md).

## Motivation
Identifying DNA patterns can tell us useful information about any living being. Closely related organisms have similar DNA, while distantly related organisms have few similarities. Humans have extremely similar genomes; studying differences can help to identify particular variants that can cause illness. Vg is a variant graph-based alignment tool for DNA mapping using graph genome references; these graphs capture variation information from populations, which allows more accurate genome studies.

## [vg](https://github.com/vgteam/vg#vg)

Vg is a set of tools for working with genome variation graphs. These graphs consist of a set of nodes and edges, where each node represents a DNA sequence; edges, connections between two nodes, can be seen as  concatenations of two sequences. We built VG graphs with genome references and their sequence variations. Because of the variation we have multiple paths through the graph, this means from a particular sequence you could have multiple edges to take.

![alt text](https://github.com/binarySequoia/VG_Recal/raw/master/doc/VG_GRAPH.png "VG GRAPH")

An essential part of vg is mapping DNA reads into the graph; that means searching for the position where the sequence is most similar to the reference graph. Mapping is challenging because genomes can be very repetitive, and in each repetition, sequences can vary. In addition to mapping, vg calculates a mapping quality score; this score is the probability of the mapping being wrong.

_Graph image was created using [Sequence TubeMap Tool](https://github.com/vgteam/sequenceTubeMap)_

## Approach
In this work, we create and benchmark models to predict the probabilities of mappings being wrong and compare our recalibration models against each other and against the original mapping quality scores. To build our dataset, we simulate sequences with errors from the reference graph and map these new sequences back into the graph, then label those mappings as correct or incorrect. We train our models to calculate when a mapping is wrong, then extract the probabilities from those predictions. Using these probabilities, we calculate mapping quality scores and compare them against the original scores calculated by vg using the Brier score.
![alt text](https://github.com/binarySequoia/VG_Recal/raw/master/doc/VG_RECALIBRATE_WORKFLOW.png "APPROACH WORKFLOW")

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


## Discussion
We test 5 different models with logistic regression using mapping quality information, mems, sequences, mems stats and a combination between mems and sequences. Our experiments show that logistic regression with mems improves by 5.23% the original mapping score given by vg in reads of length 100 base pairs but is not able to generalize well across lengths. But the Q-Q plot shows that the mems model has over confidence about its predictions.

## References
* Garrison, Erik, et al. "Sequence variation aware genome references and read mapping with the variation graph toolkit." bioRxiv (2017): 234856.
