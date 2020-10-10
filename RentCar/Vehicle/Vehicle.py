from RentCar.Vehicle.VehicleCondition import VehicleCondition
from RentCar.models import vehicle, vehiclelocation

class Vehicle:
    def __init__(self, vehicleID, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, seats):
        self.vehicleID = vehicleID
        self.vehicleName = self.setName(vehicleName)
        self.makeCompany = self.setmakeCompany(makeCompany)
        self.modelYear = modelYear
        self.currentMileage = currentMileage
        self.location = location
        self.timeLastServiced = timeLastServiced
        self.registrationTag = self.setRegistrationTag(registrationTag)
        self.vehicleCondition = self.setVehicleCondition(vehicleCondition)
        self.seats = seats

    def __hash__(self):
        return hash((self.registrationTag, self.vehicleID))

    def __eq__(self, other):
        if (self.registrationTag == other.registrationTag and self.vehicleID == other.vehicleID):
            return True
        return False

    def __repr__(self):
        return 'Vehicle(vehicleName=%s, makeCompany=%s, modelYear=%s, currentMileage=%s, location=%s, timeLastServiced=%s, registrationTag=%s, vehicleCondition=%s, seats=%s)' \
                        % (self.vehicleName, self.makeCompany, self.modelYear, self.currentMileage, self.location, self.timeLastServiced, self.registrationTag, self.vehicleCondition, self.seats)

    def isValidLocation(self, location):
        if (vehiclelocation.isLocation(location)):
            return True
        return False

    #check the parking current capacity before assigning vehicle to that parking
    def getLocationCapacity(self):
        return

    def writeToDB(self):
        if (not self.isValidLocation(self.location)):
            print("Not a valid location")
            return
        vehicleRow = vehicle(self)
        vehicle.create(vehicleRow)

    def setName(self, vehicleName):
        print(vehicleName)
        if (len(vehicleName) <= 15):
            return vehicleName
        else:
            return vehicleName[:15]

    def setmakeCompany(self, makeCompany):
        if (len(makeCompany) <= 15):
            return makeCompany
        else:
            return makeCompany[:15]

    def setRegistrationTag(self, registrationTag):
        if (len(registrationTag) <= 10):
            return registrationTag
        else:
            return registrationTag[:10]

    def setVehicleCondition(self, vehicleCondition):
        if (vehicleCondition == "BRANDNEW"):
            return VehicleCondition.BRANDNEW.name
        elif (vehicleCondition == "GOOD"):
            return VehicleCondition.GOOD.name
        elif (vehicleCondition == "NEEDSCLEANING"):
            return VehicleCondition.NEEDSCLEANING.name
        elif (vehicleCondition == "NEEDSERVICE"):
            return VehicleCondition.NEEDSERVICE.name
        return VehicleCondition.INVALID.name

    def searchVehiclebyID(self, vehicleID):
        return vehicle.searchByID(vehicleID)

    def searchVehicleByType(self, vehicleType):
        return vehicle.searchByType(vehicleType)

    def searchVehicleByLocation(self, location):
        return vehicle.searchByLocation(location)