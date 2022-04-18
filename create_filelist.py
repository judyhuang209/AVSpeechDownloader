import sys
import os
from tqdm import tqdm
# def move(source_dir, target_dir):

def main(split):
    file_list = '{}.txt'.format(split)
    with open(file_list, 'w') as f:
        for real_filename in tqdm(os.listdir(split)):
            f.write(real_filename + "\n")

if __name__ == '__main__':
    split = sys.argv[1]
    main(split)