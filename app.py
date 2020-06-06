# Import Flask来创建server
from flask import Flask
# Import render_template来渲染HTML
from flask import render_template
# Import request 来得到请求
from flask import request
# Import redirect和url_for来支持跳转
from flask import redirect, url_for
# Import PyMongo来建立database cursor
from flask_pymongo import PyMongo

# 一个server就是一个Flask Object
server = Flask(__name__)
# 将Mongo URI添加到server的config里
server.config["MONGO_URI"] = "<fill your mongo uri>"
# 创建Database Cursor
database_cursor = PyMongo(server)
# Decorator用来负责监听对应的path
# 修改decorator来添加method/request
# 创建Response
@server.route("/", methods=["GET", "POST"])
def index_response():
    request_type = request.method
    if request_type.upper() == "GET":
        return "<h1> Get request for the index page</h1>"
    elif request_type.upper() == "POST":
        return "<h1> Post request for the index page</h1>"


# 使用 <> 来在url中添加variable
@server.route("/users/<user_name>")
def user_name_response(user_name):
    return render_template("user_template.html", user_name_html=user_name)


@server.route("/users")
def users_response():
    return render_template("users.html", user_list=["dino", "jin", "frank"])


@server.route("/admin/<login_name>")
def admin_response(login_name):
    if login_name.upper() == "ADMIN":
        return "<h1> Admin Page </h1>"
    else:
        return redirect(url_for("user_name_response", user_name=login_name))


@server.route("/signup", methods=["GET", "POST"])
def sign_up_response():
    request_type = request.method
    if request_type == "GET":
        return render_template("signup.html")
    else:
        request_form = request.form
        user_name = request_form.get("username")
        password = request_form.get("password")
        db = database_cursor.db
        # database collection = db.<collection_name>
        user_password_collection = db.user_password
        # insert_one 用来向collection添加数据
        user_password_collection.insert_one({"username": user_name,
                                             "password": password})
        return redirect(url_for("user_name_response", user_name=user_name))


@server.route("/login", methods=["GET", "POST"])
def login_response():
    request_type = request.method
    if request_type == "GET":
        return render_template("login.html")
    else:
        request_form = request.form
        user_name = request_form.get("username")
        password = request_form.get("password")
        db = database_cursor.db
        # database collection = db.<collection_name>
        user_password_collection = db.user_password
        # 使用 find one来从database fetch数据
        # pass filter dictionary
        user = user_password_collection.find_one({"username": user_name,
                                             "password": password})
        if user is not None:
            return redirect(url_for("user_name_response", user_name=user_name))
        else:
            return redirect(url_for("login_response"))


if __name__ == "__main__":
    server.run(debug=True)