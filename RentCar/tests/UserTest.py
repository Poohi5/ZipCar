import unittest
from RentCar.User.User import User

class UserTest(unittest.TestCase):
    def testinsertDB(self):
        #userObj = User("vigneshk", "Vignesh Kumar", "Thangarajan", "vignesh@gmail.com", "test123", 27, 124234, "benton st",  "WAITING")
        #userObj.insertRow()
        pass

    def testremoveDB(self):
        pass
        #userObj = User()
        #userObj.removeRow("vigneshk")

    def testAuthentication(self):
        userObj = User()
        print(userObj.authenticateUser("vigneshk", "test123"))

if __name__ == '__main__':
    unittest.main()
