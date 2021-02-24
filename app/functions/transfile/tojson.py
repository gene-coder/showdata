#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

# 返回列表
def sql_to_list(data,table_title):
    if len(data[0]) == len(table_title):
        jsonData = []
        for row in data:
            result = {}
            for i in range(0,len(table_title)):
                result[table_title[i]] = row[i]
            else:
                jsonData.append(result)
        return jsonData
    else:
        print('表格列与数据列不一致')
        return '表格列与数据列不一致'