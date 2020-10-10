from RentCar.Booking.Pricing import Pricing
from RentCar.models import baseprice, bookings, vehicle
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Search:
    def __init__(self):
        pass

    @classmethod
    def searchByType(cls, vehicleType) -> list:
        res = []
        res = vehicle.searchByType(vehicleType)
        return res

    @classmethod
    def searchByLocationandType(cls, location, typelist) -> list:
        res = []
        for row in typelist:
            if (row.Location == int(location)):
                res.append(row)
        return res

    @classmethod
    def searchByAvailability(cls, pickupTime, dropTime, locationlist) -> list:
        res = []
        for row in locationlist:
            if (not bookings.isBookingByVehicleID(row.vehicle_id)):
                print('no boooking for this vehicle')
                res.append(row)
            else:
                if (not Booking.isVehicleBooked(row.vehicle_id, pickupTime, dropTime)):
                    print('not available now')
                    res.append(row)
        return res

class Booking:
    def __init__(self, vehicleID, userID, pickupTime, dropOffTime, pickupLocation, comments):
        self.vehicleID = vehicleID
        self.userID = userID
        self.pickupTime = pickupTime
        self.dropOffTime = dropOffTime
        self.pickupLocation = pickupLocation
        self.comments = comments
        self.price = self.calculatePrice(self.vehicleID, self.pickupTime, self.dropOffTime, 0)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.vehicleID, self.userID, self.pickupTime, self.dropOffTime, self.pickupLocation, self.price)

    @Pricing.calcBasePrice
    def calculatePrice(vehicleID, t1, t2, basePrice):
        diff = relativedelta(t2, t1)
        num_of_hours = 0
        i = 0
        while (i < diff.days):
            num_of_hours += 24
            i += 1
        num_of_hours += diff.hours
        if (num_of_hours <= 5):
            discount = baseprice.getFirstDiscountByID(vehicleID)
            print(discount)
            price = num_of_hours * basePrice * (1 - (0.01*discount))
        elif (num_of_hours<=10):
            discount = baseprice.getSecondDiscountByID(vehicleID)
            price = num_of_hours * basePrice * (1 - (0.01*discount))
        elif (num_of_hours<=72):
            discount = baseprice.getThirdDiscountByID(vehicleID)
            price = num_of_hours * basePrice * (1 - (0.01 * discount))
        print(price)
        return price

    @classmethod
    def isVehicleBooked(cls, vehicleID, pickuptime, droptime) -> bool:
        if (not bookings.isBookingByVehicleID(vehicleID)):
            return False
        res = bookings.getBookingsByVehicleID(vehicleID)
        for row in res:
            t1 = row.pickupdatetime
            t2 = row.dropoffdatetime
            if (pickuptime <= t2 and droptime >= t1):
                return True
            print(pickuptime)
            print(droptime)
            print(t1)
            print(t2)
        return False

    def confirmBooking(self):
        print(self)
        bookings.addRow(bookings(self.pickupTime, self.dropOffTime, self.pickupLocation, self.vehicleID, self.userID, self.price, self.comments))
    
    @classmethod
    def getBookingByUserID(cls, userId):
        result = bookings.getBookingByUserID(userId)
        return result
    
    @classmethod
    def checkValidCancel(cls, bookingId) -> bool:
        row = bookings.getBookingbyID(bookingId)
        if (row.pickupdatetime < datetime.now()):
            return False
        return True

    @classmethod
    def calcHourDifference(cls, diff) -> int:
        num_of_hours = 0
        i = 0
        while (i < diff.days):
            num_of_hours += 24
            i += 1
        num_of_hours += diff.hours
        return num_of_hours

    @classmethod
    def calcCancelDue(cls, bookingId) -> float:
        row = bookings.getBookingbyID(bookingId)
        diff = relativedelta(datetime.now(), row.pickupdatetime)
        num_of_hours = Booking.calcHourDifference(diff)

        if (num_of_hours <= 1):
            basePrice = baseprice.getBasePricebyID(row.vehicle_id)
            return basePrice
        else:
            return 0.0

    @classmethod
    def calcFinalDue(cls, bookingId) -> float:
        row = bookings.getBookingbyID(bookingId)
        if (row.dropoffdatetime < datetime.now()):
            diff = relativedelta(row.dropoffdatetime, datetime.now())
            num_of_hours = Booking.calcHourDifference(diff)
            basePrice = baseprice.getBasePricebyID(row.vehicle_id)
            return (num_of_hours * basePrice) + row.price
        else:
            return row.price


    @classmethod
    def checkValidReturn(cls, bookingId) -> bool:
        row =  bookings.getBookingbyID(bookingId)
        if (datetime.now() < row.pickupdatetime):
            return False
        return True