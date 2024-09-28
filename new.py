from flask import Flask,jsonify,request,render_template 
from flask_cors import CORS
import mysql.connector
import bcrypt

app = Flask(__name__)
CORS(app)

def create_connection():
    connection=mysql.connector.connect(
        user="root",
        database="customer_database",
        host="localhost",
        password=""
    )
    if connection.is_connected():
        return connection
    else:
        return jsonify({"message":"there is a error therefore can not connected to the database"})

@app.route('/register')
def register_page():
    return render_template('register.html')

# Serve the login HTML page
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/registers',methods=["post"])
def register():
    data=request.get_json()
    name=data["name"]
    connection=create_connection()
    find_user_alrady_exist=connection.cursor()
    register_user=connection.cursor()

    find_user=f"select user_name from customer where user_name='{name}'"
    find_user_alrady_exist.execute(find_user)
    find_customer_already_registered=find_user_alrady_exist.fetchone()

    if find_customer_already_registered:
        return jsonify({"message":"You already registerd"})
    else:
        email=data["email"]
        password=data["password"]
        confirm_password=data["confirm_password"]
        if password==confirm_password:
            password = password.encode("utf-8")
            h_password = bcrypt.hashpw(password,bcrypt.gensalt(14))
            register_customer=f"insert into customer (user_name,password,email) values(%s,%s,%s)"
            register_user.execute(register_customer,(name,h_password,email))
            connection.commit()
            return jsonify({"message":"sucuessfully registered to the system"})
        else:
            return jsonify({"message":"please check again the password and confirm password are same"})
    find_user_alrady_exist.close()
    register_user.close()
    connection.close()

@app.route('/loginscreen',methods=["get"])
def login_screen():
    return jsonify({"message":"Sucuessfully login"})

@app.route('/logins',methods=["post"])
def login():
    data=request.get_json()
    connection=create_connection()
    find_user_in_system=connection.cursor()
    user_name=data["user"]
    find_user_name_password=f"select user_name,password from customer where user_name='{user_name}'"
    find_user_in_system.execute(find_user_name_password)
    username_password=find_user_in_system.fetchone()
    if username_password:
        stored_user_name,stored_password=username_password
        stored_password = stored_password.encode('utf-8')
        password=data["password"].encode('utf-8')
        if bcrypt.checkpw(password,stored_password):
            return jsonify({"message":"Login successfully"})
        else:
            return jsonify({"message":"please check the password"})
    else:
        return jsonify({"message":"you are not in the system please create a account"})

    find_user_in_system.close()
    connection.close()


if __name__ == '__main__': 
    app.run(debug=True)