from RentCar.Vehicle.VehicleType import VehicleType
from RentCar.Vehicle import Vehicle
class SmallCar(Vehicle.Vehicle):
	def __init__(self, vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seats):
		super(SmallCar, self).__init__(vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seats)
		self.vehicleType = VehicleType.SMALLCAR.name
