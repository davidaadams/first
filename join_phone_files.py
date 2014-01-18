import csv
import sys

def JoinFiles(input1, input2, output):
	print("Joining...")
	print(input1)
	print(input2)
	lines1 = set(open(input1, "r").readlines())
	lines2 = set(open(input2, "r").readlines())
	all_lines = list(lines1 | lines2)
	all_lines.sort()
	output = open(output, 'wb')
	for l in all_lines:
		output.write(l)
	output.close()


if __name__ == "__main__":
	argv = sys.argv
	if len(argv) < 4:
		print("pass three args: the two input file names and output file names")
		sys.exit(1)
	JoinFiles(argv[1], argv[2], argv[3])
