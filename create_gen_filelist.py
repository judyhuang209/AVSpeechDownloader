import sys, os, cv2
from tqdm import tqdm
# def move(source_dir, target_dir):

def with_opencv(filename):
    import cv2
    video = cv2.VideoCapture(filename)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count/fps
    return duration, frame_count

def make_pairs(file_list):
    pair_list = []
    for idx, filename in enumerate(file_list):
        for i in range (1, 11):
            idx_pair = (idx + i) % len(file_list)
            pair_str = filename[:-4] + ' ' + file_list[idx_pair]
            # print(pair_str)
            pair_list.append(pair_str)
    return pair_list

def main(data_root):
    file_list = []
    frame_count = 0
    duration = 0
    for filename in tqdm(os.listdir(data_root)):
        # print(filename)
        if os.path.isfile(os.path.join(data_root, filename)):
            file_list.append(filename[:-4])
            dur, fc = with_opencv(os.path.join(data_root, filename))
            # print(dur, fc)
            duration += dur*10
            frame_count += fc*10
        else:
            continue
    pair_list = make_pairs(file_list)
    print('Counts of pair_list: {}'.format(len(pair_list)))

    txt = '{}_list.txt'.format(data_root)
    with open(txt, 'w') as f:
        for line in tqdm(pair_list):
            f.write(line + "\n")         
    print('Duration of all: {} secs'.format(duration))
    print('Frame count of all: {}'.format(frame_count))
    print('Average duration: {} secs'.format(duration/10/len(os.listdir(data_root))))
    print('Average frame count: {}'.format(frame_count/10/len(os.listdir(data_root))))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No argument.')
        print('Trying: processing files in default root test_files')
        data_root = 'test_files'
    else:
        data_root = sys.argv[1]
    print('Processing files from {}'.format(data_root))
    main(data_root)