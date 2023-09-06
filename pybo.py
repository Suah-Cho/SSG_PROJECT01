
import math
from flask import Flask, render_template, request, redirect, url_for
import pymysql
import utils.utils as utils
from flask_cors import CORS

# 데이터 베이스 연동
db = pymysql.connect(host="localhost", 
                     user="root", password="passwd", 
                     db="test3",
                     charset="utf8")

cursor = db.cursor()


app = Flask(__name__)
# @app.route('/', defaults={'page':1})
@app.route('/')
def list() :

    cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') FROM board as b LEFT OUTER JOIN user as u on u.userId = b.userId ORDER BY b.createAt DESC LIMIT 0, 3;")
    data_list = cursor.fetchall()

    return render_template("index.html", data_list = data_list)

@app.route('/list', defaults={'page':1})
@app.route('/list/<int:page>')
def paging(page) :
    print(page)

    perpage = 10
    startat=(page-1)*perpage
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE b.status = 'active' ORDER BY b.createAt DESC LIMIT "+str(startat)+", "+str(perpage)+";")
    data_list = cursor.fetchall()

    return render_template("list.html", data_list = data_list)

@app.route('/listview/<int:id>')    
def view2(id) :
    print("id = ", id)
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.content, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = {} ORDER BY b.createAt DESC;".format(id))
    data = cursor.fetchall()
    print(data)

    return render_template("view.html", data = data)


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

@app.route('/signup')
def signup() :
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def createUser():
    try:

        name = str(request.form.get('name'))
        ID = str(request.form.get('ID'))
        password = str(request.form.get('password'))
        phoneNumber = str(request.form.get('phoneNumber'))

        password_confirm = str(request.form.get('password_confirm'))
        print(name, ID, password, password_confirm, phoneNumber)
        
        if len(ID) < 4 or len(ID) > 16 :
            return '''
                <script> alert("회원 가입에 실패했습니다.\\n  - 아이디는 4~16자로 작성하세요.");
                location.href="/signup"
                </script>
                '''
        if not utils.onlyalphanum(ID) :
            return '''
                <script> alert("회원 가입에 실패했습니다.\\n - 아이디는 영문 대소문자와 숫자로 작성하세요");
                location.href="/signup"
                </script>
                '''
        if not phoneNumber.isdecimal() :
            return '''
                <script> alert("회원 가입에 실패했습니다.\\n -  전화번호는 숫자만 작성하세요. ");
                location.href="/signup"
                </script>
                '''
        if  not name.isalpha():
            return '''
                <script> alert("회원 가입에 실패했습니다.\\n  - 이름은 한글 또는 영어로만 작성하세요");
                location.href="/signup"
                </script>
                '''
        if  password != password_confirm:
            return '''
                <script> alert("회원 가입에 실패했습니다.\\n  - 비밀번호 확인 란에 동일한 비밀번호를 입력하세요.");
                location.href="/signup"
                </script>
                '''
            

        hashed_password = utils.hash_password(str(password))

        user_info = [ name , ID , hashed_password, phoneNumber ]
        
        # a = userdao.createUser(user_info)

        cursor.execute("INSERT INTO User(name, ID, password, phoneNumber) VALUES (%s, %s, %s, %s)", 
                      (user_info[0], user_info[1], user_info[2], user_info[3]))
        
        print("before commit")
        cursor.connection.commit()
        print("after commit")


        return '''
                <script> alert("환영합니다. 회원가입에 성공했습니다 :) ");
                location.href="/"
                </script>
                '''
    
    except Exception as e :
        return {'error': str(e)}


def main() :
    app.run(debug=True, port=80)

if __name__ == '__main__' :
    main()



