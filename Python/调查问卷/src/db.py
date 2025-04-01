import os
import sqlite3
import pandas as pd
from loguru import logger

DB_FILE = "信息网络安全大队_数据库文件.db"

def init_sqlite_db(conn): #初始化数据库
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            姓名 TEXT,
            学号 INTEGER PRIMARY KEY,
            年级 INTEGER,
            区队 TEXT
        )
    ''')
    cursor.execute('''        
        CREATE TABLE IF NOT EXISTS score (
            评分人姓名 TEXT,
            评分人学号 INTEGER,
            被评分名字 TEXT,
            被评分学号 INTEGER,
            区队 TEXT,
            理想信念分数 INTEGER,
            爱国情怀分数 INTEGER,
            道德品质分数 INTEGER,
            集体观念分数 INTEGER,
            法治观念分数 INTEGER,
            总分 INTEGER,
            平均分 INTEGER,
            PRIMARY KEY (评分人学号, 被评分学号)  -- 设置联合主键
        )''')
    conn.commit()
    logger.success("数据库初始化成功")


def inset_db_excal(conn, excel_file):
    df = pd.read_excel(excel_file)
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO users (
                姓名, 学号, 年级, 区队
            ) VALUES ( ?,  ?, ?, ?)
        """, (
             row['姓名'],  row['学号'], row['年级'], row['区队']
        ))
    conn.commit()
    logger.success(f"已从 {excel_file} 插入 {len(df)} 条数据")


def init_database():
    if not os.path.exists(DB_FILE):
        logger.debug("未识别到数据文件，开始创建")
        conn = sqlite3.connect(DB_FILE)   #创建数据库文件
        init_sqlite_db(conn)
        path = os.getcwd()
        excel_file = os.path.join(path, 'excal', '22网一.xlsx')
        excel_file2 =  os.path.join(path, 'excal', '22计科.xlsx')
        excel_file3 =  os.path.join(path, 'excal', '22网二.xlsx')
        excel_file4 =  os.path.join(path, 'excal', '22网执.xlsx')
        inset_db_excal(conn, excel_file4)
        inset_db_excal(conn, excel_file3)
        inset_db_excal(conn, excel_file2)
        inset_db_excal(conn, excel_file)
    else:
        logger.info("数据库文件识别成功 正在连接")
        conn = sqlite3.connect(DB_FILE)
    return conn


def get_name():
    conn = sqlite3.connect('信息网络安全大队_数据库文件.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 姓名 FROM users where  学号==')