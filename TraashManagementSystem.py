from flask import Flask, jsonify, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Driver, Customer, Truck, City, Employee, Routes
from datetime import datetime

app = Flask(__name__)

engine = create_engine('sqlite:///trash.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/driver/JSON')
def driverdetail():
    # restaurant = session.query(Driver).filter_by(License_No=License_no)
    items = session.query(Driver).all()
    return jsonify(Driver=[i.serialize for i in items])


@app.route('/customer/JSON')
def customerdetail():
    items = session.query(Customer).all()
    return jsonify(Customer=[i.serialize for i in items])


@app.route('/trucks/JSON')
def truckdetail():
    items = session.query(Truck).all()
    return jsonify(Truck=[i.serialize for i in items])


@app.route('/employees/JSON')
def employeesdetail():
    items = session.query(Employee).all()
    return jsonify(Truck=[i.serialize for i in items])


@app.route('/city/JSON')
def citysdetail():
    items = session.query(City).all()
    return jsonify(Truck=[i.serialize for i in items])


@app.route('/driver/new', methods=['GET', 'POST'])
def newdriver():
    args = request.args
    name = args['name']
    license_no = args['license_no']
    date = args['date']
    age = args['age']
    if request.method == 'POST':
        newD = Driver(name=name, License_No=license_no, dob=date, Age=age)
        session.add(newD)
        session.commit()
        return jsonify(Status=200)


@app.route('/customer/new', methods=['GET', 'POST'])
def newcustomer():
    # employee = session.query(Employee).filter_by(Employee_id=employee_id).one()
    args = request.args
    name = args['name']
    customer_id = args['customer_id']
    house_no = args['house_no']
    street_no = args['street_no']
    locality = args['locality']
    city = args['city']
    if request.method == 'POST':
        newD = Customer(Customer_id=customer_id, Name=name, House_No=house_no, Street_No=street_no, Locality=locality,
                        City=city)
        session.add(newD)
        session.commit()
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
    # driver = session.query(Driver).filter_by(driver_id=driver_id).one()
    if request.method == 'POST':
        newD = Truck(Model=model, Register_No=register_no, driver_id=driver_id)
        session.add(newD)
        session.commit()
        return jsonify(Status=200)
    else:
        return jsonify(Status=404)


@app.route('/employee/new', methods=['GET', 'POST'])
def newemployee():
    # employee = session.query(Employee).filter_by(Employee_id=employee_id).one()
    args = request.args
    name = args['name']
    employee_id = args['employee_id']
    gender = args['gender']
    date = args['date']
    age = args['age']
    if request.method == 'POST':
        newD = Employee(Employee_id=employee_id, Name=name, Gender=gender, dob=date, Age=age)
        session.add(newD)
        session.commit()
        E = Employee()
        R = Routes()
        E.route.append(R)
        session.add(E)
        session.commit()
        return jsonify(Status=200)
    else:
        return jsonify(Status=404)


@app.route('/route/new', methods=['GET', 'POST'])
def newroute():
    args = request.args
    Route_No = args['route_no']
    Truck_no = args['truck_no']
    City_pin = args['city_pin']
    tcheck = session.query(Truck).filter_by(Register_No=Truck_no).first()
    ccheck = session.query(City).filter_by(Pincode=City_pin).first()
    if request.method == 'POST' and tcheck != 0 and ccheck != 0:
        newD = Routes(Route_No=Route_No, Truck_No=Truck_no, city_pin=City_pin)
        session.add(newD)
        session.commit()
        return jsonify(Status=200)
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
        session.add(newD)
        session.commit()
        return jsonify(Status=200)
    else:
        return jsonify(Status=404)


@app.route('/driver/delete/<int:license_no>', methods=['GET', 'POST'])
def deletedriver(license_no):
    driver = session.query(Driver).filter_by(License_No=license_no).once()
    if request.method == 'POST':
        session.delete(driver)
        session.commit()
        return jsonify(Status=200)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
