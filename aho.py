import sys
import ahocorasick
from Bio import SeqIO


def read_subgraph_as_automaton(path, k):
	automaton = ahocorasick.Automaton()
	with open(path, 'r') as f:
		for node in f:
			node = node.split()[0]
			for i in range(len(node) - k + 1):
				automaton.add_word(node[i : i + k], node[i : i + k])
	automaton.make_automaton()
	return automaton


def print_reads(read, seq, quality):
	return "{}\n{}\n+\n{}\n".format(read, seq, quality)


def write_reads(path_in_1, path_in_2, path_out_1, path__out_2, automaton, k):
	with open(path_in_1, "r") as in_1, \
		 open(path_in_2, "r") as in_2, \
		 open(path_out_1, "w") as out_1, \
		 open(path__out_2, "w") as out_2:

		for read in in_1:
			read = read[:-1]
			seq = in_1.next()[:-1] #sequence
			in_1.next()	# +...
			quality = in_1.next()[:-1]

			read_p = in_2.next()[:-1]
			seq_p = in_2.next()[:-1]
			in_2.next()
			quality_p = in_2.next()[:-1]
			is_written = 0
			for it in automaton.iter(seq):
				out_1.write(print_reads(read, seq, quality))
				out_2.write(print_reads(read_p, seq_p, quality_p))
				is_written = 1
				break
			if is_written == 0:
				for it in automaton.iter(seq_p):
					out_1.write(print_reads(read,seq, quality))
					out_2.write(print_reads(read_p, seq_p, quality_p))
					is_written = 1
					break


def main():
	k = int(sys.argv[1])
	automaton = read_subgraph_as_automaton("m1/graph.txt", k)
	print("start writting")
	write_reads("1.fastq", "2.fastq", "reads_aa_cut1.fastq", "reads_aa_cut2.fastq", automaton, k)
	

if __name__ == "__main__":
	main()
