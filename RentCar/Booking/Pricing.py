from RentCar.models import baseprice
class Pricing:
    @classmethod
    def addRow(cls, id, vehicleType, price, firstDiscount, secondDiscount, thirdDiscount):
        baseprice.create(baseprice(id, vehicleType, price, firstDiscount, secondDiscount, thirdDiscount))

    @classmethod
    def setBasePrice(cls, vehicleType, value):
        baseprice.setprice(vehicleType, value)

    @classmethod
    def setfirstDiscount(cls, vehicleType, value):
        baseprice.setFirstDiscount(vehicleType, value)

    @classmethod
    def setSecondDiscount(cls, vehicleType, value):
        baseprice.setSecondDiscount(vehicleType, value)

    @classmethod
    def setThirdDiscount(cls, vehicleType, value):
        baseprice.setThirdDiscount(vehicleType, value)

    def calcBasePrice(func):
        def commonPrice(self, vehicleID, t1, t2, basePrice):
            basePrice = baseprice.getBasePricebyID(vehicleID)
            return func(vehicleID, t1, t2, basePrice)
        return commonPrice






