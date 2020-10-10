import unittest
from RentCar.Booking.Booking import Booking
from RentCar.Booking.Pricing import Pricing
from RentCar.Vehicle.VehicleType import VehicleType
from datetime import datetime, timedelta

from _datetime import datetime
class BookingTest(unittest.TestCase):
    def test_price(self):
        a = datetime.now()
        b = a + timedelta(hours=5)
        #booking = Booking(1,3,a,b,1, "It was a good experience")
        #print(booking.calculatePrice(1, 3, 8, 0))
        #booking.confirmBooking()
        pass

    def testdb(self):
        pricing = Pricing.addRow(2, VehicleType.FULLSIZECAR.name, 25.0, 5, 10, 15)
        pass

    def testSet(self):
        #Pricing.setSecondDiscount(VehicleType.SMALLCAR.name, 15)
        pass

if __name__ == '__main__':
    unittest.main()
