# -*- coding: utf-8 -*-
"""
Created on Wed May  3 15:42:20 2023

@author: admin
"""

from django.conf import settings

import os
import uuid


def generate_filename(filename):
    CHATFILE_ROOT = settings.MEDIA_ROOT / 'filecontent'
    existing_filename = os.listdir( CHATFILE_ROOT )
    
    filename = filename.replace(" ", "+")
    while True:
        new_filename = f"{uuid.uuid4().hex}.{filename}"
        if not new_filename in existing_filename:
            break
    
    # print(f"\n  {new_filename=}\n")
    return new_filename
    
def save_file(filename, filebody):
    CHATFILE_ROOT = settings.MEDIA_ROOT / 'filecontent'
    
    with open( ( CHATFILE_ROOT / filename ), 'wb+' ) as fileIO:
        for chunk in filebody.chunks():
            fileIO.write(chunk)
    # Success signal
    return True