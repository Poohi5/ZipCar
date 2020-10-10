from RentCar.models import vehiclelocation
class VehicleLocation:
    def __init__(self, id, name, address, totalCapacity):
        self.id = id
        self.name = name
        self.address = address
        self.totalCapacity = totalCapacity
        self.vehicles = set()

    def getName(self):
        return self.name

    def getAddress(self):
        return self.address

    def getCapacity(self):
        return self.totalCapacity

    def getID(self):
        return self.id

    def setName(self, name):
        self.name = name

    def setID(self, id):
        self.id = id

    def setAddress(self, address):
        self.address = address

    def setCapacity(self, totalCapacity):
        self.totalCapacity = totalCapacity

    def addVehicle(self, vehicleObject):
        self.vehicles.add(vehicleObject)

    def removeVehicle(self, vehicleObject):
        if (vehicleObject in self.vehicles):
            self.vehicles.remove(vehicleObject)
        else:
            return

    @classmethod
    def getVehilces(cls):
        return vehiclelocation.getRows()

    def insertRow(self):
        locationRow = vehiclelocation(self.id, self.name, self.address, self.totalCapacity)
        vehiclelocation.addRow(locationRow)

    @classmethod
    def isLocationPresent(cls, location) -> bool:
        return vehiclelocation.isLocation(location)