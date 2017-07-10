from popen import Sh
import aho
import sys
from Bio import SeqIO
import ahocorasick
import subprocess
import os


def run_metacherchant(parametrs):
	str_run_metacherchant = './../metacherchant.sh '
	for arg in parametrs:
		str_run_metacherchant += arg + ' ' + parametrs[arg]
	#print(str_run_metacherchant)
	print(Sh(str_run_metacherchant))

def run_spades(reads_1, reads_2):
	str_run_spades = 'python ../../../../7/SPAdes-3.10.1-Linux/bin/spades.py --pe1-1 '
	str_run_spades += reads_1 + ' --pe1-2 '+ reads_2 +' -o out_spades'
	print(str_run_spades)
	print(Sh(str_run_spades))

def run_megahit(reads_1, reads_2):
	str_run_megahit = './../../../../megahit/megahit/megahit -1 '
	str_run_megahit += reads_1 + ' -2 ' + reads_2 + ' -o out_megahit'
	print(str_run_megahit)
	print(Sh(str_run_megahit))	

def run_aho(parametrs):
	path_subgraph = parametrs_1["--output"][:-1] + "/graph.txt"
	reads_in = parametrs['--reads'].split()
	print( path_subgraph, int(parametrs_1["--k"]))
	#print(reads_in[0], reads_in[1], "reads_cut_1.fastq", "reads_cut_2.fastq", aho, int(parametrs_1["--k"]))
	aut = aho.read_subgraph_as_automaton(path_subgraph, int(parametrs_1["--k"]))
	aho.write_reads(reads_in[0], reads_in[1], "preresult/reads_cut_1.fastq", "preresult/reads_cut_2.fastq", aut, int(parametrs_1["--k"]))


len_argv = len(sys.argv)
argv = sys.argv[1:len_argv]
len_argv -= 1
parametrs_1 = {}
parametrs_2 = {}
for i in range(0, len_argv - 1):
	if argv[i][0] == '-':
		parametrs_1[argv[i]] = ''
		parametrs_2[argv[i]] = ''
		for j in range(i+1, len_argv):
			if argv[j][0] != '-':
				parametrs_1[argv[i]] += argv[j] + ' '
				parametrs_2[argv[i]] += argv[j] + ' '
			else:
				break
#print(str(parametrs))
parametrs_1['--maxkmers'] *= 2
parametrs_1['--k'] = str(21) + ' '
parametrs_1['--coverage'] = str(0) + ' '
parametrs_1['--output'] = "preresult "
print("start running:")
run_metacherchant(parametrs_1)
run_aho(parametrs_1)
#run_spades("preresult/reads_cut_1.fastq", "preresult/reads_cut_2.fastq")
run_megahit("preresult/reads_cut_1.fastq", "preresult/reads_cut_2.fastq")
parametrs_2["--reads"] = 'out_megahit/final.contigs.fasta '
run_metacherchant(parametrs_2)
