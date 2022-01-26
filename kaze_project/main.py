# coding=utf-8

from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask import render_template
from flask import Markup
import pymysql
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
 
app = Flask(__name__)

# def return_img_stream(img_local_path):
#     import base64
#     img_stream = ''
#     with open(img_local_path, 'r') as img_f:
#         img_stream = img_f.read()
#         img_stream = base64.b64encode(img_stream)
#     return img_stream


@app.route("/")
def homepage():
    return render_template('homepage.html')


#----------------go to all kinds of web pages-------------
@app.route("/to_homepage",methods=['POST','GET'])
def to_homepage():
    return render_template('homepage.html')

@app.route("/to_introduction",methods=['POST','GET'])
def to_introduction():
    return render_template('introduction.html')
 
@app.route("/to_search",methods=['POST','GET'])
def to_search():
    return render_template('search.html')

@app.route("/to_image",methods=['POST','GET'])
def to_image():
    return render_template('image.html')

@app.route("/to_no_image",methods=['POST','GET'])
def to_no_image():
    return render_template('no_image.html')

@app.route("/to_contact",methods=['POST','GET'])
def to_contact():
    return render_template('contact.html')
#----------------go to all kinds of web pages-------------


@app.route("/year", methods = ['GET'])
def return_year_data():
    year = request.args.get('year', type=int)
    year_last2 = year - 2000
    if year_last2 < 10:
        year_last2 = "0" + str(year_last2)
    else:
        year_last2 = str(year_last2)

    conn = pymysql.connect(host = 'localhost', port = 3306, db = 'kaze', 
        user = 'root', password = '12345678', charset = 'utf8')

    cur = pymysql.cursors.Cursor(conn)
    cur.execute('select typhoon_name from tbl%s group by typhoon_name'%year_last2)
    a = cur.fetchall()
    #typhoon_number = len(a)
    f = lambda x: x[0]
    typhoon_names = list(map(f, a))
    return render_template('typhoon_name_for_search.html', messages = typhoon_names, year = year)



@app.route("/yearname", methods = ['GET'])
def return_typhoon_info():
    year = request.args.get("year", type=int)
    name = request.args.get("name", type=str)
    year_last2 = year - 2000
    if year_last2 < 10:
        year_last2 = "0" + str(year_last2)
    else:
        year_last2 = str(year_last2)

    conn = pymysql.connect(host = 'localhost', port = 3306, db = 'kaze', 
        user = 'root', password = '12345678', charset = 'utf8')

    cur = pymysql.cursors.Cursor(conn)
    cur.execute("select * from tbl%s where typhoon_name = '%s'"%(year_last2, name))

    a = cur.fetchall()
    df = pd.DataFrame(list(a))

    xs = df.iloc[:,6]
    ys = df.iloc[:,5]
    matplotlib.use('Agg')
    #fig = plt.figure()
    #ax = fig.add_subplot(1, 1, 1)
    #ax.plot(xs, ys)
    coast = pd.read_excel("static/coast.xls")
    plt.plot(coast.iloc[:,0], coast.iloc[:,1], color="#D3D3D3")
    plt.plot(xs, ys, color="b")
    plt.xlim(xs.min() - 10, xs.max() + 10)
    plt.ylim(ys.min() - 10, ys.max() + 10)

    xs = np.array(xs)
    ys = np.array(ys)
    plt.text(xs[0] + 1  , ys[0] + 1, 'Start Point')
    plt.text(xs[-1] + 1  , ys[-1] + 1, 'End Point')
    plt.scatter([xs[0], xs[-1]], [ys[0], ys[-1]], color="r")
    plt.xlabel("Longitude (°)")
    plt.ylabel("Latitude (°)")
    path = "static/resultimage%s%s.png"%(year_last2, name)
    plt.savefig(path, api=400, bbox_inches="tight")
    plt.close('all')
    
    time = df.iloc[:, 1]
    length = len(time)
    start_time = time[0].strftime("%Y-%m-%d %H:%M")
    end_time = time[length - 1].strftime("%Y-%m-%d %H:%M")

    typhoon_number = str(df.iloc[0, 2])
    if len(typhoon_number) == 3:
        typhoon_number = "0" + typhoon_number

    typhoon_class = str(df.iloc[:, 4].max())
    max_velocity = str(df.iloc[:, 8].max())
    landing = str(df.iloc[:, 15].max())


    return render_template('image.html', name=name, year=year, path=path, start_time=start_time,
        end_time=end_time, typhoon_number=typhoon_number, typhoon_class=typhoon_class,
        max_velocity=max_velocity, landing=landing)




# @app.route('/hello')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         session['user'] = request.form['user']
#         flash('Login successfully!')
#         return redirect(url_for('index'))
#     else:
#         return '''
#         <form name="login" action="/login" method="post">
#             Username: <input type="text" name="user" />
#         </form>
#         '''


 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)