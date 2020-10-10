import sys
from importlib import reload
from RentCar.Vehicle import Vehicle
reload(Vehicle)
from RentCar.Vehicle.VehicleFactory import VehicleFactory

class VehicleClient:
    vehiclefactoryObject = VehicleFactory()
    if (not vehiclefactoryObject):
        raise Exception('\n ERROR in vehiclefactoryObject instantiation \n')

    obj1 = vehiclefactoryObject.makeVehicle("Indica", "Tata", "2019", "12500", "Delhi", '31/07/2019', 'DL-05BY8597', 'GOOD', '100', "SmallCar")
    obj2 = vehiclefactoryObject.makeVehicle("Indigo", "Tata", "2019", "12500", "Delhi", '31/07/2019', 'DL-05AY8597', 'NEEDSMAINTENANCE', '300', "FullSizeCar")
    obj3 = vehiclefactoryObject.makeVehicle("Ace", "Tata", "2019", "12500", "Delhi", '31/07/2019', 'DL-05CY8597', 'NEEDSMAINTENANCE', '500', "Truck")
    obj4 = vehiclefactoryObject.makeVehicle("Nexon", "Tata", "2019", "12500", "Delhi", '31/07/2019', 'DL-05DY8597', 'NEEDSMAINTENANCE', '800', "LuxuryCar")
    print(obj1)
    print(obj2)
    print(obj3)
    print(obj4)
