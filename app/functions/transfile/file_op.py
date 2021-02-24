#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import os
# 读取文件
def readfile(filetype, filename):
    content = ''
    if filetype == 'json': 
        with open(r'./functions/showdata/json/{}.json'.format(filename), 'r', encoding='utf-8') as f:
            content = json.load(f)
    elif filetype == 'sql':
        if os.path.exists(r'./functions/showdata/sqls/{}.sql'.format(filename)):
            with open(r'./functions/showdata/sqls/{}.sql'.format(filename), 'r', encoding='utf-8') as f:
                content = f.read()
    elif filetype == 'normal':
        if os.path.exists(r'./functions/showdata/normal/{}.txt'.format(filename)):
            with open(r'./functions/showdata/normal/{}.txt'.format(filename), 'r', encoding='utf-8') as f:
                content = f.read()
    elif filetype == 'normal_json':
        if os.path.exists(r'./functions/showdata/normal/{}.txt'.format(filename)):
            with open(r'./functions/showdata/normal/{}.txt'.format(filename), 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content='{"title":"","dataid":""}'
    else:
        pass
    return content

# 写入文件，
def writefile(filetype, filename, content):
    if filetype == 'json':
        with open(r'./functions/showdata/json/{}.json'.format(filename), 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False,indent=1)
    elif filetype == 'sql':
        with open(r'./functions/showdata/sqls/{}.sql'.format(filename), 'w', encoding='utf-8') as f:
            f.write(content)
    elif filetype == 'normal':
        with open(r'./functions/showdata/normal/{}.txt'.format(filename), 'w', encoding='utf-8') as f:
            f.write(content)
    elif filetype == 'normal_json':
        with open(r'./functions/showdata/normal/{}.txt'.format(filename), 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False,indent=1)
    else:
        pass