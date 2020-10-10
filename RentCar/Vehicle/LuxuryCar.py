from RentCar.Vehicle.VehicleType import VehicleType
from RentCar.Vehicle import Vehicle
class LuxuryCar(Vehicle.Vehicle):
	def __init__(self, vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seats):
		super(LuxuryCar, self).__init__(vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seats)
		self.vehicleType = VehicleType.LUXURYCAR.name
