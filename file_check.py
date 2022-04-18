import sys

def main(txtfile):
	file_list = '{}.txt'.format(txtfile)
	with open(file_list, 'r') as f:
		lines = f.readlines()
	new_lines = list(set(lines))
	new_file_list = 'new_{}.txt'.format(txtfile)
	with open(new_file_list, 'w') as nf:
		for file_name in new_lines:
			nf.write(file_name)

if __name__ == '__main__':
	txtfile = sys.argv[1]
	main(txtfile)