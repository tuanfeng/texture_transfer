#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import bing_image_parser
import google_image_parser

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

html_folder = os.path.join(BASE_FOLDER, 'htmls')
categories = os.listdir(html_folder)
for category in categories:
    images_folder = os.path.join(BASE_FOLDER, 'images', category)
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    
    print 'Downloading %s from Bing searches...'%(category)
    bing_html_folder = os.path.join(html_folder, category, 'bing')
    bing_html_files = os.listdir(bing_html_folder)
    for bing_html_filename in bing_html_files:
        filename = os.path.join(bing_html_folder,bing_html_filename)
        bing_image_parser.parse(filename, images_folder)
     
    print 'Downloading %s from Google searches...'%(category)
    google_html_folder = os.path.join(html_folder, category, 'google')
    google_html_files = os.listdir(google_html_folder)
    for google_html_filename in google_html_files:
        filename = os.path.join(google_html_folder, google_html_filename)
        google_image_parser.parse(filename, images_folder)
