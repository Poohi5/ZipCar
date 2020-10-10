from RentCar.Vehicle.LuxuryCar import LuxuryCar
from RentCar.Vehicle.SmallCar import SmallCar
from RentCar.Vehicle.Truck import Truck
from RentCar.Vehicle.FullSizeCar import FullSizeCar
from RentCar.Vehicle import Vehicle

from importlib import reload
reload(Vehicle)

class VehicleFactory:
	__instance = None
	@staticmethod
	def getVehicleFactory():
		if (VehicleFactory.__instance):
			return VehicleFactory.__instance
		VehicleFactory()

	def __init__(self):
		if (VehicleFactory.__instance):
			raise Exception('\n ERROR! VehicleFactory is a singleton class \n')
		else:
			VehicleFactory.__instance = self

	def makeVehicle(vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, vehicleType, seatCapacity):
		vehicleObject = None
		if (vehicleType == "SMALLCAR"):
			vehicleObject = SmallCar(vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seatCapacity)
		elif (vehicleType == "FULLSIZECAR"):
			vehicleObject = FullSizeCar(vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seatCapacity)
		elif (vehicleType == "TRUCK"):
			vehicleObject = Truck(vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seatCapacity)
		elif (vehicleType == "LUXURYCAR"):
			vehicleObject = LuxuryCar(vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seatCapacity)
		return vehicleObject
