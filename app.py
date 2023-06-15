from flask import Flask,render_template,request,g,redirect,url_for,flash
import sqlite3 as sql                          #↑
#from flask import g----------------------------↑在這上面，一種省略寫法
import os
import uuid
import hashlib

DATABASE = 'database.db'

UPLOAD_FOLDER = 'static/images2/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def allowed_file(filename):
    x = ""
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        x = filename.rsplit('.', 1)[1].lower()
    return x

def sha256(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


@app.route("/")
def hello_python():
    return "<p>Hello, python!</p>"

@app.route("/name/<name>")
def name(name):
    print('Type:',type(name))
    return name

@app.route("/number/<int:number>")
def number(number):
    print('Type:',type(number))
    return f"{number}"

@app.route("/page")
def page():
    x="1234"
    dict1 = {"abc":1324,"name":"tom"}
    return render_template("page.html",a=x,b=dict1)
#def email():
#    email = request.args.get("email")
#    password = request.args.get("password")
#    return f"{email},{password}"
#http://127.0.0.1:5000/page?email=13&password=12

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":                                 #這裡沒有亮藍色
        type = "登入失敗"
        name = request.form.get("account")
        password = request.form.get("password")
        password = sha256(password)
        with get_db() as cur: #with get_db().cursor() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor() #上面的註解可以把這行省略
            cur.execute(f"select * from Users")
            data = cur.fetchall()
            cur.close()
        for i in data:
            if name == i["account"] and password == i["password"]:
                type ="成功"
                return render_template("page2.html",id=name,ps=password,type=type)
        else:
            return render_template("login.html",type=type,name=name,password=password)
    else:
        return render_template("login.html")

@app.route("/users")
def users():
    with get_db() as cur: #with get_db().cursor() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor() #上面的註解可以把這行省略
        cur.execute("select * from Users")
        data = cur.fetchall()
        cur.close()
    return render_template("users.html",data = data)

@app.route("/suggestion")
def suggestion():
    with get_db() as cur: #with get_db().cursor() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor() #上面的註解可以把這行省略
        cur.execute("select * from Suggestion")
        data = cur.fetchall()
        cur.close()
    return render_template("suggestion.html",data = data)

@app.route("/createuser",methods=["POST"])
def createuser():
    account = request.form.get("account")
    name = request.form.get("username")   #沒有亮黃光
    type = "註冊成功"
    if name =="":name = "User"
    with get_db() as cur: #with get_db().cursor() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor() #上面的註解可以把這行省略
            cur.execute(f"select * from Users")
            data = cur.fetchall()
            cur.close()
    for i in data:
        if account == i["account"]:
            type = "此帳號已註冊"
            return render_template("users.html",type = type)
    account = request.form.get("account")
    password = request.form.get("password")
    password = sha256(password)
    with get_db() as cur: #with get_db().cursor() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor() #上面的註解可以把這行省略
        cur.execute(f"INSERT INTO Users (name, account, password) VALUES ('{name}','{account}','{password}');")
        cur.close()
    flash('新增成功')
    return redirect(url_for('users'))
    return render_template("users.html",data = data)                                               ###所以這行能刪掉嗎?###

@app.route("/edit/<int:id>",methods=["GET","POST"])
def edit(id):
    if request.method =="POST":
        name = request.form.get("username")   #沒有亮黃光
        account = request.form.get("account")
        password = request.form.get("password")
        password = sha256(password)
        with get_db() as cur: #with get_db().cursor() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor() #上面的註解可以把這行省略
            cur.execute(f"UPDATE Users SET name='{ name }', account='{account}', password='{password}' WHERE id='{id}';")
            data = cur.fetchone()
            cur.close()
        flash('修改成功')
        return redirect(url_for('users'))
    else:
        with get_db() as cur: #with get_db().cursor() as cur:
            cur.row_factory = sql.Row
            cur = cur.cursor() #上面的註解可以把這行省略
            cur.execute(f"select * from Users where id = {id}")
            data = cur.fetchone()
            return render_template("edit.html",data = data)

@app.route("/deleteuser/<int:id>",methods=["POST"])
def deleteuser(id):
    with get_db() as cur: #with get_db().cursor() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor() #上面的註解可以把這行省略
        cur.execute(f"DELETE FROM Users where id={id}")
        #cur.execute("select * from Users")
        #data = cur.fetchall()
        cur.close()
    flash('刪除成功')
    return redirect(url_for('users'))
    #return render_template("users.html",data=data)

@app.route("/deletesug/<int:id>",methods=["POST"])
def deletesug(id):
    with get_db() as cur: #with get_db().cursor() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor() #上面的註解可以把這行省略
        cur.execute(f"DELETE FROM Suggestion where id={id}")
        #cur.execute("select * from Users")
        #data = cur.fetchall()
        cur.close()
    flash('刪除成功')
    return redirect(url_for('suggestion'))

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "POST":
        f = request.files["file"]
        f.filename = allowed_file(f.filename)
        name = str(uuid.uuid4())+"."+f.filename
        if f.filename == "":
            type = "副檔名不符"
        else:
            type="新增成功"
            with get_db() as cur: #with get_db().cursor() as cur:
                cur.row_factory = sql.Row
                cur = cur.cursor() #上面的註解可以把這行省略
                data = cur.execute(f"select * from Pictures")
                order = 0
                for i in data:
                    if i["p_order"] > order:
                        order = i["p_order"]
                cur.execute(f"INSERT INTO Pictures (p_name,p_order) VALUES ('{name}','{order+1}');")
                cur.close()
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
        return render_template("upload.html",type=type)
    return render_template("upload.html")

@app.route("/show")
def show():
    with get_db() as cur: #with get_db().cursor() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor() #上面的註解可以把這行省略
        cur.execute("select * from Pictures order by p_order") #DESC，由大排到小，放在p_order後面
        data = cur.fetchall()
        cur.close()
    return render_template("show.html",data=data)

@app.route("/pictures")
def pictures():
    with get_db() as cur: #with get_db().cursor() as cur:
        cur.row_factory = sql.Row
        cur = cur.cursor() #上面的註解可以把這行省略
        cur.execute("select * from Pictures order by p_order")
        data = cur.fetchall()
        length = len(data)
        for i in data:
            if i["p_order"] > length:
                length = i["p_order"]
        cur.close()
    return render_template("pictures.html",data=data,len=length)

@app.route("/MP",methods=["POST"])
def MP():
    with get_db() as cur: #with get_db().cursor() as cur:
        id = request.form.get("id")
        fun = request.form.get("fun")
        if fun == "修改":
            p_order = request.form.get("p_order")
            with get_db() as cur: #with get_db().cursor() as cur:
                cur.row_factory = sql.Row
                cur = cur.cursor() #上面的註解可以把這行省略
                cur.execute(f"UPDATE Pictures SET p_order='{ p_order }' WHERE id='{id}';")
                cur.close()
            flash("修改成功")
        else:
            p_name = request.form.get("p_name")
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], p_name))
            with get_db() as cur:
                cur.row_factory = sql.Row
                cur = cur.cursor()
                cur.execute(f"DELETE FROM Pictures WHERE id='{id}';")
                cur.close()
            flash("刪除成功")
        return redirect(url_for("pictures"))

if __name__ =="__main__":
    app.secret_key = "Your Key"
    app.run(debug=True)