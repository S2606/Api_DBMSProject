import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import DateTime
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, composite, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


class Driver(Base):
    __tablename__ = 'Driver'

    name = Column(String(30), nullable=False)
    License_No = Column(Integer, primary_key=True)
    dob = Column(String(10))
    Age = Column(Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'license_no': self.License_No,
            'DOB': self.dob,
            'Age': self.Age
        }
        # _truck = relationship('Truck', uselist=False, back_populates='Driver')


association_table2 = Table('Truck_City', Base.metadata,
                           Column('Truck_No', Integer, ForeignKey('Truck.Register_No')),
                           Column('City_Pin', Integer, ForeignKey('City.Pincode'))
                           )


class Truck(Base):
    __tablename__ = 'Truck'

    Model = Column(String(10), nullable=False)
    Register_No = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('Driver.License_No'))
    # _driver = relationship('Driver', back_populates='Truck')
    route = relationship('Routes')
    city = relationship("City",
                        secondary=association_table2)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'model': self.Model,
            'Register_no': self.Register_No,
            'Driver_id': self.driver_id
        }


class City(Base):
    __tablename__ = 'City'

    Pincode = Column(Integer, primary_key=True)
    Name = Column(String(20), nullable=False)
    State = Column(String(20), nullable=False)
    # truck_id = Column(Integer, ForeignKey('Truck.Register_No'))
    # truck = relationship("Truck")
    routes = relationship("Routes")


association_table = Table('Employee_Route', Base.metadata,
                          Column('Employee_id', Integer, ForeignKey('Employee.Employee_id')),
                          Column('Route_No', Integer, ForeignKey('Routes.Route_No'))
                          )

association_table3 = Table('Customer_Route', Base.metadata,
                           Column('Customer_id', Integer, ForeignKey('Customer.Customer_id')),
                           Column('Route_No', Integer, ForeignKey('Routes.Route_No'))
                           )


class Routes(Base):
    __tablename__ = 'Routes'

    Route_No = Column(Integer, primary_key=True)
    Truck_No = Column(Integer, ForeignKey('Truck.Register_No'))
    city_pin = Column(Integer, ForeignKey('City.Pincode'))


class Employee(Base):
    __tablename__ = 'Employee'

    Employee_id = Column(Integer, primary_key=True)
    Name = Column(String(20), nullable=False)
    Gender = Column(String(10), nullable=False)
    dob = Column(String(10))
    Age = Column(Integer)
    route = relationship("Routes",
                         secondary=association_table)


class Customer(Base):
    __tablename__ = 'Customer'

    Customer_id = Column(Integer, primary_key=True)
    Name = Column(String(20), nullable=False)
    House_No = Column(Integer, primary_key=True)
    Street_No = Column(Integer, primary_key=True)
    Locality = Column(String(30))
    City = Column(String(20))
    Address = composite(House_No, Street_No, Locality, City)
    # employee_id = Column(Integer, ForeignKey('Employee.Employee_id'))
    # employee = relationship("Employee")
    route = relationship("Routes",
                         secondary=association_table3)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'Customer_id': self.Customer_id,
            'Name': self.Name,
            'Address': self.Address
        }


engine = create_engine('sqlite:///trash.db')
Base.metadata.create_all(engine)
