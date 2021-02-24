#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template
from functions.showdata.showdataurl import showdata


app = Flask(__name__)
app.register_blueprint(showdata, url_prefix='/showdata')



@app.route('/')
def hello_world():
    return render_template('head/welcome.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
