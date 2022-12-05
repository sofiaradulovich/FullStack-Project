#desde aca se enruta y se hace las funcionalidades de las paginas
from flask import Flask;
from flask import render_template, request;
from flaskext.mysql import MySQL;

app = Flask(__name__);


mysql = MySQL() 
app.config['MYSQL_DATABASE_HOST'] ="localhost"
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_DB'] = 'sistema22538'

mysql.init_app(app);


@app.route('/')
def main():

    """sql = "INSERT INTO `empleados` (`id`, `nombre`, `email`, `imagen`) VALUES (NULL, 'Sofia', 'sofi@gmail.com', 'sofia.jpg');" #se guarda la consulta (select from)
    conn = mysql.connect(); # se conecta a la base de datos
    cursor = conn.cursor(); #el cursor interactua con la base de datos
    cursor.execute(sql); #ejecutar consulta
    conn.commit(); #cerrar la operacion"""

    prueba = 'SELECT user,authentication_string,plugin,host FROM mysql.user'
    conn = mysql.connect(); # se conecta a la base de datos
    cursor = conn.cursor(); #el cursor interactua con la base de datos
    probando= cursor.fetchall(); 
    print(probando)
    cursor.execute(prueba); #ejecutar consulta
    conn.commit(); #cerrar la operacion"""

    return render_template('empleados/index.html');    
#estructura para hacer todas las rutas



@app.route('/create')
def create():
    return render_template('empleados/create.html');

@app.route('/storage', methods=['POST'])
def storage():
    nombre = request.form['nombreValue'];
    email = request.form['emailValue'];
    imagen = request.files['fileValue'];

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `email`, `imagen`) VALUES (NULL, %s, %s, %s);" 
    conn = mysql.connect(); 
    cursor = conn.cursor(); 
    cursor.execute(sql, (nombre, email, imagen)); 
    conn.commit(); 
    return render_template('empleados/index.html');


if __name__ == '__main__':
    app.run(debug=True);



