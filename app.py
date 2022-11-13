from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import Login, Register, AddExpenses, Show, SearchShow, OTP
from datetime import datetime, date
import smtplib
import random                                                                       #important imports
app = Flask(__name__)

app.config['SECRET_KEY'] = ''                                                       #secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'                         #defining database file

db = SQLAlchemy(app)

class Employee(db.Model):                                                           #declaring a Employee Class
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    portfolio = db.Column(db.String(15), nullable=False)
    def __repr__(self):
        return f"Employee('{self.username}', '{self.email}', '{self.password}', '{self.portfolio}')"

class Transactions(db.Model):                                                       #declaring a Transactions Class
    id = db.Column(db.Integer, primary_key=True)
    salesperson_id = db.Column(db.Integer, nullable=False)
    time_of_transaction = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    show_id = db.Column(db.Integer, nullable=False)
    ttype = db.Column(db.String(7), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Transactions('{self.id}', '{self.salesperson_id}', '{self.show_id}', '{self.ttype}', '{self.amount}', '{self.time_of_transaction}')"

class Expenses(db.Model):                                                           #declaring a Expenses Class
    id = db.Column(db.Integer, primary_key=True)
    accounts_clerk_id = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(100))
    expenses = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    def __repr__(self):
        return f"Expenses('{self.id}', '{self.accounts_clerk_id}', '{self.show_id}', '{self.details}', '{self.expenses}', '{self.date}')"

class Shows(db.Model):                                                              #declaring a Shows Class
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    ordinary_seats = db.Column(db.Integer, nullable=False)
    o_price = db.Column(db.Integer, nullable=False)
    balcony_seats = db.Column(db.Integer, nullable=False)
    b_price = db.Column(db.Integer, nullable=False)
    b_seats = db.Column(db.JSON, nullable=False)
    o_seats = db.Column(db.JSON, nullable=False)
    def __repr__(self):
        return f"Shows('{self.id}','{self.name}', '{self.date}', '{self.start_time}', '{self.end_time}')"

@app.route('/', methods=['GET','POST'])                                             #app route for home page
def home():
    form = Login()                                                                  #form to get login details
    if form.validate_on_submit():
        e_list_size = len(Employee.query.filter_by(username=form.username.data).filter_by(password=form.password.data).all())
        if e_list_size != 0:
            _data = Employee.query.filter_by(username=form.username.data).first()
            return redirect("/otp/" + str(_data.id))
        else:
            flash(f'Invalid Login! Please enter valid credentials.','danger')
    return render_template("home.html", form=form, is_home=True)
otp = -1
@app.route('/otp/<int:id>', methods=['GET','POST'])
def otp(id):
    global otp
    form = OTP()                                                                        #form to collect OTP details and validate them
    if form.validate_on_submit():
        if form.otp.data == str(otp):
            portfolio_ = Employee.query.filter_by(id=id).first().portfolio
            if portfolio_ == 'Salesperson':
                return redirect('/salesperson/' + str(id))
            elif portfolio_ == 'AccountsClerk':
                return redirect('/accounts_clerk/' + str(id))
            else:
                return redirect('/manager/' + str(id))
        else:
            flash(f'Incorrect OTP! Please enter valid credentials.','danger')
    else:
        otp = random.randrange(100000, 1000000)                                         #generate a random 6 digit OTP on fresh generation of page
        email = Employee.query.filter_by(id=id).first().email
        message = "Your Login OTP for the SAMS website is " + str(otp)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("samsqwertyemail@gmail.com", "QWERTY@12345")
        server.sendmail("samsqwertyemail@gmail.com", email, message)
    return render_template("otp.html", form=form, is_home=True)

@app.route('/manager/<int:id>', methods=['GET','POST'])                                 #app route for manager dashboard
def manager(id):
    return render_template("manager.html", data=Employee.query.filter_by(id=id).first())

@app.route('/register/<string:portfolio_>/<int:id>', methods=['GET','POST'])            #app route for registering employee
def register(portfolio_,id):
    form = Register()
    if form.validate_on_submit():
        user = Employee(username=form.username.data, email=form.email.data, password=form.password.data, portfolio=portfolio_)             #storing Employee details in database
        db.session.add(user)
        try:
            db.session.commit()
            flash(f'Account Created!!!','success')
            return redirect('/manager/' + str(id))
        except:
            db.session.rollback()
            flash(f'Username already exists!!!','danger')
    return render_template("register.html", form=form)

@app.route('/accounts_clerk/<int:id>', methods=['GET','POST'])                          #app route for Clerk dashboard
def accounts_clerk(id):
    return render_template("accounts_clerk.html", data=Employee.query.filter_by(id=id).first())

@app.route('/salesperson/<int:id>', methods=['GET','POST'])                             #app route for Salesperson dashboard
def salesperson(id):
    return render_template("salesperson.html", data=Employee.query.filter_by(id=id).first())

@app.route('/seat_details/0/<int:show_id>', methods=['GET','POST'])                     #app route for getting seats for Shows
def seat_details(show_id):
    show = Shows.query.filter_by(id=show_id).first()
    return render_template("seat_details.html", is_home=True, show=show, show_id=show_id)

@app.route('/SeatOccupancy/<int:id>/<int:show_id>')                                     #app route for getting details of seat occupancy of selected show
def SeatOccupancy(id, show_id):
    show=Shows.query.filter_by(id=show_id).first()                                      #filtering show database by given show id
    o_seat = show.ordinary_seats
    b_seat = show.balcony_seats
    o_av = 0
    b_av = 0
    for i in show.o_seats:
        if i == 1:
            o_av = o_av + 1
    for i in show.b_seats:
        if i == 1:
            b_av = b_av + 1
    o_pc = o_av * 100 / o_seat
    b_pc = b_av * 100 / b_seat
    o_pc = round(o_pc,2)
    b_pc = round(b_pc,2)
    return render_template("seat_occupancy.html", id=id, show_id=show_id, o_pc=o_pc, b_pc=b_pc)

@app.route('/CreateShow/<int:id>', methods=['GET','POST'])                               #app route for creating a new show
def CreateShow(id):
    add = Show()
    if add.validate_on_submit():
        o_occupied=[]
        b_occupied=[]
        for i in range(add.ordinary_seats.data):
            o_occupied.append(0)
        for i in range(add.balcony_seats.data):
            b_occupied.append(0)
        if add.start_time.data >= add.end_time.data:
            flash(f'Start time should be before End time!!!','danger')
        else:
            show = Shows(name=add.name.data, date=add.date.data, start_time=add.start_time.data, end_time=add.end_time.data,
                        ordinary_seats=add.ordinary_seats.data, balcony_seats=add.balcony_seats.data, o_price=add.o_price.data,
                        b_price=add.b_price.data, o_seats=o_occupied, b_seats=b_occupied)
            db.session.add(show)
            db.session.commit()                                                           #adding show details to database
            return redirect('/manager/' + str(id))
    return render_template("create_show.html", form=add)

@app.route('/Transactions/<int:id>', methods=['GET','POST'])                              #app route for checking transactions by desired salesperson through salesperson ID
def TransactionRecords(id):
    if request.form.get("Salesperson_ID") == "" or request.form.get("commission_rate") == "":
        flash(f'Input is required!!!','danger')
        return redirect('/manager/' + str(id))
    transaction_data = Transactions.query.filter_by(salesperson_id=request.form.get("Salesperson_ID")).all()        #filtering Transactions by salesperson ID
    commission_rate = float(request.form.get("commission_rate"))
    sales = 0
    for _data in transaction_data:
        if _data.ttype == "book":
            sales = sales + _data.amount
    commission = sales * commission_rate / 100
    return render_template("transaction_records.html", data=transaction_data, commission=commission)

@app.route('/AnnualBalanceSheet/<int:id>', methods=['GET','POST'])                        #app route for getting annual balance sheet of auditorium
def AnnualBalanceSheet(id):                                                               #function filters data by year
    if request.form.get("annual_balance") == "":
        flash(f'Input is required!!!','danger')
        return redirect('/manager/' + str(id))
    year = int(request.form.get("annual_balance"))
    data1 = Transactions.query.filter(Transactions.time_of_transaction>=datetime(year,1,1,0,0,0),Transactions.time_of_transaction<=datetime(year,12,31,23,59,59)).all()
    data2 = Expenses.query.filter(Expenses.date>=date(year,1,1),Expenses.date<=date(year,12,31)).all()
    return render_template("annual_balance_sheet.html", data1=data1, data2=data2)

@app.route('/ShowBalanceSheet/<int:id>', methods=['GET','POST'])                                 #app route to get balance sheet of selected show
def ShowBalanceSheet(id):
    if request.form.get("show_balance") == "":
        flash(f'Input is required!!!','danger')
        return redirect('/manager/' + str(id))
    show_id = int(request.form.get("show_balance"))
    data = Transactions.query.filter_by(show_id=show_id).all()
    return render_template("show_balance_sheet.html", show_id=show_id, data=data)

@app.route('/EnterExpenses/<int:id>/<int:show_id>', methods=['GET','POST'])             #app route for entering expenses for show
def EnterExpenses(id, show_id):
    add = AddExpenses()
    if add.validate_on_submit():
        expense = Expenses(accounts_clerk_id=id, details=add.details.data, expenses=add.amount.data, show_id=show_id)       #storing expense for show in database
        db.session.add(expense)
        db.session.commit()
        return redirect('/accounts_clerk/' + str(id))
    return render_template("enter_expenses.html", form=add, id=id)

@app.route('/show_book/<int:user>/<int:show>/<string:seat>/<int:id>', methods=['GET','POST'])
def show_book(user,show,seat,id):                                                      #shows the temporary booking (denoted by 2) in yellow
    change_seat = Shows.query.filter_by(id=show).first()
    if seat == "o":
        data = list(change_seat.o_seats)
        if data[id] == 0:
            data[id] = 2
        elif data[id] == 2:                                                             #reselecting the yellow revertss the choice
            data[id] = 0
        change_seat.o_seats = data
        db.session.commit()
    else:
        data = list(change_seat.b_seats)
        if data[id] == 0:
            data[id] = 2
        elif data[id] == 2:
            data[id] = 0
        change_seat.b_seats = data
        db.session.commit()
    return redirect('/BookTickets/' + str(user) + '/' + str(show))

@app.route('/show_cancel/<int:user>/<int:show>/<string:seat>/<int:id>', methods=['GET','POST'])
def show_cancel(user,show,seat,id):                                                     #shows the temporary booking (denoted by 3) in yellow
    change_seat = Shows.query.filter_by(id=show).first()
    if seat == "o":
        data = list(change_seat.o_seats)
        if data[id] == 1:
            data[id] = 3
        elif data[id] == 3:                                                             #reselecting the yellow revertss the choice
            data[id] = 1
        change_seat.o_seats = data
        db.session.commit()
    else:
        data = list(change_seat.b_seats)
        if data[id] == 1:
            data[id] = 3
        elif data[id] == 3:
            data[id] = 1
        change_seat.b_seats = data
        db.session.commit()
    return redirect('/CancelTickets/' + str(user) + '/' + str(show))

@app.route('/book/<int:id>/<int:show_id>', methods=['GET','POST'])                                  #app route for seat booking
def book(id,show_id):
    show = Shows.query.filter_by(id=show_id).first()
    o_seat = 0
    b_seat = 0
    olist = []                                                          #list for storing the indexes of booked ordinary seats
    blist = []                                                          #list for storing the indexes of booked balcony seats
    date = datetime.now()
    data = list(show.o_seats)
    for i in range(len(show.o_seats)):                                  #loop check for ordinary seats
        if data[i] == 2:
            data[i] = 1
            olist.append(i)
            o_seat = o_seat + 1
    show.o_seats = data
    db.session.commit()
    data = list(show.b_seats)
    for i in range(len(show.b_seats)):                                  #loop check for balcony seats
        if data[i] == 2:
            data[i] = 1
            blist.append(i)
            b_seat = b_seat + 1
    show.b_seats = data
    db.session.commit()
    if o_seat == 0 and b_seat == 0:                                     #no seats booked
        return redirect('/salesperson/' + str(id))
    amount = o_seat * show.o_price + b_seat * show.b_price
    transaction = Transactions(salesperson_id=id, ttype="book", amount=amount, show_id=show_id)
    db.session.add(transaction)
    db.session.commit()
    return render_template("ticket.html", id=id, show=Shows.query.filter_by(id=show_id).first(), amount=amount, type_='book',
                            olist=olist, blist=blist, today_date=date)

@app.route('/cancel/<int:id>/<int:show_id>', methods=['GET','POST'])                                    #app route for seat cancelling
def cancel(id,show_id):
    show = Shows.query.filter_by(id=show_id).first()
    o_seat = 0
    b_seat = 0
    olist = []                                                          #list for storing the indexes of cancelled ordinary seats
    blist = []                                                          #list for storing the indexes of cancelled bay seats
    date = datetime.now()
    data = list(show.o_seats)
    for i in range(len(show.o_seats)):
        if data[i] == 3:
            data[i] = 0
            olist.append(i)
            o_seat = o_seat + 1
    show.o_seats = data
    db.session.commit()
    data = list(show.b_seats)
    for i in range(len(show.b_seats)):
        if data[i] == 3:
            data[i] = 0
            blist.append(i)
            b_seat = b_seat + 1
    show.b_seats = data
    db.session.commit()
    if o_seat == 0 and b_seat == 0:
        return redirect('/salesperson/' + str(id))
    amount = o_seat * show.o_price + b_seat * show.b_price
    day_gap = (datetime.utcnow().date() - show.date).days
    if day_gap > 4:
        amount = amount - 5 * (o_seat + b_seat)
    elif day_gap == 1 or day_gap == 0:
        amount = amount / 2
    else:
        amount = amount - 10 * o_seat - 15 * b_seat
    transaction = Transactions(salesperson_id=id, ttype="cancel", amount=amount, show_id=show_id)
    db.session.add(transaction)
    db.session.commit()
    return render_template("ticket.html", id=id, show=Shows.query.filter_by(id=show_id).first(), amount=amount, type_='cancel',
                            olist=olist, blist=blist, today_date=date)

@app.route('/BookTickets/<int:id>/<int:show_id>', methods=['GET','POST'])                           #app route for book ticket page
def BookTickets(id, show_id):
    show = Shows.query.filter_by(id=show_id).first()
    return render_template("book_tickets.html", id=id, show_id=show_id, show=show)

@app.route('/CancelTickets/<int:id>/<int:show_id>', methods=['GET','POST'])                         #app route for cancel ticket page
def CancelTickets(id, show_id):
    show = Shows.query.filter_by(id=show_id).first()
    return render_template("cancel_tickets.html", id=id, show_id=show_id, show=show)

@app.route('/<string:task>/ChooseShow/<int:id>', methods=['GET','POST'])                            #app route for choosing show
def ChooseShow(task, id):
    show = SearchShow()
    if request.method == 'POST':
        if show.validate_on_submit():
            show_new = Shows.query.filter(Shows.name.contains(show.show_name.data)).order_by(Shows.date.desc()).all()
            return render_template("choose_show.html", shows=show_new, show=show, task=task, id=id)
    else:
        shows = Shows.query.order_by(Shows.date.desc()).all()
    return render_template("choose_show.html", shows=shows, show=show, task=task, id=id)
