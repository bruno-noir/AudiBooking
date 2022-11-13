# AudiBooking
An auditorium management software based on Python Flask.

## Dependencies
1. flask
    `pip3 install flask`
2. flask_sqlalchemy
    `pip3 install flask_sqlalchemy`
3. flask_wtf
    `pip3 install flask_wtf`
4. Setup Python virtual environment

## Notes
This software runs on local machine and supports three categories of users: *Managers*, *Salespeople* and *Accounts Clerks*.
OTP based login is supported. The default email address of manager is set as: *manager.officer.12345@gmail.com*. This manager can create other employees who can have their own email IDs. To change the manager's email address, open a terminal window in the folder containing the project and run the following:
1. `python -i`
2. `from app import db`
3. `db.create_all()`
4. `from app import Employee`
5. `x = Employee(username='FooBar', email='foobar@gmail.com', password='12345678abcd', portfolio='Manager')`
6. `db.session.add(x)`
7. `db.session.commit()`

## Screenshots
1. ![login](/Screenshots/login.png)
2. ![manager dashboard](/Screenshots/manager%20dashboard.png)
3. ![balance sheet for show](/Screenshots/balance%20sheet%20for%20show.png)
4. ![choose show](/Screenshots/choose%20show.png)
5. ![create show](/Screenshots/create%20show.png)
6. ![book ticket](/Screenshots/book%20ticket.png)
7. ![book tickets](/Screenshots/book%20tickets.png)
