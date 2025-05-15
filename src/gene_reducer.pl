use strict;
use warnings;

my @genes;
open(my $fh, "initial.genes.txt") or die;
my %len;
while (<$fh>) {
	next if /^#/;
	chomp;
	my ($ch, $len, $introns, $rna, $iso) = split;
	$len{$ch} = $len;
	push @genes, {base => $ch, len => $len, introns => $introns, rna => $rna, iso => $iso};
}

if (not -s "build/apc.fa") {
	foreach my $gene (@genes) {
		`cat build/genes/$gene->{base}.fa >> build/apc.fa`;
	}
	`makeblastdb -in build/apc.fa -dbtype nucl`;
	`blastn -db build/apc.fa -query build/apc.fa -evalue 1e-20 -outfmt 6 > build/apc.blast`;
}

my %kill;
my %seen;
open(my $bfh, "build/apc.blast") or die;
while (<$bfh>) {
	my ($q, $s, $pct, $score) = split;
	next if $q eq $s;
	next if $kill{$q};
	my $spct = $score / $len{$q};
	if ($pct > 95 and $spct > 0.95) {
		$kill{$s} = 1;
	}
}

my %out;
foreach my $gene (sort {$a->{introns} <=> $b->{introns} or $a->{iso} <=> $b->{iso} or $a->{base} cmp $b->{base}} @genes) {
	next if exists $kill{$gene->{base}};
	my $in = $gene->{introns};
	my $is = $gene->{iso};
	push @{$out{$in}{$is}}, $gene->{base};
}

`mkdir -p smallgenes`;
foreach my $in (sort {$a <=> $b} keys %out) {
	my $n = 0;
	foreach my $is (sort {$a <=> $b} keys %{$out{$in}}) {
		foreach my $base (@{$out{$in}{$is}}) {
			my $ctxname = "ch.$in\_$n";
			swap_names("build/genes/$base.fa",
				"smallgenes/$ctxname.fa", $ctxname, $base);
			swap_names("build/genes/$base.gff3",
				"smallgenes/$ctxname.gff3", $ctxname, $base);
			$n++;
		}
	}
	
}

sub swap_names {
	my ($infile, $outfile, $newstr, $oldstr) = @_;
	open(my $ifh, $infile) or die;
	open(my $ofh, ">$outfile") or die;
	while (<$ifh>) {
		s/$oldstr/$newstr/g;
		print $ofh $_;
	}
}