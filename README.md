smallgenes
==========

Small eukaryotic genes in small genomic contexts.

## Background ##

Genes and genomes can vary in size from small to HUGE. Smaller genes are useful
for development, testing, and tutorials. This project seeks to create a set of
small genes for a variety of common genomes.

A smallgene _locus_ has the following features:

- The DNA is represented in a FASTA file
- The annotation is represented in a GFF3 file
- There is 1 protein-coding gene whose length is short (e.g < 1000 bp)
- The gene is flanked by a little genomic sequence (e.g. 99 bp)
- The gene is moderately to highly expressed
- All introns follow the GT-AG rule
- Intron and exon lengths are not unusually short or long
- The gene is not too similar to other genes in the set

## Genomes ##

Initial smallgene sets are built for the following genomes.

- A. thaliana
- C. elegans
- D. melanogaster

## Build Procedure ##

The build procedure for each genome requires some customization due to
differences in the way each community represents its GFF.

Some software is required:

- git clone KorfLab/grimoire
	- add `grimoire/grimoire` to your PYTHONPATH
	- add `grimoire/haman` to your PATH
- git clone KorfLab/isoforms
	-add `isoforms` to your PYTHONPATH
- install `blastn` (e.g. via mini-conda)


## C. elegans ##

In the lines below, `$DATA` is wherever you keep your data.

```bash
mkdir build
cd build
ln -s $DATA/c_elegans.PRJNA13758.WS282.genomic.fa.gz genome.gz
ln -s $DATA/c_elegans.PRJNA13758.WS282.annotations.gff3.gz gff3.gz
gunzip -c gff3.gz | grep -E "WormBase|RNASeq" > ws282.gff3
cd ..
haman build/genome.gz build/ws282.gff3 pcg genes --issuesok --plus
python3 gene_selector.py build/genes
```

This results in 2 new file: `initial.genes.txt` and `initial.log.json`

Some of the genes are duplicates or near duplicates. The next step trims the
set to be more unique.

```bash
perl gene_reducer.pl
```

This results in the `smallgenes` directory, which has 1045 genes. The final
step is to rename the directory to the genome and create a tar-ball.

```bash
mv smallgenes c.elegans.smallgenes
tar -czf c.elegans.smallgenes.tar.gz c.elegans.smallgenes
```
