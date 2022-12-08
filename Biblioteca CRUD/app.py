#desde aca se enruta y se hace las funcionalidades de las paginas
from flask import Flask;
from flask import render_template, request, redirect, send_from_directory, url_for;
from flaskext.mysql import MySQL;
from datetime import datetime;
import os;

app = Flask(__name__);

mysql = MySQL() 
app.config['MYSQL_DATABASE_HOST'] ="localhost"
app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD']= ''
app.config['MYSQL_DATABASE_DB'] = 'library'
app.config['MYSQL_DATABASE_PORT'] = 3308

mysql.init_app(app);

CARPETA = os.path.join("uploads");
app.config['CARPETA'] = CARPETA;

@app.route('/uploads/<nombreImg>')
def uploads(nombreImg):
    return send_from_directory(app.config['CARPETA'], nombreImg);


@app.route('/')
def main():
    sql = "SELECT * FROM books";
    conn = mysql.connect(); # se conecta a la base de datos
    cursor = conn.cursor(); #el cursor interactua con la base de datos
    cursor.execute(sql); #ejecutar consulta
    libros = cursor.fetchall();
    conn.commit(); #cerrar la operacion

    return render_template('libros/index.html', libros = libros);    
#estructura para hacer todas las rutas



@app.route('/create')
def create():
    return render_template('libros/create.html');

@app.route('/storage', methods=['POST'])
def storage():
    nombre = request.form['nombreValue'];
    anio = request.form['anioValue'];
    autor = request.form['autorValue'];
    imagen = request.files['fileValue'];

    nuevoNombreImg = '';

    if imagen.filename != '':
        now = datetime.now();
        moment = now.strftime('%Y-%M-%S');
        nuevoNombreImg = moment + "-" + imagen.filename;
        imagen.save('uploads/' + nuevoNombreImg);

    sql = "INSERT INTO `books` (`id`, `name`, `year`,  `author`, `image`) VALUES (NULL, %s, %s, %s, %s);" 
    conn = mysql.connect(); 
    cursor = conn.cursor(); 
    cursor.execute(sql, (nombre, anio, autor, nuevoNombreImg)); 
    conn.commit(); 

    return redirect('/')

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect();
    cursor = conn.cursor();
    
    cursor.execute("SELECT image FROM books WHERE id =%s", id);
    imagen = cursor.fetchall();
    os.remove(os.path.join(app.config["CARPETA"], imagen[0][0]));
    
    sql = "DELETE FROM `books` WHERE id = %s";
    cursor.execute(sql, id); 
    conn.commit();
    return redirect('/');

@app.route("/edit/<int:id>")
def edit(id):
    conn = mysql.connect();
    cursor = conn.cursor();
    cursor.execute("SELECT * FROM books WHERE id =%s", id);
    libro = cursor.fetchall();
    conn.commit();
    return render_template('libros/edit.html', libro = libro);


@app.route('/modify', methods=['POST'])
def modify():
    nombre = request.form['nombreValue'];
    anio = request.form['anioValue'];
    autor = request.form['autorValue'];
    imagen = request.files['fileValue'];
    id = request.form['idValue'];

    conn = mysql.connect(); 
    cursor = conn.cursor(); 

    nuevoNombreImg = '';

    if imagen.filename != '':
        now = datetime.now();
        moment = now.strftime('%Y-%M-%S');
        nuevoNombreImg = moment + "-" + imagen.filename;
        imagen.save('uploads/' + nuevoNombreImg);
        
        #traer la foto vieja y borrarla de uploads
        cursor.execute('SELECT image FROM books WHERE id =%s', id);
        imagen = cursor.fetchall();
        os.remove(os.path.join(app.config['CARPETA'], imagen[0][0]));

        cursor.execute('UPDATE books SET image=%s WHERE id =%s', (nuevoNombreImg, id));
        conn.commit();

    sql = "UPDATE books SET name=%s, year=%s, author=%s WHERE id =%s"; 
    
    cursor.execute(sql, (nombre, anio, autor, id)); 
    conn.commit(); 
    return redirect('/');



if __name__ == '__main__':
    app.run(debug=True);



