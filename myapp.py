#!/usr/bin/python3
import sys
from flask import Flask,render_template, request
from flaskext.mysql import MySQL


app = Flask(__name__)

'''
Configuration required to access to MySQL database server
'''
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'flaskapp'
app.config['MYSQL_DATABASE_PORT']=3306

mysql = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
    '''
    Depending on whether the application receives a POST or a GET request it will proceed differently if a POST request is received the application will attempt to store 
    the information provided on index.html into the database and then proceed to show the user the success.html if the information was correctly stored into the database,
    on the other hand if a GET request is received it will show index.html to the user.
    '''

    if request.method == "POST":
        #print (app.config)
        details = request.form
        name = details['Name']
        color = details['FavColor']
        animal = details['CatDog']
        print(app.config)
        print (name)
        cursor = mysql.get_db().cursor()
        cursor.execute("INSERT INTO Data(Name,Favorite_Color,CatOrDog)  VALUES (%s, %s, %s)", (name, color, animal))
        mysql.get_db().commit()
        cursor.close()
        return render_template('success.html')
    return render_template('index.html')

'''
    If there is any error with the database and an Internal Server Error is created the following code will render error.html to let the user know about this and let him go
    back to index.html
'''

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
