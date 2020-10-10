from flask import request
from RentCar.Vehicle.VehicleFactory import VehicleFactory
from RentCar.Vehicle.Vehicle import Vehicle
from RentCar.models import vehicle, user
from _datetime import datetime
class Admin:
    def __init__(self):
        pass
    @classmethod
    def addVehicleDetails(self, vehicleId, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, vehicleType, seatCapacity):
        vehicleObj = VehicleFactory.makeVehicle(vehicleId, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, vehicleType, seatCapacity)
        vehicleObj.writeToDB()

    @classmethod
    def getVehicleDetails(cls, vehicleId):
        res = vehicle.searchByID(vehicleId)
        return res

    @classmethod
    def updateVehicleDetails(self, vehicleId, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, vehicleType, seats):
        vehicleObj = VehicleFactory.makeVehicle(vehicleId, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, vehicleType, seats)
        vehicle.updateVehicle(vehicleObj)

    @classmethod
    def removeVehicleDetails(cls, vehicleId):
        return vehicle.removeVehicle(vehicleId)

    @classmethod
    def listUser(cls):
        userList = user.listUser()
        return userList

    @classmethod
    def removeUser(cls, userName):
        user.removeUser(userName)
