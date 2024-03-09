import pymysql
from flask import Flask, render_template, redirect

app = Flask(__name__, template_folder='pages', static_folder='static')


@app.route('/')
def home():
    return redirect('http://36.134.148.174:9110/index.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/index1.html')
def ariticle():
    # 跳转到另一个模板 
    # 数据库连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='Ujs32138.', db='yuqin')
    # 检查连接是否成功
    if conn:
        print('数据库连接成功')
    else:
        print('数据库连接失败')
    cursor = conn.cursor()
    sql = "SELECT title, content, url, publish_time, key_word, sentiment FROM article"
    cursor.execute(sql)
    results = cursor.fetchall()
    data = []
    for row in results:
        title = row[0]
        content = row[1]
        url = row[2]
        publish_time = row[3]
        key_word = row[4]
        sentiment = row[5]
        data.append([title, content, url, publish_time, key_word, sentiment])
    cursor.close()
    conn.close()

    return render_template('index1.html', data=data)


@app.route('/index2.html')
def comment():
    # 跳转到另一个模板
    # 数据库连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='Ujs32138.', db='yuqin')
    # 检查连接是否成功
    if conn:
        print('数据库连接成功')
    else:
        print('数据库连接失败')
    cursor = conn.cursor()

    # 执行查询语句
    sql = 'SELECT u_name, comment, publish_time, url, sentiment FROM comment '
    cursor.execute(sql)

    # 获取查询结果
    results = cursor.fetchall()

    # 关闭游标和连接
    cursor.close()
    conn.close()

    # 将结果传到前端表格中
    data = []
    for result in results:
        username = result[0]
        content = result[1]
        publish_time = result[2]
        url = result[3]
        sentiment = result[4]
        data.append([username, content, publish_time, url, sentiment])
    return render_template('index2.html', data=data)


@app.route('/index3.html')
def yaowen():
    # 跳转到另一个模板
    # 数据库连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='Ujs32138.', db='yuqin')
    # 检查连接是否成功
    if conn:
        print('数据库连接成功')
    else:
        print('数据库连接失败')
    cursor = conn.cursor()
    sql1 = "select title,content,publish_time,url,sentiment from yaowen where source='国务院';"
    cursor.execute(sql1)
    result1 = cursor.fetchall()

    sql2 = "select title,content,publish_time,url,sentiment from yaowen where source='江大官网';"
    cursor.execute(sql2)
    result2 = cursor.fetchall()

    data = {'data1': result1, 'data2': result2}

    return render_template('index3.html', data=data)


@app.route('/index4.html')
def hot():
    # 数据库连接
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='Ujs32138.', db='yuqin')
    # 检查连接是否成功
    if conn:
        print('数据库连接成功')
    else:
        print('数据库连接失败')
    cursor = conn.cursor()
    sql1 = "SELECT rank_num, title, num, sentiment FROM wb_dy_hot WHERE source = '抖音' ORDER BY rank_num ASC LIMIT 10;"
    cursor.execute(sql1)
    result1 = cursor.fetchall()

    sql2 = "SELECT rank_num, title, num, sentiment FROM wb_dy_hot WHERE source = '微博' ORDER BY rank_num ASC LIMIT 10;"
    cursor.execute(sql2)
    result2 = cursor.fetchall()

    sql3 = "SELECT rank_num, title, sentiment FROM wc_bili_hot WHERE source = 'Bilibili' ORDER BY rank_num ASC LIMIT 10;"
    cursor.execute(sql3)
    result3 = cursor.fetchall()

    sql4 = "SELECT rank_num, title, sentiment FROM wc_bili_hot WHERE source = 'weixin' ORDER BY rank_num ASC LIMIT 10;"
    cursor.execute(sql4)
    result4 = cursor.fetchall()

    data = {"data1": result1, 'data2': result2, 'data3': result3, 'data4': result4}
    # 跳转到另一个模板
    return render_template('index4.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9110)
