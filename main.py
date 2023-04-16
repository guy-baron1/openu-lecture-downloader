import os
import shutil
from requests import get
from tqdm import tqdm

# TODO: change according to desired video
num_batches = 5
md5 = 'ZEZ2EOPFMNKclM9_s2Vg9Q'
expires = 1681728962
output_file_name = 'infi2_lesson_4'

def setup():
    dirs = ['./batches', './output']
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def generate_batch_url(md5, expires, batch_num):
    return f'https://souvod.bynetcdn.com/vod/smil:vod/openu/PRV5/l9XuqVl4pa/App/l9XuqVl4pa_10.smil/media_b400000_{batch_num}.ts?md5={md5}&expires={expires}'

def download_batches():
    for batch in tqdm(range(num_batches)):
        response = get(generate_batch_url(md5, expires, batch))
        open(f'batches/{batch}.ts', 'wb').write(response.content)

def merge_batches():
    with open('batches/batches_list.txt', "w") as file:
        for batch_num in range(num_batches):
            file.write(f"file '{batch_num}.ts'\n")
    # concat all batches
    os.system('ffmpeg -f concat -i ./batches/batches_list.txt -c copy ./batches/all.ts')

    # convert ts to mp4
    os.system(f'ffmpeg -i ./batches/all.ts -acodec copy -vcodec copy ./output/{output_file_name}.mp4')

def cleanup():
    shutil.rmtree('./batches')	

def main():
    setup()
    download_batches()
    merge_batches()
    cleanup()

main()
