
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
# def list() :

#     # cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') FROM board as b LEFT OUTER JOIN user as u on u.userId = b.userId WHERE b.status = 'active' ORDER BY b.createAt DESC;")
#     # rows = cursor.fetchmany(size=10)

#     # while rows :
#     #     data_list = cursor.fetchmany(size=10)
#     #     return render_template("list.html", data_list = data_list)

    
#     # print(rows)
#     # data_list = cursor.fetchall()


#     # page = request.args.get('page', type=int, default=1)
#     # data_list = data_list.paginate(page, per_page=10)

#     return render_template("list.html")
@app.route('/<int:page>')
def paging(page) :
    perpage = 10
    startat=page*perpage
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') FROM board as b LEFT OUTER JOIN user as u on u.userId = b.userId WHERE b.status = 'active' ORDER BY b.createAt DESC LIMIT "+str(startat)+", "+str(perpage)+";")
    data_list = list(cursor.fetchall())

    return render_template("list.html", data_list = data_list)

@app.route('/edit/')
def edit() :
    return render_template("edit.html")

@app.route('/view', methods=['GET', 'POST'])
def view() :
    print(request.method)
    
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.content, b.location, date_format(b.createAt, '%Y-%m-%d') FROM board as b LEFT OUTER JOIN user as u on u.userId = b.userId WHERE boardId = (SELECT MAX(boardId) FROM board) ORDER BY b.createAt DESC;",)
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
       
        
        cursor.execute("INSERT INTO board (userId, title, content, location) VALUES ((SELECT userId FROM user WHERE ID = %s), %s, %s, %s);", (user, title, contents, location))
        cursor.connection.commit()

        return redirect(url_for('view'))
    # return render_template("write.html")




def main() :
    app.run(debug=True, port=80)

if __name__ == '__main__' :
    main()



