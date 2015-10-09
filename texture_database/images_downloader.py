#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import hashlib
import requests
import datetime
import argparse

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}

def download(urls, image_folder):
    count = 0
    for idx, url in enumerate(urls):
        filename = url.split('/')[-1]
        extension = filename.split('.')[-1]
        print datetime.datetime.now(), 'downloading image {0:04d} of {1:04d} from {2}...'.format(idx, len(urls), url),
        sys.stdout.flush()
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                filename = os.path.join(image_folder, hashlib.md5(response.content).hexdigest()+'.'+extension)
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print 'succeeded.'
                count = count + 1
            else:
                print 'failed.'
                #print response.text
        except:
            print 'failed.'

    print count, 'images are successfully downloaded.'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download images for url.")
    parser.add_argument('-u', '--url', help='Image url.', required=True)
    parser.add_argument('-i', '--image_folder', help='Folder for saving images.', required=True)
    args = parser.parse_args()
    download([args.url], args.image_folder)
