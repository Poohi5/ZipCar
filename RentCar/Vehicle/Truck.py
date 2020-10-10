from RentCar.Vehicle.VehicleType import VehicleType
from RentCar.Vehicle import Vehicle
class Truck(Vehicle.Vehicle):
	def __init__(self, vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seats):
		super(Truck, self).__init__(vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seats)
		self.vehicleType = VehicleType.TRUCK.name
