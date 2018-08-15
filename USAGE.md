# USAGE
Instruction to runs this experiments.

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
