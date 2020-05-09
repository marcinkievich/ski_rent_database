from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dbzjemox:LzNxipSdbWaHY1jWOYP3DjX7hvUEh1xw@manny.db.elephantsql.com:5432/dbzjemox'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:karolina13@localhost/postgres'
    app.config['SECRET_KEY'] = 'secret'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Skis(db.Model):
    __tablename__ = 'skis'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    length = db.Column(db.Integer)
    softness = db.Column(db.Integer)
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean)

    def __init__(self, id, name, length, softness, price, availability):
        self.id = id
        self.name = name
        self.length = length
        self.softness = softness
        self.price = price
        self.availability = availability

class Snowboard(db.Model):
    __tablename__ = 'snowboard'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    length = db.Column(db.Integer)
    softness = db.Column(db.Integer)
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean)

    def __init__(self, id, name, length, softness, price, availability):
        self.id = id
        self.name = name
        self.length = length
        self.softness = softness
        self.price = price
        self.availability = availability

class Boots(db.Model):
    __tablename__ = 'boots'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    size = db.Column(db.Integer)
    purpose = db.Column(db.Boolean)
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean)

    def __init__(self, id, name, size, purpose, price, availability):
        self.name = name
        self.id = id
        self.size = size
        self.purpose = purpose
        self.price = price
        self.availability = availability

class Ski_poles(db.Model):
    __tablename__ = 'ski_poles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    length = db.Column(db.Integer)
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean)

    def __init__(self, id, name, length, price, availability):
        self.id = id
        self.name = name
        self.length = length
        self.price = price
        self.availability = availability

class Customers(db.Model):
    __tablename__='customers'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    surname=db.Column(db.String(50))
    eq_type=db.Column(db.Integer())
    eq_id=db.Column(db.Integer)
    def __init__(self,name,surname, eq_type, eq_id):
        self.name=name
        self.surname=surname
        self.eq_type=eq_type
        self.eq_id=eq_id



#form components
class Form(FlaskForm):
    length = SelectField('length', choices=[])
    size = SelectField('size', choices=[])
    ski_poles = SelectField('ski_poles', choices=[])
    result = SelectField('lol', choices=[])



@app.route('/', methods=['GET', 'POST'])
def index():
    #fetching data from db in order to fill select fields with many choices
    form = Form()
    form.length.choices = [(skis.length, skis.length) for skis in db.session.query(Skis).distinct('length')]
    form.size.choices = [(boots.size, boots.size) for boots in db.session.query(Boots).distinct('size')]
    form.ski_poles.choices = [(ski_poles.length, ski_poles.length) for ski_poles in db.session.query(Ski_poles).distinct('length')]





    #insert_loop_sb()
    #insert_loop()
    #insert_loop_boots()
    #insert_loop_kijki()
    return render_template('index.html', form=form)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        customers_checked=request.form.getlist('customers_checked')
        for value in range(len(customers_checked)):
            customers_deleted = Customers.query.filter_by(id=customers_checked[value]).first()
            db.session.delete(customers_deleted)
    db.session.commit()
    customers = Customers.query.all()
    return redirect(url_for('database', customers=customers))






@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        #collecting user input
        eq_type = request.form['eq_type']
        length = request.form['length']
        size = request.form['size']
        ski_poles = request.form['ski_poles']
        print(eq_type, length, size, ski_poles)
        #query for eq and extrecting its return
        if eq_type =='0':
            flash('Please choose equipment type')
            return redirect(url_for('index'))
        elif eq_type == 'ski_option':
            eq_type = '1'
            eq_list = Skis.query.filter_by(length=length, availability='true').all()
        else:
            eq_list = Snowboard.query.filter_by(length=length, availability='true').all()
        boots_list = Boots.query.filter_by(size=size, availability='true').all()
        ski_poles_list = Ski_poles.query.filter_by(length=ski_poles, availability='true').all()
        return render_template('result.html', eq_list=eq_list, boots_list=boots_list,ski_poles_list=ski_poles_list, eq_type=eq_type)

@app.route('/temp', methods=['GET', 'POST'])
def database():
    customers = Customers.query.all()
    return render_template('summary.html', customers=customers)


@app.route('/summary', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        eq_checked_list=request.form.getlist('eq_checked')
        boots_checked_list=request.form.getlist('boots_checked')
        ski_poles_checked_list=request.form.getlist('ski_poles_checked')
        name = request.form['name']
        surname = request.form['surname']
        eq_type = request.form['eq_type']
        eq_id = []
        boots_id = []
        ski_poles_id = []
        customer_list = []
        if eq_type == '1':
            for value in range(len(eq_checked_list)):
                skis_reserved = Skis.query.filter_by(id=eq_checked_list[value]).first()
                skis_reserved.availability = False
                eq_id.append(eq_checked_list[value])
                customer_list.append(Customers(name, surname, eq_type, eq_id[value]))
                db.session.add(Customers(name, surname, eq_type, eq_id[value]))
        else:
            for value in range(len(eq_checked_list)):
                snowboard_reserved = Snowboard.query.filter_by(id=eq_checked_list[value]).first()
                snowboard_reserved.availability = False
                eq_id.append(eq_checked_list[value])
                customer_list.append(Customers(name, surname, eq_type, eq_id[value]))
                db.session.add(Customers(name, surname, eq_type, eq_id[value]))

        for value in range(len(boots_checked_list)):
            boots_reserved = Boots.query.filter_by(id=boots_checked_list[value]).first()
            boots_reserved.availability = False
            boots_id.append(boots_checked_list[value])
            customer_list.append(Customers(name, surname, 3, boots_id[value]))
            db.session.add(Customers(name, surname, 3, boots_id[value]))
        for value in range(len(ski_poles_checked_list)):
            ski_poles_reserved = Ski_poles.query.filter_by(id=ski_poles_checked_list[value]).first()
            ski_poles_reserved.availability = False
            ski_poles_id.append(ski_poles_checked_list[value])
            customer_list.append(Customers(name, surname, 4, ski_poles_id[value]))
            db.session.add(Customers(name, surname, 4, ski_poles_id[value]))

        #customer = Customers(name, surname, int(eq_type), int())
        db.session.commit()
        customers = Customers.query.all()
        print(customers[1])
        refresh = False


    return redirect(url_for('delete', customers=customers))
    #return render_template('summary.html', customers=customers, refresh=refresh)

#function filling skis table
def insert_loop():
    mark = ['head', 'fischer', 'rossignol', 'atomic', 'salomon']
    send_data = []
    for j in range(5):
        for i in range(50):
            id = j * 50 + i + 1
            length = 90 + 2 * (i + 1)
            if i > 25:
                softness = (j + 1) * 2
            else:
                softness = j + 1
            if i % 5 == 0:
                price = 50 + j / 5
            availability = True
            temp = Skis(id, mark[j], length, softness, price, availability)
            send_data.append(temp)
            db.session.add(send_data[j * 50 + i])
    db.session.commit()

#function filling snowboard table
def insert_loop_sb():
    mark = ['head', 'burton', 'dc', 'raven', 'salomon']
    send_data = []
    for j in range(5):
        for i in range(50):
            id = j * 50 + i + 1
            length = 90 + 2 * (i + 1)
            if i > 25:
                softness = (j + 1) * 2
            else:
                softness = j + 1
            if i%5==0:
                price = 50 + j/5
            availability = True
            temp = Snowboard(id, mark[j], length, softness, price, availability)
            send_data.append(temp)
            db.session.add(send_data[j * 50 + i])
    db.session.commit()

#function filling boots table
def insert_loop_boots():
    mark = ['head', 'burton', 'fischer', 'salomon']
    send_data = []
    for j in range(4):
        if j > 1:
            purpose = False
        else:
            purpose = True
        for i in range(20):
            id = j * 20 + i + 1
            size = 28 + i
            if i%10==0:
                price = 15 + j/10
            availability = True
            temp = Boots(id, mark[j], size, purpose, price, availability)
            send_data.append(temp)
            db.session.add(send_data[j * 20 + i])
    db.session.commit()

#function filling ski_poles table
def insert_loop_kijki():
    mark = ['fischer', 'salomon']
    send_data = []
    for j in range(2):
        for i in range(13):
            id = j * 13 + i + 1
            length = 75 + 5 * i
            price = 10
            availability = True
            temp = Ski_poles(id, mark[j], length, price, availability)
            send_data.append(temp)
            db.session.add(send_data[j * 13 + i])
    db.session.commit()


if __name__ == '__main__':
    app.run()
