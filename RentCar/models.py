'''
Table Creation in AWS DB
Author: Pooja Patil
'''

from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.dialects.postgresql import JSON
import datetime as dt
from RentCar import app, db, login_manager
from flask_login import UserMixin
from sqlalchemy import exc, and_, Sequence
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class user(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15),unique=True)
	fname = db.Column(db.String(15), nullable=False)
	lname = db.Column(db.String(15), nullable=False)
	email = db.Column(db.String(20),unique=True)
	passowrd = db.Column(db.String(10),nullable=False)
	age = db.Column(db.Integer,nullable=False)
	driverId = db.Column(db.Integer,nullable=False)
	driverValidity = db.Column(db.String(15),nullable=False)
	address = db.Column(db.String(100))

	def __init__(self, username, fname, lname, email, passowrd, age, driverId, address, driverValidity):
		self.username = username
		self.fname = fname
		self.lname = lname
		self.email = email
		self.passowrd = passowrd
		self.age = age
		self.driverId = driverId
		self.driverValidity = driverValidity
		self.address = address

	def __repr__(self):
		return '<{} {} {} {} {} {} {} {} {} {}>'.format(self.id, self.username,
					self.fname, self.lname, self.email, self.passowrd, self.age, self.driverId, self.driverValidity, self.address)

	def is_active(self):
		"""True, as all users are active."""
		return True

	def get_id(self):
		"""Return the email address to satisfy Flask-Login's requirements."""
		return self.email

	def is_authenticated(self):
		"""Return True if the user is authenticated."""
		return self.authenticated

	def is_anonymous(self):
		"""False, as anonymous users aren't supported."""
		return False

	@classmethod
	def addRow(cls, UserObj):
		try:
			print('addrow '+str(UserObj))
			db.session.add(UserObj)
		except exc.SQLAlchemyError:
			print("add error")
			pass
		try:
			app.logger.info(UserObj.id)
			db.session.commit()
		except exc.SQLAlchemyError:
			print("commit error")
			pass

	@classmethod
	def removeUser(cls, userName):
		try:
			db.session.query(user).filter(user.username == userName).delete()
			db.session.commit()
		except exc.SQLAlchemyError:
			pass
	
	@classmethod
	def listUser(cls):
		try:
			result = db.session.query(user).all()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def isUserExist(cls, username):
		exists = False
		try:
			exists = db.session.query(user.username).filter_by(username=username).scalar() is not None
			return exists
		except exc.SQLAlchemyError:
			print("User doesn't exists")
			pass
		return exists

	@classmethod
	def isEmailExist(cls, email):
		exists = False
		try:
			exists = db.session.query(user.email).filter_by(email=email).scalar() is not None
			return exists
		except exc.SQLAlchemyError:
			print("email query error")
			pass
		return exists


	@classmethod
	def getPassword(cls, email):
		result = ""
		try:
			#exists = db.session.query(user.passowrd).filter_by(username=username).scalar() is not None
			result = db.session.query(user.passowrd).filter_by(email=email).scalar()
		except exc.SQLAlchemyError:
			print("getPassword Error")
			pass
		return result

	@classmethod
	def getUsername(cls, email):
		result = ""
		try:
			result = db.session.query(user.username).filter_by(email=email).scalar()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def getRow(cls, email):
		row = None
		try:
			row = db.session.query(user).filter_by(email=email).first()
		except exc.SQLAlchemyError:
			pass
		return row


class admin(db.Model):
	__tablename__ = 'admin'
	admin_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
	username = db.Column(db.String(15),unique=True)
	fname = db.Column(db.String(15), nullable=False)
	lname = db.Column(db.String(15), nullable=False)
	email = db.Column(db.String(20),unique=True)
	password = db.Column(db.String(10),nullable=False)
	address = db.Column(db.String(100))

	def __init__(self, username, fname, lname, email, password, address):
		self.username = username
		self.fname = fname
		self.lname = lname
		self.email = email
		self.password = password
		self.address = address
	def __repr__(self):
		return '<admin_id {}>'.format(self.admin_id)


class vehiclelocation(db.Model):
	__tablename__ = 'vehiclelocation'
	location_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(15), nullable=False)
	address = db.Column(db.String(100))
	total_capacity = db.Column(db.Integer, nullable=False)

	def __init__(self, id, name, address, total_capacity):
		self.location_id = id
		self.name = name
		self.address = address
		self.total_capacity = total_capacity
	def __repr__(self):
		return '<location_id {}>'.format(self.location_id)

	@classmethod
	def addRow(cls, locationObj):
		try:
			db.session.add(locationObj)
		except exc.SQLAlchemyError:
			print('ADD ERROR !!!')
			pass
		try:
			db.session.commit()
		except exc.SQLAlchemyError:
			print('commit ERROR !!!')
			pass

	@classmethod
	def isLocation(cls, location):
		exists = False
		try:
			exists = db.session.query(vehiclelocation.location_id).filter_by(location_id=location).scalar() is not None
		except exc.SQLAlchemyError:
			print("Location Read error")
			pass
		return exists

	@classmethod
	def getLocationDetails(cls, locationId):
		try:
			result = db.session.query(vehiclelocation).filter_by(location_id = locationId).first()
		except exc.SQLAlchemyError:
			print("Location Read error")
			pass
		return result

	@classmethod
	def updateRow(cls, locationObj):
		try:
			result = db.session.query(vehiclelocation).filter_by(location_id = locationObj.location_id).first()
			result.name = locationObj.name
			result.address = locationObj.address
			result.total_capacity = locationObj.total_capacity
			db.session.add(result)
			# db.session.flush()
			db.session.commit()
		except exc.SQLAlchemyError:
			pass
	
	@classmethod
	def deleteRow(cls, locationId):
		try:
			result = db.session.query(vehiclelocation).filter_by(location_id = locationId).first()
			db.session.delete(result)
			db.session.commit()
		except exc.SQLAlchemyError:
			print("Location Read error")
			pass
		return result

	@classmethod
	def getRows(cls):
		rows = []
		try:
			rows = db.session.query(vehiclelocation).all()
		except exc.SQLAlchemyError:
			pass
		return rows

class vehicle(db.Model):
	__tablename__= 'vehicle'
	vehicle_id = db.Column(db.Integer,primary_key=True)
	vehicle_name = db.Column(db.String(15), nullable=False)
	vehicle_type = db.Column(db.String(15), nullable=False)
	make_company = db.Column(db.String(15),nullable=False)
	model_year = db.Column(db.Integer)
	registration_tag = db.Column(db.String(10), nullable=False)
	current_milegae = db.Column(db.Integer)
	last_service = db.Column(db.Date)
	vehicle_condition = db.Column(db.String(15))
	Location = db.Column(db.Integer,db.ForeignKey('vehiclelocation.location_id'), nullable=False)
	seat_capacity = db.Column(db.Integer, nullable=False)


	def __init__(self, vehicleObj):
		self.vehicle_id = vehicleObj.vehicleID
		self.vehicle_name = vehicleObj.vehicleName
		self.vehicle_type = vehicleObj.vehicleType
		self.make_company = vehicleObj.makeCompany
		self.model_year = vehicleObj.modelYear
		self.registration_tag = vehicleObj.registrationTag
		self.current_milegae = vehicleObj.currentMileage
		self.last_service = vehicleObj.timeLastServiced
		self.vehicle_condition = vehicleObj.vehicleCondition
		self.Location = vehicleObj.location
		self.seat_capacity = vehicleObj.seats
	def __repr__(self):
		return '<{} {} {} {} {} {} {} {} {} {} {}>'.format(self.vehicle_id,
			     self.vehicle_name, self.vehicle_type, self.make_company, self.model_year, self.registration_tag, self.current_milegae,
					self.last_service, self.vehicle_condition, self.Location, self.seat_capacity)

	@classmethod
	def create(cls, vehicleObject):
		try:
			print(vehicleObject)
			db.session.add(vehicleObject)
		except exc.SQLAlchemyError:
			print('add error')
			pass
		try:
			db.session.commit()
		except exc.SQLAlchemyError:
			print('commit error')
			pass

	@classmethod
	def searchByID(cls, vehicleID):
		try:
			result = db.session.query(vehicle).filter_by(vehicle_id = vehicleID).first()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def updateVehicle(cls, vehicleObj):
		try:
			print(vehicleObj)
			result = db.session.query(vehicle).filter_by(vehicle_id = vehicleObj.vehicleID).first()
			result.vehicle_name = vehicleObj.vehicleName
			result.vehicle_type = vehicleObj.vehicleType
			result.make_company =  vehicleObj.makeCompany
			result.model_year  =  vehicleObj.modelYear
			result.registration_tag =  vehicleObj.registrationTag
			result.current_milegae =  vehicleObj.currentMileage
			result.last_service =  vehicleObj.timeLastServiced
			result.vehicle_condition =  vehicleObj.vehicleCondition
			result.Location =  vehicleObj.location
			result.seat_capacity =  vehicleObj.seats
			db.session.add(result)
			db.session.commit()
		except exc.SQLAlchemyError:
			pass

	@classmethod
	def removeVehicle(cls, vehicleId):
		try:
			result = db.session.query(vehicle).filter_by(vehicle_id=vehicleId).first()
			if result:
				db.session.delete(result)
				db.session.commit()
				return True
			else:
				return False	
		except exc.SQLAlchemyError:
			print("removeVehicle error")
			pass

	@classmethod
	def searchByType(cls, vehicleType):
		try:
			result = db.session.query(vehicle).filter_by(vehicle_type=vehicleType).all()
		except exc.SQLAlchemyError:
			print("searchByType error")
			pass
		return result

	@classmethod
	def searchByLocation(cls, locationID):
		try:
			result = db.session.query(vehicle).filter_by(Location=locationID).all()
		except exc.SQLAlchemyError:
			print("searchByLocation error")
			pass
		return result

	@classmethod
	def searchByLocationandType(cls, locationID, vehicleType):
		result = []
		try:
			result = db.session.query(vehicle).filter_by(Location=locationID).filter_by(vehicle_type=vehicleType).all()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def getVehicleType(cls, vehicleID):
		try:
			exits = db.session.query(vehicle.vehicle_type).filter_by(vehicle_id=vehicleID).scalar() is not None
			if (exits):
				return db.session.query(vehicle.vehicle_type).filter_by(vehicle_id=vehicleID).scalar()
			else:
				return -1
		except exc.SQLAlchemyError:
			pass

	@classmethod
	def searchIDByType(cls, vehicleType):
		result = []
		try:
			result = db.session.query(vehicle.vehicle_id).filter_by(vehicle_type=vehicleType).all()
		except exc.SQLAlchemyError:
			print("searchByType error")
			pass
		return result

class bookings(db.Model):
	__tablename__ = 'bookings'
	booking_id = db.Column(db.Integer,primary_key=True, autoincrement=True)
	pickupdatetime = db.Column(db.DateTime, nullable=False)
	dropoffdatetime = db.Column(db.DateTime, nullable=False)
	pickup_location = db.Column(db.Integer, nullable=False)
	vehicle_id = db.Column(db.Integer,db.ForeignKey('vehicle.vehicle_id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	price = db.Column(db.Float)
	comments = db.Column(db.String(100))

	def __init__(self, pickupdatetime, dropoffdatetime, pickup_location, vehicle_id, user_id, price, comments):
		self.pickupdatetime = pickupdatetime
		self.dropoffdatetime = dropoffdatetime
		self.pickup_location = pickup_location
		self.vehicle_id = vehicle_id
		self.user_id = user_id
		self.price = price
		self.comments = comments

	def __repr__(self):
		return '<booking_id {}>'.format(self.booking_id)

	@classmethod
	def addRow(cls, bookingObj):
		try:
			db.session.add(bookingObj)
		except exc.SQLAlchemyError:
			print("Add Error")
			pass
		try:
			db.session.commit()
		except exc.SQLAlchemyError:
			print('commit error')
			pass

	@classmethod
	def isBookingByVehicleID(cls, vehicleID):
		try:
			exists = db.session.query(vehicle).filter_by(vehicle_id=vehicleID).first() is not None
			if (exists):
				return True
			else:
				return False
		except exc.SQLAlchemyError:
			pass
		return False

	@classmethod
	def getBookingsByVehicleID(cls, vehicleID):
		result = []
		try:
			result = db.session.query(bookings).filter_by(vehicle_id=vehicleID).all()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def getBookingByUserID(cls, userId):
		result = []
		try:
			result = db.session.query(bookings).filter_by(user_id=userId).all()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def cancelBooking(cls, bookingId):
		try:
			result = db.session.query(bookings).filter_by(booking_id=bookingId).first()
			db.session.delete(result)
			db.session.commit()
		except exc.SQLAlchemyError:
			print('commit error')
			pass

	@classmethod
	def getBookingbyID(cls, bookingId):
		result = []
		try:
			result = db.session.query(bookings).filter_by(booking_id=bookingId).first()
		except exc.SQLAlchemyError:
			pass
		return result

class baseprice(db.Model):
	__tablename__ = 'price'
	price_id  = db.Column(db.Integer, primary_key=True)
	vehicle_type = db.Column(db.String(15),nullable=False)
	price = db.Column(db.Float, nullable=False)
	FirstDiscount = db.Column(db.Integer)
	SecondDiscount = db.Column(db.Integer)
	ThirdDiscount = db.Column(db.Integer)

	def __init__(self, id, vehicle_type, price, FirstDiscount, SecondDiscount, ThirdDiscount):
		self.price_id = id
		self.vehicle_type = vehicle_type
		self.price = price
		self.FirstDiscount = FirstDiscount
		self.SecondDiscount = SecondDiscount
		self.ThirdDiscount = ThirdDiscount
	def __repr__(self):
		return 'price {}, firstDiscount {}, secondDiscount {}, thirdDiscount {}'.format(self.price_id,
													self.FirstDiscount, self.SecondDiscount, self.ThirdDiscount)

	@classmethod
	def getBasePricebyID(cls, vehicleID):
		try:
			vehicleType = vehicle.getVehicleType(vehicleID)
			result = db.session.query(baseprice.price).filter_by(vehicle_type=vehicleType).scalar()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def getFirstDiscountByID(cls, vehicleID):
		try:
			vehicleType = vehicle.getVehicleType(vehicleID)
			result = db.session.query(baseprice.FirstDiscount).filter_by(vehicle_type=vehicleType).scalar()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def getSecondDiscountByID(cls, vehicleID):
		try:
			vehicleType = vehicle.getVehicleType(vehicleID)
			result = db.session.query(baseprice.SecondDiscount).filter_by(vehicle_type=vehicleType).scalar()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def getThirdDiscountByID(cls, vehicleID):
		try:
			vehicleType = vehicle.getVehicleType(vehicleID)
			result = db.session.query(baseprice.ThirdDiscount).filter_by(vehicle_type=vehicleType).scalar()
		except exc.SQLAlchemyError:
			pass
		return result

	@classmethod
	def setprice(cls, vehicleType, price):
		try:
			row = db.session.query(baseprice).filter(baseprice.vehicle_type == vehicleType).first()
			row.price = price
			db.session.commit()
		except exc.SQLAlchemyError:
			print("SET error !!!")
			pass
		return
	@classmethod
	def setFirstDiscount(cls, vehicleType, value):
		try:
			row = db.session.query(baseprice).filter(baseprice.vehicle_type == vehicleType).first()
			row.FirstDiscount = value
			db.session.commit()
		except exc.SQLAlchemyError:
			pass
		return
	@classmethod
	def setSecondDiscount(cls, vehicleType, value):
		try:
			row = db.session.query(baseprice).filter(baseprice.vehicle_type == vehicleType).first()
			row.SecondDiscount = value
			db.session.commit()
		except exc.SQLAlchemyError:
			pass
		return
	@classmethod
	def setThirdDiscount(cls, vehicleType, value):
		try:
			row = db.session.query(baseprice).filter(baseprice.vehicle_type == vehicleType).first()
			row.ThirdDiscount = value
			db.session.commit()
		except exc.SQLAlchemyError:
			pass
		return
	@classmethod
	def create(cls, basePriceobj):
		try:
			print(basePriceobj)
			db.session.add(basePriceobj)
			db.session.commit()
		except exc.SQLAlchemyError:
			print('Error')
			pass
		return



# Changes by Ranjani from here......................................................................................................
# Post is to post details in the home page

@login_manager.user_loader
def load_user(user_id):
		try:
			return db.session.query(user).filter_by(email=user_id).first()
		except:
			return None

