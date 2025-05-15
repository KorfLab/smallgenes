import argparse
import glob
import json
import os
import re
import subprocess
import sys

from grimoire.genome import Reader
from isoform import Locus

#######
# CLI #
#######

parser = argparse.ArgumentParser(
	description='initial gene selector for smallgenes')
parser.add_argument('genes', type=str, metavar='<genes dir>',
	help='path to gene build directory')
parser.add_argument('--seqlen', type=int, metavar='<int>', default=1200,
	required=False, help='maximum sequence length [%(default)i]')
parser.add_argument('--rnaseq', type=int, metavar='<int>', default=10000,
	required=False, help='minimum RNAseq value [%(default)i]')
parser.add_argument('--ilen', type=int, metavar='<int>', default=35,
	required=False, help='minimum intron length [%(default)i]')
parser.add_argument('--elen', type=int, metavar='<int>', default=25,
	required=False, help='minimum exon length [%(default)i]')
parser.add_argument('--flank', type=int, metavar='<int>', default=99,
	required=False, help='genomic flank length [%(default)i]')
parser.add_argument('--isoforms', type=float, metavar='<float>', default=10,
	required=False, help='maximum number of isoforms in millions[%(default).1f]')
parser.add_argument('--debug', action='store_true')
arg = parser.parse_args()
arg.isoforms *= 1000000

################
# Output Files # they are named :(
################

gfh = open("initial.genes.txt", "w")
lfh = open("initial.log.json", "w")

########
# Main #
########

print('# id\tlength\tintrons\tRNAseq\tisoforms', file=gfh, flush=True)

log = {
	'total_gene_regions': 0,
	'region_too_long': 0,
	'multiple_genes': 0,
	'no_introns': 0,
	'poorly_expressed': 0,
	'non_canonical': 0,
	'too_many_isoforms': 0,
	'kept_genes': 0,
}

for ff in glob.glob(f'{arg.genes}/*.fa'):
	gf = ff[:-2] + 'gff3'

	genome = Reader(gff=gf, fasta=ff)
	chrom = next(genome) # there is only one in a pcg build
	log['total_gene_regions'] += 1
	
	# debug
	if arg.debug and log['kept_genes'] >= 20: break

	##########
	# filter 1: not too long
	##########
	if len(chrom.seq) > arg.seqlen:
		log['region_too_long'] += 1
		print('L', end='', file=sys.stderr, flush=True)
		continue

	##########
	# filter 2: isolated protein-coding genes
	##########
	genes = len([None for f in chrom.ftable.features if f.type == 'gene'])
	if genes > 1:
		log['multiple_genes'] += 1
		print('M', end='', file=sys.stderr, flush=True)
		continue

	gene = chrom.ftable.build_genes()[0] # the one true gene

	##########
	# filter 3: has introns
	##########
	max_introns = 0
	for tx in gene.transcripts():
		if len(tx.introns) > max_introns: max_introns = len(tx.introns)
	if max_introns == 0:
		log['no_introns'] += 1
		print('0', end='', file=sys.stderr, flush=True)
		continue

	##########
	# filter 4: plentiful splicing data matching the introns
	##########
	introns = {}
	for tx in gene.transcripts():
		for intron in tx.introns:
			sig = (intron.beg, intron.end)
			if sig not in introns: introns[sig] = True

	maxexp = 0
	for f in chrom.ftable.features:
		sig = (f.beg, f.end)
		if f.source == 'RNASeq_splice' and sig in introns and f.score > maxexp:
			maxexp = int(f.score)
	if maxexp < arg.rnaseq:
		log['poorly_expressed'] += 1
		print('P', end='', file=sys.stderr, flush=True)
		continue

	##########
	# filter 5: not weird (see grimoire defaults for gene build)
	##########
	weird = False
	for tx in gene.transcripts():
		if tx.issues:
			weird = True
			break
	if weird:
		log['non_canonical'] += 1
		print('W', end='', file=sys.stderr, flush=True)
		continue

	##########
	# filter 6: not too many isoforms
	##########
	loc = Locus(chrom.name, chrom.seq, arg.ilen, arg.elen, arg.flank,
		(None, None, None, None, None, None),
		(None, None, None, None, None, None),
		0, limit=int(arg.isoforms), countonly=True)
	isos = loc.isocount
	if isos >= arg.isoforms:
		log['too_many_isoforms'] += 1
		print('N', end='', file=sys.stderr, flush=True)
		continue
	
	##########
	# made it!
	##########
	log['kept_genes'] += 1
	print('K', end='', file=sys.stderr, flush=True)
	print('\t'.join((chrom.name, str(len(chrom.seq)), str(max_introns),
		str(maxexp), str(isos))), file=gfh, flush=True)
	
print(file=sys.stderr, flush=True)
print(json.dumps(log, indent=4), file=lfh)
