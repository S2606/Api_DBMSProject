import os

import sqlalchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bef7d95f9f1338:d8d72bdb@us-cdbr-iron-east-03.cleardb.net' \
                                        '/heroku_3f989737c82efdf'
db = SQLAlchemy(app)
heroku = Heroku(app)


# Create our database model
class Driver(db.Model):
    __tablename__ = 'Driver'

    name = db.Column(db.String(30), nullable=False)
    License_No = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.String(10))
    Age = db.Column(db.Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'license_no': self.License_No,
            'DOB': self.dob,
            'Age': self.Age
        }
        # _truck = db.relationship('Truck', uselist=False, back_populates='Driver')


# association_table2 = sqlalchemy.Table('Truck_City', db.Model.metadata,
#                                      db.Column('Truck_No', db.Integer, db.ForeignKey('Truck.Register_No')),
#                                      db.Column('City_Pin', db.Integer, db.ForeignKey('City.Pincode'))
#                                      )


class Truck(db.Model):
    __tablename__ = 'Truck'

    Model = db.Column(db.String(10), nullable=False)
    Register_No = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('Driver.License_No'))
    trash_capacity = db.Column(db.Integer, nullable=False)
    # _driver = db.relationship('Driver', back_populates='Truck')
    route = db.relationship('Routes')

    # city = db.relationship("City")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'model': self.Model,
            'Register_no': self.Register_No,
            'Driver_id': self.driver_id,
            'Trash_Capacity(in kg)': self.trash_capacity
        }


class City(db.Model):
    __tablename__ = 'City'

    Pincode = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    State = db.Column(db.String(20), nullable=False)
    # truck_id = db.Column(db.Integer, db.ForeignKey('Truck.Register_No'))
    # truck = db.relationship("Truck")
    routes = db.relationship("Routes")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Pincode': self.Pincode,
            'Name': self.Name,
            'State': self.State
        }


# association_table = db.Table('Employee_Route', db.Model.metadata,
#                             db.Column('Employee_id', db.Integer, db.ForeignKey('Employee.Employee_id')),
#                             db.Column('Route_No', db.Integer, db.ForeignKey('Routes.Route_No'))
#                             )

# association_table3 = db.Table('Customer_Route', db.Model.metadata,
#                              db.Column('Customer_id', db.Integer, db.ForeignKey('Customer.Customer_id')),
#                              db.Column('Route_No', db.Integer, db.ForeignKey('Routes.Route_No'))
#                              )


# class Truck_City(db.Model):
#    __tablename__ = 'Truck_City'

#    Truck_No = db.Column(db.Integer, db.ForeignKey('Truck.Register_No'))
#    City_Pin = db.Column(db.Integer, db.ForeignKey('City.Pincode'))


class Routes(db.Model):
    __tablename__ = 'Routes'

    Route_No = db.Column(db.Integer, primary_key=True)
    Truck_No = db.Column(db.Integer, db.ForeignKey('Truck.Register_No'))
    city_pin = db.Column(db.Integer, db.ForeignKey('City.Pincode'))
    employee = db.relationship('Employ_Route')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Route_No': self.Route_No,
            'Truck_No': self.Truck_No,
            'City_Pin': self.city_pin
        }


class Employee(db.Model):
    __tablename__ = 'Employee'

    Employee_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(10))
    Age = db.Column(db.Integer)
    customer = db.relationship('Cust_Employ')
    route = db.relationship('Employ_Route')

    # route = db.relationship("Routes",
    #                         secondary=association_table)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Employee_id': self.Employee_id,
            'Name': self.Name,
            'Gender': self.Gender,
            'dob': self.dob
        }


class Customer(db.Model):
    __tablename__ = 'Customer'

    Customer_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    House_No = db.Column(db.Integer, unique=True, nullable=False)
    Street_No = db.Column(db.Integer, unique=True, nullable=False)
    Locality = db.Column(db.String(30))
    City = db.Column(db.String(20))
    # Address = db.composite(House_No, Street_No, Locality, City)
    trash_deposited = db.Column(db.Integer, nullable=False)
    employee = db.relationship('Cust_Employ')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Customer_id': self.Customer_id,
            'Name': self.Name,
            'House No': self.House_No,
            'Street_No': self.Street_No,
            'Locality': self.Locality,
            'City': self.City,
            # 'Address': self.Address,
            'Trash_Deposited(in g)': self.trash_deposited
        }


class Cust_Employ(db.Model):
    __tablename__ = 'Cust_Employ'

    relationship_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_Id = db.Column(db.Integer, db.ForeignKey('Customer.Customer_id'))
    Employee_Id = db.Column(db.Integer, db.ForeignKey('Employee.Employee_id'))

    # customer = db.relationship('')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Customer_id': self.Customer_Id,
            # 'Employee_id': self.Employee_Id
        }


class Employ_Route(db.Model):
    __tablename__ = 'Employ_Route'

    relationship_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Employee_Id = db.Column(db.Integer, db.ForeignKey('Employee.Employee_id'))
    Route_no = db.Column(db.Integer, db.ForeignKey('Routes.Route_No'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Route_no': self.Route_no
        }


class Customer_Route(db.Model):
    __tablename__ = 'Cust_Route'

    relationship_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Customer_Id = db.Column(db.Integer, db.ForeignKey('Customer.Customer_id'))
    Route_no = db.Column(db.Integer, db.ForeignKey('Routes.Route_No'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Route_no': self.Route_no
        }


db.create_all()
db.session.commit()


# driver
@app.route('/driver/JSON')
def driverdetail():
    # restaurant = db.session.query(Driver).filter_by(License_No=License_no)
    try:
        items = db.session.query(Driver).all()
        return jsonify(Driver=[i.serialize for i in items])
    except Exception:
        return jsonify(Status=500)


@app.route('/customer/JSON')
def customerdetail():
    try:
        items = db.session.query(Customer).all()
        return jsonify(Customer=[i.serialize for i in items])
    except Exception:
        return jsonify(Status=500)


@app.route('/trucks/JSON')
def trucksdetail():
    try:
        items = db.session.query(Truck).all()
        return jsonify(Truck=[i.serialize for i in items])
    except Exception:
        return jsonify(Status=500)


@app.route('/employees/JSON')
def employeesdetail():
    try:
        items = db.session.query(Employee).all()
        return jsonify(Employee=[i.serialize for i in items])
    except Exception:
        return jsonify(Status=500)


@app.route('/city/JSON')
def citysdetail():
    try:
        items = db.session.query(City).all()
        return jsonify(City=[i.serialize for i in items])
    except Exception:
        return jsonify(Status=500)


@app.route('/empl_cus/JSON', methods=['GET', 'POST'])
def emplcusdetail():
    args = request.args
    name = args['employee_id']
    if request.method == 'POST':
        try:
            items = db.session.query(Cust_Employ).filter_by(Employee_Id=name).all()
            return jsonify(Cust_Employ=[i.serialize for i in items])
        except Exception:
            return jsonify(Status=500)


@app.route('/empl_route/JSON', methods=['GET', 'POST'])
def emplroutedetail():
    args = request.args
    name = args['employee_id']
    if request.method == 'POST':
        try:
            items = db.session.query(Employ_Route).filter_by(Employee_Id=name).all()
            return jsonify(Employ_Route=[i.serialize for i in items])
        except Exception:
            return jsonify(Status=500)


@app.route('/route_empl/JSON', methods=['GET', 'POST'])
def routeempldetail():
    args = request.args
    name = args['route_no']
    if request.method == 'POST':
        try:
            items = db.session.query(Employ_Route).filter_by(Route_no=name).all()
            return jsonify(Employ_Route=[i.serialize for i in items])
        except Exception:
            return jsonify(Status=500)


@app.route('/cust_route/JSON', methods=['GET', 'POST'])
def custroutedetail():
    args = request.args
    name = args['customer_id']
    if request.method == 'POST':
        try:
            items = db.session.query(Customer_Route).filter_by(Customer_Id=name).all()
            return jsonify(Cust_Route=[i.serialize for i in items])
        except Exception:
            return jsonify(Status=500)


@app.route('/route_cust/JSON', methods=['GET', 'POST'])
def routecustdetail():
    args = request.args
    name = args['route_no']
    if request.method == 'POST':
        try:
            items = db.session.query(Customer_Route).filter_by(Route_no=name).all()
            return jsonify(Cust_Route=[i.serialize for i in items])
        except Exception:
            return jsonify(Status=500)


@app.route('/driver/new', methods=['GET', 'POST'])
def newdriver():
    args = request.args
    name = args['name']
    license_no = args['license_no']
    date = args['date']
    age = args['age']
    if request.method == 'POST':
        try:
            newD = Driver(name=name, License_No=license_no, dob=date, Age=age)
            db.session.add(newD)
            db.session.commit()
            return jsonify(Status=200)
        except Exception:
            return jsonify(Status=500)


@app.route('/customer/new', methods=['GET', 'POST'])
def newcustomer():
    # employee = db.session.query(Employee).filter_by(Employee_id=employee_id).one()
    args = request.args
    name = args['name']
    customer_id = args['customer_id']
    house_no = args['house_no']
    street_no = args['street_no']
    locality = args['locality']
    city = args['city']
    tdep = args['trash_dep']
    if request.method == 'POST':
        newD = Customer(Customer_id=customer_id, Name=name, House_No=house_no, Street_No=street_no,
                        Locality=locality,
                        City=city, trash_deposited=tdep)
        db.session.add(newD)
        db.session.commit()
        return jsonify(Status=200)
    else:
        return jsonify(Status=404)


@app.route('/truck/new',
           methods=['GET', 'POST'])
def newtruck():
    args = request.args
    model = args['model']
    register_no = args['reg_no']
    driver_id = args['driver_id']
    tcap = args['trash_cap']
    # driver = db.session.query(Driver).filter_by(driver_id=driver_id).one()
    if request.method == 'POST':
        try:
            newD = Truck(Model=model, Register_No=register_no, driver_id=driver_id, trash_capacity=tcap)
            db.session.add(newD)
            db.session.commit()
            return jsonify(Status=200)
        except Exception:
            return jsonify(Status=500)
    else:
        return jsonify(Status=404)


@app.route('/employee/new', methods=['GET', 'POST'])
def newemployee():
    # employee = db.session.query(Employee).filter_by(Employee_id=employee_id).one()
    args = request.args
    name = args['name']
    employee_id = args['employee_id']
    gender = args['gender']
    date = args['date']
    age = args['age']
    if request.method == 'POST':
        try:
            newD = Employee(Employee_id=employee_id, Name=name, Gender=gender, dob=date, Age=age)
            db.session.add(newD)
            db.session.commit()
            # E = Employee()
            # R = Routes()
            # E.route.append(R)
            # db.session.add(E)
            # db.session.commit()
            return jsonify(Status=200)
        except Exception:
            return jsonify(Status=500)
    else:
        return jsonify(Status=404)


@app.route('/route/new', methods=['GET', 'POST'])
def newroute():
    args = request.args
    Route_No = args['route_no']
    Truck_no = args['truck_no']
    City_pin = args['city_pin']
    Employ_Id = args['emp_id']
    tcheck = db.session.query(Truck).filter_by(Register_No=Truck_no).first()
    ccheck = db.session.query(City).filter_by(Pincode=City_pin).first()
    echeck = db.session.query(Employee).filter_by(Employee_id=City_pin).first()
    if request.method == 'POST' and tcheck != 0 and ccheck != 0 and echeck !=0:
        try:
            newD = Routes(Route_No=Route_No, Truck_No=Truck_no, city_pin=City_pin)
            db.session.add(newD)
            newE = Employ_Route(Employee_Id=Employ_Id, Route_no=Route_No)
            db.session.add(newE)
            db.session.commit()
            return jsonify(Status=200)
        except Exception:
            return jsonify(Status=500)
    else:
        return jsonify(Status=404)


@app.route('/city/new', methods=['GET', 'POST'])
def newcity():
    args = request.args
    pincode = args['pin']
    name = args['name']
    state = args['state']
    if request.method == 'POST':
        newD = City(Pincode=pincode, Name=name, State=state)
        db.session.add(newD)
        db.session.commit()
        return jsonify(Status=200)
    else:
        return jsonify(Status=404)


@app.route('/cust-empl/new', methods=['GET', 'POST'])
def addcustempl():
    args = request.args
    city_pin = args['cpin']
    empl_pin = args['epin']
    ccheck = db.session.query(Customer).filter_by(Customer_id=city_pin).first()
    echeck = db.session.query(Employee).filter_by(Employee_id=empl_pin).first()
    if request.method == 'POST' and ccheck != 0 and echeck != 0:
        try:
            newC = Cust_Employ(city_pin, empl_pin)
            db.session.add(newC)
            db.session.commit()
            return jsonify(Status=200)
        except Exception:
            return jsonify(Sattus=500)
    else:
        return jsonify(Status=404)


@app.route('/cust-empl/check', methods=['GET', 'POST'])
def checkcustempl():
    args = request.args
    cpin = args['cpin']
    epin = args['epin']
    try:
        ccheck = db.session.query(Cust_Employ).filter_by(Customer_Id=cpin, Employee_Id=epin).first()
        if request.method == 'POST' and ccheck != 0:
            return jsonify(Status=200)
        else:
            return jsonify(Status=404)
    except Exception:
        return jsonify(Status=500)


@app.route('/empl-route/new', methods=['GET', 'POST'])
def addemplroute():
    args = request.args
    # city_pin = args['cpin']
    empl_pin = args['epin']
    route_no = args['rno']
    ccheck = db.session.query(Routes).filter_by(Route_No=route_no).first()
    echeck = db.session.query(Employee).filter_by(Employee_id=empl_pin).first()
    if request.method == 'POST' and ccheck != 0 and echeck != 0:
        try:
            newC = Cust_Employ(empl_pin, route_no)
            db.session.add(newC)
            db.session.commit()
            return jsonify(Status=200)
        except Exception:
            return jsonify(Sattus=500)
    else:
        return jsonify(Status=404)


@app.route('/empl-route/check', methods=['GET', 'POST'])
def checkemplroute():
    args = request.args
    empl_pin = args['epin']
    try:
        ccheck = db.session.query(Employ_Route).filter_by(Employee_Id=empl_pin).first()
        if request.method == 'POST' and ccheck is not None:
            return jsonify(Status=200)
        else:
            return jsonify(Status=404)
    except Exception:
        return jsonify(Status=500)


@app.route('/driver/delete', methods=['GET', 'POST'])
def deletedriver():
    args = request.args
    cpin = args['license_no']
    try:
        driver = db.session.query(Driver).filter_by(License_No=cpin).first()
        if request.method == 'POST':
            db.session.delete(driver)
            db.session.commit()
            return jsonify(Status=200)
    except Exception:
        return jsonify(Status=500)


@app.route('/truck/delete', methods=['GET', 'POST'])
def deletetruck():
    args = request.args
    cpin = args['registration_no']
    try:
        truck = db.session.query(Truck).filter_by(Register_No=cpin).first()
        if request.method == 'POST':
            db.session.delete(truck)
            db.session.commit()
            return jsonify(Status=200)
    except Exception:
        return jsonify(Status=500)


@app.route('/route/delete', methods=['GET', 'POST'])
def deleteroute():
    args = request.args
    cpin = args['route_no']
    try:
        truck = db.session.query(Routes).filter_by(Route_No=cpin).first()
        if request.method == 'POST':
            db.session.delete(truck)
            db.session.commit()
            return jsonify(Status=200)
    except Exception:
        return jsonify(Status=500)


@app.route('/truck/edit', methods=['GET', 'POST'])
def edittruck():
    args = request.args
    register_no = args['reg_no']
    driver_id = args['driver_id']
    occupieddriver = db.session.query(Truck).filter_by(driver_id=driver_id).first()
    editedtruck = db.session.query(Truck).filter_by(Register_No=register_no).first()
    if request.method == 'POST':
        if occupieddriver is None and editedtruck is not None:
            editedtruck.driver_id = driver_id
            db.session.add(editedtruck)
            db.session.commit()
            return jsonify(Status=200)
        elif occupieddriver is not None and editedtruck is not None:
            occupieddriver.driver_id = 1
            editedtruck.driver_id = driver_id
            db.session.add(occupieddriver)
            db.session.add(editedtruck)
            db.session.commit()
            return jsonify(Status=200)
        else:
            return jsonify(Truck='Does not exist')
    else:
        return jsonify(Status=404)


@app.route('/cust/trash', methods=['GET', 'POST'])
def trascollect():
    args = request.args
    cus = args['cus_id']
    trash = args['trash']
    occupiedriver = db.session.query(Customer).filter_by(Customer_id=cus).one()
    if request.method == 'POST':
        if occupiedriver is not None:
            t = occupiedriver.trash_deposited
            t += int(trash)
            occupiedriver.trash_deposited = t
            db.session.add(occupiedriver)
            db.session.commit()
            return jsonify(Trash=200)
        elif occupiedriver is None:
            return jsonify(Trash=404)
    else:
        return jsonify(Driver=404)


@app.route('/trash_stats', methods=['GET', 'POST'])
def trashstat():
    args = request.args
    cus = args['cus_id']
    try:
        cust = db.session.query(Customer).filter_by(Customer_id=cus).first()
        sum = 0
        if request.method == 'POST':
            sum += int(cust.trash_deposited)
        return jsonify(Total_trash=sum)
    except Exception:
        return jsonify(Status=500)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
