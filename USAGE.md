# USAGE
Instruction to runs this experiments.
More info about how works [click here](https://github.com/binarySequoia/vg_recal#characterizing-mapping-quality-recalibration-approaches-in-a-variant-graph-genomics-tool).
### Dependecies
* [vg](https://github.com/vgteam/vg)
* Jupyter Notebook
* SciPy
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

### Building a vg graph
<pre><code>vg construct -r <i>[fasta file]</i> -v <i>[vcf file]</i> > vg_graph.vg</code></pre>
We are using vg graphs in xg/gcsa index pair format. To create this format run the following line.
```bash
# store the graph in the xg/gcsa index pair
vg index -x vg_graph.xg -g vg_graph.gcsa -k 16 vg_graph.vg
```

If you want to know more about vg functionalities, please go to [vg](https://github.com/vgteam/vg). 

***NOTE:  The data folder already contains the xg and gcsa files to work.***

### Reads Simulation
#### Training and testing data generation

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

#### Label training and testing data
After run _vg sim_ we have simulated reads that are similar to some region in the genome graph but not the same. Now for label the read we are will try map those reads back to the same place in the graph. If a read is map in the same place we label that read as correct, if not we label that read as incorrect.

Now, for do that we need to use _vg map_ and _vg annotate_.

<pre><code>vg map -x <i>[xg file]</i> -g <i>[gcsa file]</i> -G simulated.gam | vg annotate -x <i>[xg file]</i>  -a - -p > mapped.gam</code></pre>


To label our training amd testing reads we run:
```bash
# Generate Training data
vg map -x data/genome_data/snp1kg-CHR21.xg -g data/genome_data/snp1kg-CHR21.gcsa 
     -G train_sim_len100.gam | vg annotate -x -x data/genome_data/snp1kg-CHR21.xg  -a - -p > train_mapped_len100.gam
# Genearte Testing data
vg map -x data/genome_data/snp1kg-CHR21.xg -g data/genome_data/snp1kg-CHR21.gcsa 
     -G test_sim_len100.gam | vg annotate -x -x data/genome_data/snp1kg-CHR21.xg  -a - -p > test_mapped_len100.gam
```

