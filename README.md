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
differences in the way each community represents its GFF. Details are described
in the READMEs in each of the `genome` directories.

The generic requirements are as follows:

