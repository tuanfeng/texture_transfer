#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import argparse
import images_downloader

def parse(html_file, image_folder):
    with open(html_file, 'r') as f:
        html_content = f.read()
    pattern = r'imgurl=(http://.*?)&amp;'
    urls = re.findall(pattern, html_content)
    images_downloader.download(urls, image_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse Google image search results.")
    parser.add_argument('-f', '--html_file', help='Input html filename.', required=True)
    parser.add_argument('-i', '--image_folder', help='Folder for saving images.', required=True)
    args = parser.parse_args()
    parse(args.html_file, args.image_folder)
