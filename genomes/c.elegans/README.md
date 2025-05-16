C. elegans smallgenes
=====================

Stuff you need:

- grimoire in your PYTHONPATH
- isoform2 in your PYTHONPATH
- blast executables in your PATH (`conda install blast`)

In the lines below, `$DATA` is wherever you keep your data.

```
mkdir build
cd build
ln -s $DATA/c_elegans.PRJNA13758.WS282.genomic.fa.gz genome.gz
ln -s $DATA/c_elegans.PRJNA13758.WS282.annotations.gff3.gz gff3.gz
gunzip -c gff3.gz | grep -E "WormBase|RNASeq" > ws282.gff3
../gene-selector genome.gz ws282.gff3 initial ../worm.splicemodel --verbose
```

This results in a directory `build/initial` that contains the initial
smallgenes set. There may be some very close paralogs. To remove
near-duplicates.

```
../gene-reducer build/initial build/scratch build/smallgenes
tar -czf smallgenes.tar.gz build/smallgenes
```
