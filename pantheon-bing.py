import sys
if sys.version_info[0] < 3:
    raise BaseException('Please run under python3 environment.')

import os, requests, json
from datetime import date

current_dir = os.path.dirname(os.path.realpath(__file__))
base_url = 'http://www.bing.com'
hpimagearchive_url = '/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=ar'

def get_image_link():
    GET_DATA = requests.get(base_url + hpimagearchive_url)
    json_obj = json.loads(GET_DATA.content.decode('utf-8'))
    return json_obj['images'][0]['url']

def download_image_copyright():
    GET_DATA = requests.get(base_url + hpimagearchive_url)
    json_obj = json.loads(GET_DATA.content.decode('utf-8'))
    img_copyright = json_obj['images'][0]['copyright']
    file_name = date.today().strftime('%Y%m%d') + ".txt"
    data_file = open(os.path.join(current_dir, 'img', file_name), 'wb')
    data_file.write(img_copyright.encode('utf-8'))
    data_file.close()
    return img_copyright

def download_image(img_link):
    if img_link is not None:
        img = requests.get(img_link)
        file_name = date.today().strftime('%Y%m%d') + ".jpg"
        img_file = open(os.path.join(current_dir, 'img', file_name), 'wb')
        img_file.write(img.content)
        img_file.close()
        return img_file.name
    return None

def set_wallpaper():
    name = download_image(base_url + get_image_link())
    download_image_copyright()
    path = os.path.join(current_dir, 'img', name)
    cmd_set_last_image = '/usr/lib/x86_64-linux-gnu/io.elementary.contract.set-wallpaper {0}'.format(path)
    os.system(cmd_set_last_image)

set_wallpaper()
