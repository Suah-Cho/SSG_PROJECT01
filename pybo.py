
import math
from flask import Flask, render_template, request, redirect, url_for
import pymysql

# 데이터 베이스 연동
db = pymysql.connect(host="localhost", 
                     user="root", password="passwd", 
                     db="test3",
                     charset="utf8")

cursor = db.cursor()


app = Flask(__name__)

@app.route('/', defaults={'page':1})
@app.route('/list/<int:page>')
def paging(page) :
    print(page)

    perpage = 10
    startat=(page-1)*perpage
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE b.status = 'active' ORDER BY b.createAt DESC LIMIT "+str(startat)+", "+str(perpage)+";")
    data_list = list(cursor.fetchall())

    return render_template("list.html", data_list = data_list)

@app.route('/edit/')
def edit() :
    return render_template("edit.html")

@app.route('/view')
def view() :
    print(request.method)
    
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.content, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = (SELECT MAX(boardId) FROM Board) ORDER BY b.createAt DESC;",)
    data = cursor.fetchall()
    print(data)

    return render_template("view.html", data = data)

@app.route('/listview/<int:id>')    
def view2(id) :
    print("id = ", id)
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.content, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = {} ORDER BY b.createAt DESC;".format(id))
    data = cursor.fetchall()
    print(data)

    return render_template("view.html", data = data)



@app.route('/write/', methods=['GET', 'POST'])
def write() :
    print(request.method)
    if request.method == 'GET' :
        return render_template("write.html")
    elif request.method == 'POST' :
        
        title = request.form['title']
        user = request.form['username']
        location = request.form['userlocation']
        contents = request.form['body']
       
        
        cursor.execute("INSERT INTO Board (userId, title, content, location) VALUES ((SELECT userId FROM User WHERE ID = %s), %s, %s, %s);", (user, title, contents, location))
        cursor.connection.commit()

        return redirect(url_for('view'))




def main() :
    app.run(debug=True, port=80)

if __name__ == '__main__' :
    main()



