import pymysql
from flask import Flask
from flask import render_template, request, session, url_for, redirect, flash, g
import sqlite3
import config

conn = pymysql.connect(host = 'localhost', port = 3306, db = 'kaze', 
    user = 'root', password = '12345678', charset = 'utf8')

cur = pymysql.cursors.Cursor(conn)
cur.execute('select count(*) from tbl01')
print(cur.fetchall())