from flask import Flask,  render_template, request, redirect, url_for, session # pip install Flask
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb


app = Flask(__name__)
app.config['MYSQL_HOST'] = ' '#ingresar host de tu DB
app.config['MYSQL_USER'] = ' '#ingresar el user que entrega tu base de datos
app.config['MYSQL_PASSWORD'] = ' '#ingresar la contraseña en tu base de datos*/
app.config['MYSQL_DB'] = 'useraccountdb'#ingresar nombre de tu DB
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("contenido.html")    

@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("contenido.html")


@app.route('/login', methods= ["GET", "POST"])
def login():

    

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = cur.fetchone()
        cur.close()

        if len(user)>0:
            if password == user["password"]:
                session['name'] = user['name']
                session['email'] = user['email']
                session['tipo'] = user['id_tip_usu']

                if session['tipo'] == 1:
                    return render_template("premium/home.html")
                
            else:
                
                return render_template("login.html")
        else:
            
            return render_template("login.html")
    else:
        
        return render_template("login.html")



@app.route('/registro', methods = ["GET", "POST"])
def registro():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tip_usu")
    tipo = cur.fetchall()

    cur.close()

    if request.method == 'GET':
        return render_template("registro.html", tipo = tipo )
    
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        tip = request.form['tipo']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, id_tip_usu) VALUES (%s,%s,%s,%s)", (name, email, password,tip))
        mysql.connection.commit()
        
        return redirect(url_for('login'))


    
if __name__ == '__main__':
    app.secret_key = "pinchellave"
    app.run(host='0.0.0.0', port='80',debug=True)
    