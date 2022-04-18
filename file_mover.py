import sys
import os
from pathlib import Path
import shutil
from tqdm import tqdm

# def move(source_dir, target_dir):

def main(split):
	file_list = '{}.txt'.format(split)
	with open(file_list, 'r') as f:
		lines = f.readlines()
	lines = lines[:len(lines)//4]
    
	flie_split = open('sub{}.txt'.format(split), 'w')
	out_dir = 'sub' + split
	os.makedirs(out_dir, exist_ok=True)
	count = 0

	for file_name in tqdm(lines):
		if lines.count(file_name) > 1:
			# print('duplicate file ', file_name)
		# print('file_name', file_name)
		# print('file_name[:-1]', file_name[:-1])
		for real_filename in os.listdir(split):
			if file_name[:-1] in real_filename:
				original = split + "/" + real_filename
				target = out_dir + "/" + real_filename
				# copy_to_mydir = partial(shutil.copyfile, dst=target)
				# print('From: {}\nTo: {}'.format(original,target))
				shutil.copyfile(original, target)
				count += 1
				flie_split.write(real_filename[:-4] + "\n")
				
	print('count', count)

	flie_split.close()

if __name__ == '__main__':
	split = sys.argv[1]
	main(split)