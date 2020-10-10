from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField, FloatField, ValidationError, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import DateTimeField
from wtforms.fields.html5 import DateField
from RentCar.User.User import User
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, NumberRange, AnyOf, Optional, Required
from datetime import datetime
from dateutil.relativedelta import relativedelta
from RentCar.Vehicle.VehicleLocation import VehicleLocation

class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname',
                           validators=[DataRequired(), Length(min=5, max=15)])
    lastname = StringField('Lastname',
                           validators=[DataRequired(), Length(min=5, max=15)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=18, max=60)])
    driverId = IntegerField('Driver ID',validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(min=10, max=50)])
    submit = SubmitField('Payment')

    def validate_username(self, username):
        if (User.isUserPresent(username.data)):
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if (User.isEmailPresent(email.data)):
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class BookingForm(FlaskForm):
    def validate(self):
        t1 = self.date_pickup.data
        t2 = self.date_drop.data
        t1 = datetime.strptime(str(t1), '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime(str(t2), '%Y-%m-%d %H:%M:%S')
        if (t1 < datetime.now()):
            self.date_pickup.errors = ('', 'Please select a future date and time.')
            return False

        diff = relativedelta(t2, t1)
        num_of_hours = 0
        i = 0
        while (i < diff.days):
            num_of_hours += 24
            i += 1
        num_of_hours += diff.hours
        if (num_of_hours < 1):
            self.date_drop.errors = ('', 'Drop time should be minimum 1 hour away from PickupTime')
            return False
        elif (num_of_hours > 72):
            self.date_drop.errors = ('', 'Please select drop time not more than 3 days.')
            return False
        return True

    cartype = SelectField('Car Rental Type', choices=[('SMALLCAR', 'Small Car'), ('FULLSIZECAR', 'Full size car'), ('TRUCK', 'Truck'), ('LUXURYCAR', 'Luxury Car')], validators=[InputRequired()])
    date_pickup = DateTimeLocalField('Pickup Date-Time', format='%Y-%m-%dT%H:%M' , validators=[DataRequired()])
    date_drop = DateTimeLocalField('Drop-Off Date-Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    _list = VehicleLocation.getVehilces()
    pickup_location = SelectField('Pickup Location', choices=[(c.location_id, c.name) for c in _list])
    submit = SubmitField('Search Vehicle')
    submitbook = SubmitField('Book')

class UseraccountForm(FlaskForm):
    username = StringField('Driver ID',validators=[DataRequired(), Length(min=5, max=15)])
    fname = StringField('Driver ID',validators=[DataRequired(), Length(min=5, max=15)])
    lname =StringField('Driver ID',validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    age = SelectField('Age', validators=[DataRequired(), NumberRange(min=18, max=60)])
    driverId = IntegerField('Driver ID',validators=[DataRequired(), Length(min=5, max=10)])
    address = StringField('Username', validators=[DataRequired(), Length(min=10, max=50)])
    submit = SubmitField('Submit')
    
class CancelbookingForm(FlaskForm):
    booking_id = IntegerField('Booking ID')
    pickupdatetime = DateTimeLocalField('Pickup Date-Time', format='%y/%m/%d')
    dropoffdatetime = DateTimeLocalField('Drop-Off Date-Time', format='%y/%m/%d')
    _list = VehicleLocation.getVehilces()
    pickup_location = SelectField('Pickup Location', choices=[(c.location_id, c.name) for c in _list])
    vehicle_id = IntegerField('Enter the Vehicle ID To Remove')
    price = FloatField('Price')
    submit =  SubmitField('Cancel')

class VehicleReturnForm(FlaskForm):
    booking_id = IntegerField('Booking ID')
    pickupdatetime = DateTimeLocalField('Pickup Date-Time', format='%y/%m/%d')
    dropoffdatetime = DateTimeLocalField('Drop-Off Date-Time', format='%y/%m/%d')
    _list = VehicleLocation.getVehilces()
    pickup_location = SelectField('Pickup Location', choices=[(c.location_id, c.name) for c in _list])
    vehicle_id = IntegerField('Enter the Vehicle ID To Remove')
    price = FloatField('Price')
    submit = SubmitField('Return Vehicle')

class FinalPriceForm(FlaskForm):
    price = DecimalField('Your Final Price')
    comments = TextAreaField('Enter Comments (Optional)', validators=[Optional()])
    submit = SubmitField('Payment')

class FinalPaymentForm(FlaskForm):
    price = DecimalField('Your Final Price')

class VehicleSearchForm(FlaskForm):
    vehicle_id = IntegerField('Vehicle ID')
    vehicle_name = StringField('Vehicle Name')
    Location = IntegerField('Vehicle Location')
    seat_capacity = IntegerField('Vehicle Seat Capacity')
    vehicle_type = StringField('Vehicle Type')
    submitbook =  SubmitField('Book')

class RemoveVehicleForm(FlaskForm):
    vehId = IntegerField('Enter the Vehicle ID To Remove', [DataRequired(message="Enter a Valid Vehicle ID")])
    submit = SubmitField('Delete Vehicle')

class AddVehicleForm(FlaskForm):
    vehId = IntegerField('Enter the Vehicle ID', [DataRequired(message="Enter a Valid Vehicle ID"), NumberRange(min=1)])
    vehName = StringField('Enter the Vehicle Name', [DataRequired(message="Enter a Valid Vehicle Name"), Length(max=25)])
    vehCompany = StringField('Enter the Vehicle Company', [DataRequired(message="Enter a Valid Vehicle Company"), Length(max=15)])
    vehModel = IntegerField('Enter the Model Year for the Vehicle', [DataRequired(message="Enter a Valid Vehicle Model"), NumberRange(min=1990, max=2020)])
    vehMileage = DecimalField('Enter the Vehicle Mileage', [DataRequired(message="Enter a Valid Vehicle Mileage"), NumberRange(min=0, max=200000)])
    #vehLocation = IntegerField('Enter the Vehicle Location', [DataRequired(message="Enter a Valid Vehicle Location"), NumberRange(min=1, max=200)])
    _list = VehicleLocation.getVehilces()
    vehLocation = SelectField('Vehicle Location', coerce=int, choices=[(c.location_id, c.name) for c in _list])
    timeLastServiced = DateField('Enter the Last Vehicle Service Date', [DataRequired(message="Enter a Valid Service Date")])
    registrationTag = StringField('Enter the Serivce Tag', [DataRequired(message="Enter a Valid Service Tag"), Length(max=10)])
    seatCapacity = IntegerField('Enter the Seat Capacity', [DataRequired(message="Enter a Valid Vehicle Seat Capacity"), NumberRange(min=1, max=9)])
    vehType = SelectField('Select Vehicle Type', choices=[('SMALLCAR', 'Small Car'), ('FULLSIZECAR', 'Full size car'), ('TRUCK', 'Truck'), ('LUXURYCAR', 'Luxury Car')])
    vehCondition = SelectField('Select Vehicle Condition', choices=[('BRANDNEW', 'Brand New'), ('GOOD', 'Good'), ('NEEDSCLEANING', 'Needs Cleaning'), ('NEEDSERVICE', 'Needs Service')])
    submit = SubmitField('Add Vehicle')

class GetVehicleForm(FlaskForm):
    vehId = IntegerField('Enter the Vehicle ID', [DataRequired(message="Enter a Valid Vehicle ID")])
    getsubmit = SubmitField('Get Vehicle Details')

class UpdateVehicleForm(FlaskForm):
    vehId = IntegerField('Enter the Vehicle ID To Remove', [DataRequired(message="Enter a Valid Vehicle ID"), NumberRange(min=1)])
    vehName = StringField('Enter the Vehicle Name', [DataRequired(message="Enter a Valid Vehicle Name")])
    vehCompany = StringField('Enter the Vehicle Company', [DataRequired(message="Enter a Valid Vehicle Company"), Length(max=15)])
    vehModel = IntegerField('Enter the Model Year for the Vehicle', [DataRequired(message="Enter a Valid Vehicle Model"), NumberRange(min=1990, max=2020)])
    vehMileage = DecimalField('Enter the Vehicle Mileage', [DataRequired(message="Enter a Valid Vehicle Mileage"), NumberRange(min=0, max=200000)])
    # vehLocation = IntegerField('Enter the Vehicle Location', [DataRequired(message="Enter a Valid Vehicle Location"), NumberRange(min=1, max=200)])
    _list = VehicleLocation.getVehilces()
    vehLocation = SelectField('Vehicle Location', coerce=int, choices=[(c.location_id, c.name) for c in _list])
    timeLastServiced = DateField('Enter the Last Vehicle Service Date', [DataRequired(message="Enter a Valid Service Date")])
    registrationTag = StringField('Enter the Serivce Tag', [DataRequired(message="Enter a Valid Service Tag"), Length(max=10)])
    seatCapacity = IntegerField('Enter the Seat Capacity', [DataRequired(message="Enter a Valid Vehicle Seat Capacity"), NumberRange(min=1, message='Enter a Valid Number')])
    vehType = SelectField('Select Vehicle Type', choices=[('SMALLCAR', 'Small Car'), ('FULLSIZECAR', 'Full size car'), ('TRUCK', 'Truck'), ('LUXURYCAR', 'Luxury Car')])
    vehCondition = SelectField('Select Vehicle Type', choices=[('BRANDNEW', 'Brand New'), ('GOOD', 'Good'), ('NEEDSCLEANING', 'Needs Cleaning'), ('NEEDSERVICE', 'Needs Service')])
    updatesubmit = SubmitField('Update Vehicle')

class VehicleLocationForm(FlaskForm):
    locationId = IntegerField('Enter the Vehicle Location ID', [DataRequired(message="Enter a Valid Vehicle Location"), NumberRange(min=1, max=200)])
    name = StringField('Enter the Location Name', [DataRequired(message="Enter a Valid Location Name")])
    address = StringField('Enter the Location Address', [DataRequired(message="Enter a Valid Location Address"), Length(min=5, max=50)])
    totalcapacity = IntegerField('Enter the Capacity of the Location', [DataRequired(message="Enter a Valid Numeric value"), NumberRange(min=1, max=500)])
    submit = SubmitField('Enter Location Details')

class GetLocationForm(FlaskForm):
    locationId = IntegerField('Enter the Vehicle Location ID', [DataRequired(message="Enter a Valid Vehicle Location"), NumberRange(min=1, max=200)])
    submit = SubmitField('Get Location Details')

class UpdateLocationForm(FlaskForm):
    locationId = IntegerField('Enter the Vehicle Location ID', [DataRequired(message="Enter a Valid Vehicle Location"), NumberRange(min=1, max=200)])
    name = StringField('Enter the Location Name', [DataRequired(message="Enter a Valid Location Name")])
    address = StringField('Enter the Location Address', [DataRequired(message="Enter a Valid Location Address")])
    totalcapacity = IntegerField('Enter the Capacity of the Location', [DataRequired(message="Enter a Valid Numeric value"), NumberRange(min=1)])
    submit = SubmitField('Update Location Details')

class GetLocationRemovalForm(FlaskForm):
    locationId = IntegerField('Enter the Vehicle Location ID', [DataRequired(message="Enter a Valid Vehicle Location"), NumberRange(min=1, max=200)])
    submit = SubmitField('Get Location Details To Remove')

class RemoveLocationForm(FlaskForm):
    locationId = IntegerField('Enter the Vehicle Location ID', [DataRequired(message="Enter a Valid Vehicle Location"), NumberRange(min=1, max=200)])
    name = StringField('Enter the Location Name', [DataRequired(message="Enter a Valid Location Name")])
    address = StringField('Enter the Location Address', [DataRequired(message="Enter a Valid Location Address")])
    totalcapacity = IntegerField('Enter the Capacity of the Location', [DataRequired(message="Enter a Valid Numeric value"), NumberRange(min=1)])
    submit = SubmitField('Remove Location Details')

class GetVehicleTypeForm(FlaskForm):
    vehicle_type = SelectField('Select Vehicle Type', choices=[('SMALLCAR', 'Small Car'), ('FULLSIZECAR', 'Full size car'), ('TRUCK', 'Truck'), ('LUXURYCAR', 'Luxury Car')])
    submit = SubmitField('Submit')

class PriceForm(FlaskForm):
    price_id  = IntegerField('PriceID')
    vehicle_type = SelectField('Select Vehicle Type', choices=[('SMALLCAR', 'Small Car'), ('FULLSIZECAR', 'Full size car'), ('TRUCK', 'Truck'), ('LUXURYCAR', 'Luxury Car')])
    price = FloatField('Base Price', [DataRequired('Enter the Base Price')])
    FirstDiscount = IntegerField('First Discount', [DataRequired(message="Enter a Valid First Discount"), NumberRange(min=1, max=50)])
    SecondDiscount = IntegerField('Second Discount', [DataRequired(message="Enter a Valid Second Discount"), NumberRange(min=1, max=50)])
    ThirdDiscount = IntegerField('Third Discount', [DataRequired(message="Enter a Valid Third Discount"), NumberRange(min=1, max=50)])
    submit = SubmitField('Submit to Set Price')

class TerminateForm(FlaskForm):
    cancel = SubmitField('Terminate Membership')