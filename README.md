smallgenes
==========

Simple eukaryotic genes in small genomic contexts.

## Background ##

Genes and genomes can vary in size from small to HUGE. Smaller genes are useful
for development, testing, and tutorials. This project seeks to create a set of
small genes primarily used in the "isoforms project".

A smallgene _locus_ has the following features:

- The DNA of the locus is represented in a single FASTA file
- The annotation is represented in a single GFF3 file
	- gene, mRNA, exon, UTRs, and spliced RNA-Seq are kept
	- all other features are removed
- There is only 1 gene in the region (no gene overlaps, not even ncRNAs)
- The gene is flanked by a little genomic sequence (e.g. 99 bp)
- The gene is protein-coding
- At least 1 transcript is spliced
- The gene has canonical features
	- Introns follow the GT-AG rule
	- CDS has normal start and stop codons
	- The intron and exon lengths are not unusually short
- The gene is not too long (e.g. <= 1000 bp)
- The gene is moderately to highly expressed (e.g. > 10,000 observed splices)
- The splicing landscape isn't too complex (e.g. < 10M possible isoforms)
- Some features are purged from the GFF
	- All features in the flanking region are removed
	- RNA-Seq introns with non-canonical splice sites are removed
	- RNA-Seq introns from the opposite strand are removed
- The gene is not too similar to other genes in the set
- The name of the locus follows `g.i.r` where
	- `g` is an abbreviation for the genome
	- `i` is the number of introns
	- `r` is the rank of splicing complexity compared to others in `i`


## Genomes ##

The initial build is the C. elegans genome. Other genomes will eventually
follow. The build procedure for each genome may be a little different. Details
for the C. elegans build are in `genomes/c.elegans`.
