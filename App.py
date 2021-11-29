
from flask import Flask, render_template,request,redirect , url_for, flash
from flask_sqlalchemy import SQLAlchemy
# import sqlite3
# import os

#create the object of Flask
# app  = Flask(__name__)

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///topper.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#MYSQL database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/crud'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#create a sql alchemy object and pass app
db= SQLAlchemy(app)
#Here the database connection is completed

#create Table model
class Data(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    phone=db.Column(db.String(100))

    def __init__(self,name,email,phone):
        self.name=name
        self.email=email
        self.phone=phone


 
#creating our routes
@app.route('/')
def Index():
    all_data=Data.query.all()
    return render_template("index.html",employees=all_data)
    
 


@app.route('/insert',methods=['POST'])
def insert():
    if request.method =='POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']

        my_data = Data(name,email,phone)
        db.session.add(my_data)
        db.session.commit()

        flash("New Employee Inserted Successfully")
        
        return redirect(url_for('Index'))

@app.route('/update', methods=['GET','POST'])
def update():
    if request.method=='POST':
        my_data=Data.query.get(request.form.get('id'))
        my_data.name=request.form['name']
        my_data.email=request.form['email']
        my_data.phone=request.form['phone']

        db.session.commit()
        flash("Employee Details Updated Successfully")
        return redirect(url_for('Index'))

@app.route('/delete/<id>/',methods=['GET','POST'])
def delete(id):
    my_data=Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('Index'))

 
#run flask app
if __name__ == "__main__":
    app.run(debug=True)