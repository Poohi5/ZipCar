from RentCar.models import user
class User:
    def __init__(self, username, fname, lname, email, password, age, driverID, address, driverValidity):
        self.username = username
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
        self.age = age
        self.driverID = driverID
        self.driverValidity = driverValidity
        self.address = address

    def insertRow(self):
        userobj = user(self.username, self.fname, self.lname, self.email, self.password, self.age, self.driverID, self.address, self.driverValidity)
        user.addRow(userobj)

    @classmethod
    def removeRow(cls, username):
        user.removeUser(username)

    @classmethod
    def authenticateUser(cls, email, password) -> bool:
        if (not user.isEmailExist(email)):
            return False
        return (user.getPassword(email) == password)

    @classmethod
    def isUserPresent(cls, username) -> bool:
        if (user.isUserExist(username)):
            return True
        return False

    @classmethod
    def isEmailPresent(cls, email) -> bool:
        if (user.isEmailExist(email)):
            return True
        return False

    @classmethod
    def getusername(cls, email):
        return user.getUsername(email)

    @classmethod
    def getRow(cls, email):
        return user.getRow(email)