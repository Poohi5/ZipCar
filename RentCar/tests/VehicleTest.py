import unittest
from datetime import datetime
from RentCar.Vehicle.VehicleFactory import VehicleFactory
from RentCar.Vehicle.VehicleLocation import VehicleLocation
from RentCar.Vehicle.VehicleType import VehicleType
from RentCar.Vehicle.VehicleCondition import VehicleCondition
from RentCar.models import vehicle

class VehicleTest(unittest.TestCase):
    def testDB(self):
        return
        mydate = datetime.now()
        #location =  VehicleLocation(1, "santaclara", "california", 50)
        #location.insertRow()
        vehicleObj = VehicleFactory.makeVehicle(4, "ACCORD", "HONDA", 2020, 100, 1, mydate, "349753", VehicleCondition.BRANDNEW.name, VehicleType.FULLSIZECAR.name, 5)
        vehiclerow = vehicle(vehicleObj)
        vehicle.create(vehiclerow)

    def testSearch(self):
        res = vehicle.searchByLocation(1)
        for r in res:
            print(type(r))

if __name__ == '__main__':
    unittest.main()
