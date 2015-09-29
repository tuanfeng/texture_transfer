#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import argparse
from apiclient.discovery import build

def crawl(developer_key, cx, query, start, number):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(BASE_DIR, 'database')
    json_dir = os.path.join(database_dir, 'json')

    service = build("customsearch", "v1", developerKey=developer_key)
    batch_size = 10
    batch_num = (number+batch_size-1)/batch_size
    for batch_idx in range(batch_num):
        start_idx = start+batch_idx*batch_size
        end_idx = start_idx+batch_size-1
        print 'Crawling for images in range [%d, %d] with keywords \"%s\"...'%(start_idx, end_idx, query)
        response = service.cse().list(q=query, cx=cx, searchType='image', num=batch_size, start=start_idx).execute()
        if not 'items' in response:
            print 'No result!!\nThe response is: {}'.format(res)
        else:
            filename = query.replace(' ', '_')+'_{0:05d}_{1:05d}.json'.format(start_idx, end_idx)
            fullpath = os.path.join(json_dir, filename)
            print 'Saving results to %s...'%(fullpath)
            with open(fullpath, 'w') as json_file:
                json.dump(response, json_file)
        time.sleep(0.2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crawl images from Google image search.")
    parser.add_argument('--developer_key', help='Google developer key.', required=True)
    parser.add_argument('--cx', help='Custom search engine ID.', required=True)
    parser.add_argument('--query', help='Query keywords.', required=True)
    parser.add_argument('--start', help='Start index.', type=int, required=True)
    parser.add_argument('--number', help='Image number to be retrieved.', type=int, required=True)
    args = parser.parse_args()
    crawl(args.developer_key, args.cx, args.query, args.start, args.number)
