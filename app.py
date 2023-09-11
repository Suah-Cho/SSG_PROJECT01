from flask import *
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
app.config['SECRET_KEY'] = 'asdf'

@app.route('/', methods=['GET', 'POST'])
def index() :
    global cursor

    if request.method == 'GET' :
        if 'id' in session:
            cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE b.status = 'active' ORDER BY b.createAt DESC LIMIT 0, 3;")
            data_list = cursor.fetchall()

            return render_template('login.html', data_list=data_list, a = session['id'])
        
        else :
            cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE b.status = 'active' ORDER BY b.createAt DESC LIMIT 0, 3;")
            data_list = cursor.fetchall()

            return render_template("index.html", data_list = data_list)
        
    elif request.method == 'POST' :

        id_receive = request.form.get('username')
        pw_receive = request.form.get('password')
              
        # 입력 x
        if len(id_receive) == 0 or len(pw_receive) == 0:
            return redirect(url_for('index'))
        
        # 입력 o
        else:
            # 입력받은 id에 해당하는 row 가져옴
            cursor = db.cursor()
            sql = "select userId, ID, password from User where ID=%s and status= 'active';"
            cursor.execute(sql, id_receive) #none / user정보 한줄
             
            # 입력받은 user가 db에 있으면 해당 row 한줄을 가져옴 
            row = cursor.fetchone()
            
            # id, pw 체크 (row[2] = ID정보, row[3] = password정보)

            if row and id_receive == row[1] and  utils.verfifyPwd(pw_receive, row[2]):
                
                # session id, userid 오브젝트 생성*저장
                session['logFlag'] = True
                session['id'] = id_receive
                session['userid'] = row[0]
                
                
                # 로그인 성공 메시지 출력 후 /sesesion 이동 
                return '''
                    <script> alert("안녕하세요, {}님 :)");
                    location.href="/"
                    </script>
                '''.format(id_receive)      
            
            else:
                return '''
                    <script> alert("회원가입을 해주세요 :)");
                    location.href="/signup"
                    </script>
                '''

    else:
        return 'wrong access'      


@app.route('/logout', methods=['GET', 'POST'])
def logout() :
    session.pop('id', None)
    return redirect(url_for('index'))

    

@app.route('/list', defaults={'page':1})
@app.route('/list/<int:page>')
def paging(page) :

    perpage = 10
    startat=(page-1)*perpage
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE b.status = 'active' ORDER BY b.createAt DESC LIMIT "+str(startat)+", "+str(perpage)+";")
    data_list = cursor.fetchall()

    return render_template("list.html", data_list = data_list)

@app.route('/toylist', defaults={'page':1})
@app.route('/toylist/<int:page>')
def toylistpaging(page):
    perpage = 10
    startat = (page - 1) * perpage
    cursor.execute("select boardId, title, userage, area, date_format(createAt, '%Y-%m-%d') FROM ToyBoard WHERE status = 'active' ORDER BY createAt DESC LIMIT "+str(startat)+", "+str(perpage)+";")
    data_list = cursor.fetchall()

    return render_template("toylist.html", data_list=data_list)

@app.route('/listview/<int:id>')    
def view2(id) :

    cursor.execute("SELECT b.boardId, b.title, u.ID, b.content, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = {} ORDER BY b.createAt DESC;".format(id))
    data = cursor.fetchall()

    return render_template("view.html", data = data)

@app.route('/toylistview/<int:id>')    
def toyview(id) :

    # cursor.execute("SELECT b.boardId, b.title, u.ID, b.content, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = {} ORDER BY b.createAt DESC;".format(id))
    cursor.execute("SELECT boardId, title, content, userage, area, phoneNumber, rent, createAt FROM ToyBoard WHERE boardId = {} ORDER BY createAt DESC;".format(id))
    
    data = cursor.fetchall()

    return render_template("toyview.html", data = data)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id) :
    if request.method == 'GET' :
        cursor.execute("SELECT u.ID FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = {};".format(id))
        userId = cursor.fetchall()
        userId = userId[0][0]
        ID = session.get('id')

        if userId != ID :
            return '''
                    <script> alert("권한이 없습니다 :)");
                    location.href="/list"
                    </script>
                '''

        cursor.execute("SELECT b.boardId, b.title, u.ID, b.content, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = {} ORDER BY b.createAt DESC;".format(id))
        data = cursor.fetchall()

        return render_template("edit.html", data=data, ID = ID)
    
    elif request.method == 'POST' :
        ID = session.get('id')
            
        # location = request.form.get('userlocation')
        contents = request.form.get('body')
        print(id , type(id))
        cursor.execute("UPDATE Board SET content = '{}' WHERE boardId = {};".format(contents, id))
        cursor.connection.commit()

        return redirect(url_for('view2', id=id))
        

    return render_template("edit.html")

# 게시글 삭제
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def edit_delete(id) :
    if request.method == 'GET' :
        cursor.execute("SELECT u.ID FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = {};".format(id))
        userId = cursor.fetchall()
        userId = userId[0][0]   # userId 값 받는 부분 복사함
        ID = session.get('id')  # ID값 session으로 받는 부분 복사함

        if userId != ID :
            return '''
                    <script> alert("게시글 삭제 권한이 없습니다 :)");
                    location.href="/list"
                    </script>
                '''

        else:
            cursor.execute("UPDATE Board SET status = 'inactive' WHERE boardId = {};".format(id))
            cursor.connection.commit()
            return '''
                    <script> alert("해당 게시글이 삭제되었습니다. :)");
                    location.href="/list"
                    </script>
                '''

@app.route('/view')
def view() :
    
    cursor.execute("SELECT b.boardId, b.title, u.ID, b.content, b.location, date_format(b.createAt, '%Y-%m-%d') FROM Board as b LEFT OUTER JOIN User as u on u.userId = b.userId WHERE boardId = (SELECT MAX(boardId) FROM Board) ORDER BY b.createAt DESC;")
    data = cursor.fetchall()

    return render_template("view.html", data = data)




@app.route('/write/', methods=['GET', 'POST'])
def write() :

    if request.method == 'GET' :
        ID=session.get('id')
        if 'id' in session :
            return render_template("write.html", ID = ID)
        else :
            return '''
                    <script> alert("로그인을 해주세요:)");
                    location.href="/"
                    </script>
                '''
    
    elif request.method == 'POST' :
        if 'id' in session :

            title = request.form.get('title')
            ID = session.get('id')
            
            location = request.form.get('userlocation')
            contents = request.form.get('body')
            
            cursor.execute("INSERT INTO Board (userId, title, content, location) VALUES ((SELECT userId FROM User WHERE ID = %s), %s, %s, %s);", (ID, title, contents, location))
            cursor.connection.commit()

            return redirect(url_for('view'))
        else :
            return '''
                    <script> alert("로그인을 해주세요:)");
                    location.href="/"
                    </script>
                '''
        
        

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

        #ID existence check
        cursor.execute("SELECT ID from User WHERE ID = %s", ID)
        checkID = cursor.fetchone()

        if checkID:
            return '''
                <script> alert("회원 가입에 실패했습니다.\\n  - 존재하는 아이디입니다. 다른 아이디를 사용해주세요.");
                location.href="/signup"
                </script>
                '''

        #phoneNumber existence check
        cursor.execute("SELECT phoneNumber from User WHERE phoneNumber = %s", phoneNumber)
        checkPhone= cursor.fetchone()

        if checkPhone :
            return '''
                <script> alert("회원 가입에 실패했습니다.\\n  - 존재하는 전화번호 입니다. 다시 확인해주세요");
                location.href="/signup"
                </script>
                '''
        
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

        cursor.execute("INSERT INTO User(name, ID, password, phoneNumber) VALUES (%s, %s, %s, %s)", 
                      (user_info[0], user_info[1], user_info[2], user_info[3]))
        
        cursor.connection.commit()


        return '''
                <script> alert("환영합니다. 회원가입에 성공했습니다 :) ");
                location.href="/"
                </script>
                '''
    
    except Exception as e :
        return {'error': str(e)}
    

#회원탈퇴
@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        # ID = str(request.form.get('ID'))
    
        if 'userid' in session :

            userId = session.get('userid')
            cursor.execute("UPDATE User SET status = 'inactive' WHERE userId = %s and status = 'active' ", userId)
            
            cursor.connection.commit()

            # return redirect(url_for('delete_user_complete'))
            return '''
                    <script> alert("감사합니다. 회원 탈퇴에 성공했습니다 :) ");
                    location.href="/logout"
                    </script>
                    '''
    
    
    except Exception as e :
        return {'error': str(e)}   


def main() :
    app.run(debug=True, port=80)

if __name__ == '__main__' :
    main()



