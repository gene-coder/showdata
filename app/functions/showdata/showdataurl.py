#!/usr/bin/env python
# -*- coding: utf-8 -*-


from functions.connectmysql import connectdb
from flask import Flask, render_template, Blueprint,redirect
from flask import request
from flask import url_for
from flask import redirect
from xpinyin import Pinyin
import time
import datetime
from functions.transfile import file_op
from functions.transfile import tojson

showdata = Blueprint('showdata', __name__)

# 分页
def get_data(data):
    limit = int(request.args.get("limit"))
    page = int(request.args.get("page"))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    ret = data[start:end]
    return {"code": 0, "msg": "", "count": len(data), "data": ret, }


# 过滤,筛选的时候用
def select_date(data,condition):
    key=str(condition[0])[4:-1]
    value=condition[1].strip()
    for i in list(reversed(data)):
        # 筛选相同
        # if i[key] != value and len(str(value))>0 :
        # 筛选相似
        if str(value) not in str(i[key]) :
            data.remove(i) 
        else:
            pass

            
# 获取分页数据
def get_date_search(data):
    # print(dict(request.args).items())
    select_dict=dict(request.args).items()
    key_list=list(select_dict)[2:]
    # print(key_list)
    for i in key_list:
        value=i[1].strip()
        if len(str(value))>0:
            select_date(data,i)
        else:
            pass

    # 原有
    limit = int(request.args.get("limit"))
    page = int(request.args.get("page"))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    ret = data[start:end]
    return {"code": 0, "msg": "", "count": len(data), "data": ret, }

def get_date_search_limit(data):
    key = request.args.get("key[*]")
    # print('111',key)
    limit = int(request.args.get("limit"))
    page = int(request.args.get("page"))
    start = (page - 1) * limit
    end = page * limit if len(data) > page * limit else len(data)
    ret = data[start:end]
    return {"code": 0, "msg": "", "count": len(data), "data": ret, }


# 根据url 查找type，page
def find_url(dict, url):
    for dict_type, page in dict.items():
        for page_name, page_conf in page.items():
            if page_conf['url'] == url:
                return dict_type, page_name


@ showdata.route('/')
def showdate1():
    # print('aaaaaa',request.remote_addr)
    return render_template("/showdata/show_data.html", dict_nav=file_op.readfile('json', 'dict_nav'))

# 配置数据库-主页
@showdata.route('/add_database')
def add_database():
    return render_template("/showdata/add_database.html", title='_配置数据库', dict_nav=file_op.readfile('json', 'dict_databases'))

# 配置数据库-新增数据库
@ showdata.route('/add_database/save', methods=['POST', 'GET'])
def add_database_sava():
    if request.method == 'POST':
        databases_read = file_op.readfile('json', 'dict_databases')
        database_dic = {}
        get_dataid = request.form['dataid']
        database_dic['get_dataid'] = request.form['dataid']
        database_dic['get_datatype'] = request.form['datatype']
        database_dic['get_dataip'] = request.form['dataip']
        database_dic['get_dataport'] = request.form['dataport']
        database_dic['get_database'] = request.form['database']
        database_dic['get_datausr'] = request.form['datausr']
        database_dic['get_datapwd'] = request.form['datapwd']
        database_dic['get_datadesc'] = request.form['datadesc']
        # print(database_dic)
        if get_dataid in databases_read.keys():
            databases_read[get_dataid] = database_dic
        else:
            databases_read[get_dataid] = {}
            databases_read[get_dataid] = database_dic
        file_op.writefile('json', 'dict_databases', databases_read)
    return redirect(url_for('showdata.add_database'))
    # return render_template('/showdata/add_database.html', dict_nav=file_op.readfile('json', 'dict_databases'))

# 配置数据库-删除数据库
@ showdata.route('/add_database/del/<databaseid>')
def del_database(databaseid):
    dict_database=file_op.readfile('json', 'dict_databases')
    del dict_database[databaseid]
    # print(dict_database)
    file_op.writefile('json', 'dict_databases', dict_database)
    return databaseid + '删除成功'

# 配置数据库-测试数据库
@ showdata.route('/add_database/btn_test/<databaseid>')
def database_conntest(databaseid):
    database = file_op.readfile('json','dict_databases')[databaseid]
    try:
        if database['get_datatype']=='MYSQL':
            data_mysql = connectdb.run_mysql(database, "select 'OK'")
        elif database['get_datatype']=='ORACLE':
            data_mysql = connectdb.run_mysql(database, "select 'OK' from dual")
        else:
            pass
    except Exception  as e:
        res = str(e)
    else:
        res = '连接成功'
    return res

# 配置数据库-修改数据库
@ showdata.route('/add_database/chage/<databaseid>')
def deatavase_chage(databaseid):
    database = file_op.readfile('json','dict_databases')[databaseid]
    # print(database)
    return database


# 配置数据类型--展示页面
@ showdata.route('/add_tree')
def add_tree():
    return render_template("/showdata/add_tree.html", title='_维护页面', dict_nav=file_op.readfile('json', 'dict_nav'))

# 配置数据类型--删除页面
@showdata.route('/show_page/del/<bnt_value>')
def delete(bnt_value):
    dict_nav_read = file_op.readfile('json', 'dict_nav')
    # 循环时，无法删除字典，所以以方法返回
    dict_type, page_name = find_url(dict_nav_read, bnt_value)
    del dict_nav_read[dict_type][page_name]
    if dict_nav_read[dict_type] == {}:
        del dict_nav_read[dict_type]
    file_op.writefile('json', 'dict_nav', dict_nav_read)
    return '删除成功'


# 配置数据类型--新增页面
@showdata.route('/show_page/save', methods=['POST', 'GET'])
def datasave():
    if request.method == 'POST':
        get_type = request.form['type']
        get_page = request.form['page']
        dict_nav_read = file_op.readfile('json', 'dict_nav')
        save_time = round(time.time())
        file_name = Pinyin().get_pinyin(get_page, '') + str(save_time)
        # 将name url 定义为字典
        pre_dic = {}
        pre_dic['name'] = get_page
        pre_dic['url'] = file_name
        # 将新字典加入
        if get_type in dict_nav_read.keys():
            dict_nav_read[get_type][get_page] = pre_dic
        else:
            dict_nav_read[get_type] = {}
            dict_nav_read[get_type][get_page] = pre_dic
        # 保存
        file_op.writefile('json', 'dict_nav', dict_nav_read)

    return render_template('/showdata/add_tree.html', dict_nav=file_op.readfile('json', 'dict_nav'))


# 配置展示数据--打开编辑页面主页
@ showdata.route('/data_source')
def confure():
    databases = file_op.readfile('json', 'dict_databases').keys()
    dict_all={"title": " ", "dataid": " ", "col_select": "checked", "col_select_name": " "}
    return render_template('/showdata/data_source_readme.html', databases=databases,title='_配置展示数据' ,dict_nav=file_op.readfile('json', 'dict_nav'),dict_all=dict_all)

# 配置展示数据--编辑页面
@ showdata.route('/show_confure/<file_serial>')
def show_confure(file_serial):
    page_title = find_url(file_op.readfile('json', 'dict_nav'), file_serial)[0] + '_' + find_url(file_op.readfile('json', 'dict_nav'), file_serial)[1] + '_'
    # print(file_op.readfile('normal_json', file_serial))
    title = eval(file_op.readfile('normal_json', file_serial))['title']
    dataid = eval(file_op.readfile('normal_json', file_serial))['dataid']
    dict_all=eval(file_op.readfile('normal_json', file_serial))
    sql = file_op.readfile('sql', file_serial)
    databases = file_op.readfile('json', 'dict_databases').keys()
    return render_template('/showdata/data_source.html',databases=databases,title='_配置展示数据',dict_nav=file_op.readfile('json', 'dict_nav'), file_serial=page_title + file_serial,dataid=dataid, title_sql=title, sql=sql,dict_all=dict_all)

# 配置展示数据--保存编辑
@ showdata.route('/confure/save', methods=['POST', 'GET'])
def confure_save():
    if request.method == 'POST':
        file_name = request.form['filename'].split('_')[-1]
        title_get = request.form['title']
        sql_get = request.form['sql']
        dataid = request.form['dataid']
        col_select = request.form.get('col_select',default='unchecked')
        col_select_name = request.form['col_select_name']
        file_massge={'title':title_get,'dataid':dataid,'col_select':col_select,'col_select_name':col_select_name}
        file_op.writefile('normal_json', file_name, file_massge)
        file_op.writefile('sql', file_name, sql_get)
        databases = file_op.readfile('json', 'dict_databases').keys()
        page_title = find_url(file_op.readfile('json', 'dict_nav'), file_name)[0] + '_' + find_url(file_op.readfile('json', 'dict_nav'), file_name)[1] + '_'
    return render_template('/showdata/data_source.html',databases=databases,dict_nav=file_op.readfile('json', 'dict_nav'), file_serial=page_title + file_name, title_sql=title_get, sql=sql_get,dataid=dataid,dict_all=file_massge)

# 显示数据--返回列名
@ showdata.route('/show_page/colname/<url>')
def showdate(url):
    table_title = eval(file_op.readfile('normal_json', url))
    return table_title


# 显示数据--返回数据
@ showdata.route('/show_page/data/<url>')
def show_page(url):
    table_title=eval(file_op.readfile('normal_json', url))['title'].split(',')
    dataid=eval(file_op.readfile('normal_json', url))['dataid']
    database = file_op.readfile('json','dict_databases')[dataid]
    # data_mysql = connectdb.mysql(file_op.readfile('sql', url))
    data_mysql = connectdb.run_mysql(database, file_op.readfile('sql', url))
    data = tojson.sql_to_list(data_mysql, table_title)
    return get_date_search(data)
