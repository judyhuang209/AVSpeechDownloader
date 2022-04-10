import sys
import os
from multiprocessing.pool import ThreadPool

from yt_dlp import YoutubeDL
import ffmpeg


class VidInfo:
    def __init__(self, yt_id, start_time, end_time, outdir):
        self.yt_id = yt_id
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.out_filename = os.path.join(outdir, yt_id + '_' + start_time + '_' + end_time + '.mp4')


def download(vidinfo):

    yt_base_url = 'https://www.youtube.com/watch?v='

    yt_url = yt_base_url+vidinfo.yt_id

    duration = str(int(vidinfo.end_time) - int(vidinfo.start_time))

    ydl_opts = {
        'format': '22/18',
        'quiet': True,
        'ignoreerrors': True,
        'no_warnings': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            download_url = ydl.extract_info(url=yt_url, download=False)['url']
    except:
        return_msg = '{}, ERROR (youtube)!'.format(vidinfo.yt_id)
        return return_msg
    try:
        (
            ffmpeg
                .input(download_url, ss=vidinfo.start_time, t=duration)
                .output(vidinfo.out_filename, format='mp4', r=25, vcodec='libx264',
                        crf=18, preset='veryfast', pix_fmt='yuv420p', acodec='aac', audio_bitrate=128000,
                        strict='experimental')
                .global_args('-y')
                .global_args('-loglevel', 'error')
                .run()

        )
    except:
        return_msg = '{}, ERROR (ffmpeg)!'.format(vidinfo.yt_id)
        return return_msg
    
    return '{}, DONE!'.format(vidinfo.yt_id)


if __name__ == '__main__':

    split = sys.argv[1]
    csv_file = 'avspeech_{}.csv'.format(split)
    out_dir = split

    os.makedirs(out_dir, exist_ok=True)

    with open(csv_file, 'r') as f:
        lines = f.readlines()
        lines = [x.split(',') for x in lines]
        vidinfos = [VidInfo(x[0], x[1], x[2], out_dir) for x in lines]
    # train 46669
    # test 1669
    vid_num = 1669
    sub_vidinfos = vidinfos[:vid_num]
    print('subvidinfo len', len(sub_vidinfos))
    bad_files = open('bad_files_{}.txt'.format(split), 'w')
    file_list = open('{}.txt'.format(split), 'w')
    results = ThreadPool(5).imap_unordered(download, sub_vidinfos)
    cnt = 0
    for r in results:
        cnt += 1
        print(cnt, '/', len(sub_vidinfos), r)
        if 'ERROR' in r:
            bad_files.write(r + '\n')
        else:
            file_list.write(r[:-7] + '\n')
    bad_files.close()
    file_list.close()
