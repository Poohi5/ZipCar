from RentCar import app
from flask import render_template, url_for, flash, redirect, request
from RentCar.forms import *
from RentCar.models import bookings, vehiclelocation
from flask_login import login_user, current_user, logout_user, login_required
from RentCar.Admin.Admin import Admin
from RentCar.Booking.Booking import Booking
from RentCar.Booking.Pricing import Pricing
from RentCar import stripe_keys
import stripe
from _datetime import datetime
from RentCar.User.User import User
from RentCar.Booking.Booking import Search
from RentCar.Vehicle.VehicleType import VehicleType
from RentCar.Vehicle.VehicleLocation import VehicleLocation

global bookid

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html') #Home Page  #post

@app.route("/home_user")
def home_user():
    return render_template('home_user.html') 

@app.route("/home_admin")
def home_admin(): 
    return render_template('home_admin.html') #Admin Home page #post

@app.route("/vehiclereturn", methods=['GET','POST'])
def vehiclereturn():
    rows = Booking.getBookingByUserID(current_user.id)
    names=[]
    for row in rows:
        names.append(vehiclelocation.getLocationDetails(row.pickup_location).name)
    form = VehicleReturnForm()
    global bookid
    if form.is_submitted():
        booking_id = int(form.booking_id.data)
        if (not Booking.checkValidReturn(booking_id)):
            flash('Vehicle cannot be returned before Pickup Time','danger')
            return render_template('vehiclereturn.html', results=zip(rows,names), form=form)
        bookid = booking_id
        price = Booking.calcFinalDue(booking_id)
        return redirect(url_for('finalprice', data=price))
    return render_template('vehiclereturn.html', results=zip(rows,names), form=form)

@app.route("/finalprice", methods=['GET','POST'])
def finalprice():
    price = request.args.get('data')
    form = FinalPriceForm()
    form.price.data = float(price)
    if form.validate_on_submit():
        return redirect(url_for('payment', data=price))
    return render_template('finalprice.html', form=form)

@app.route("/cancelbooking", methods=['GET','POST']) 
def cancelbooking():
    rows = Booking.getBookingByUserID(current_user.id)
    names = []
    for row in rows:
        names.append(vehiclelocation.getLocationDetails(row.pickup_location).name)
    form = CancelbookingForm()
    price = 0.0
    global bookid
    if form.is_submitted():
        booking_id = int(form.booking_id.data)
        bookid = booking_id
        if (Booking.checkValidCancel(booking_id)):
            price = Booking.calcCancelDue(booking_id)
            if (price<=0.0):
                bookings.cancelBooking(booking_id)
                flash('Your booking has been cancelled', 'success')
                return redirect(url_for('home_user'))
            elif price>0.0:
                return redirect(url_for('finalprice', key=stripe_keys['publishable_key'], data=price))
        else:
            flash('Past Pickup Time Bookings can only be returned', 'danger')
    return render_template('cancelbooking.html', results=zip(rows,names), form=form)

@app.route("/terminate_membership",methods=['GET','POST'])
def terminate_membership():
    form = TerminateForm()
    if form.is_submitted():
        temp = current_user.username
        logout_user()
        User.removeRow(temp)
        return redirect(url_for('login'))
    return render_template('terminate_membership.html', form=form)

@app.route("/add-vehicle-details", methods=['GET', 'POST'])
def addvehicledetails():
    showForm = "addVehicle"
    form = AddVehicleForm()
    if form.validate_on_submit():
        vehicleId = int(form.vehId.data)
        vehicleObject = Admin.getVehicleDetails(vehicleId)
        if vehicleObject:
            flash('The Vehicle ID already exists. Enter a new ID', 'danger')
            return render_template('vehicledetails.html', showForm = showForm, form = form)
        else:
            vehicleId = int(form.vehId.data)
            vehicleName = str(form.vehName.data)
            vehicleType = str(form.vehType.data)
            makeCompany = str(form.vehCompany.data)
            modelYear = int(form.vehModel.data)
            currentMileage = float(form.vehMileage.data)
            location = int(form.vehLocation.data)
            timeLastServiced = datetime.strptime(str(form.timeLastServiced.data), '%Y-%M-%d')
            registrationTag = str(form.registrationTag.data)
            vehicleCondition = str(form.vehCondition.data)
            seatCapacity = int(form.seatCapacity.data)
            Admin.addVehicleDetails(vehicleId, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, vehicleType, seatCapacity)
            flash('Vehicle Details Added Successfully', 'success')
            return redirect(url_for('home_admin'))
    return render_template('vehicledetails.html', showForm = showForm, form = form)

@app.route("/update-vehicle-details", methods=['GET','POST'])
def updatevehicledetails():
    showForm = "getVehicleDetails"
    form1 = GetVehicleForm()
    form2 = UpdateVehicleForm()
    formid = request.args.get('formid', 1, type=int)
    if formid == 2:
        print('-----------------------------------------------------UpdateVehicleFormSubmit')
        vehicleId = int(form2.vehId.data)
        vehicleName = str(form2.vehName.data)
        vehicleType = str(form2.vehType.data)
        makeCompany = str(form2.vehCompany.data)
        modelYear = int(form2.vehModel.data)
        currentMileage = float(form2.vehMileage.data)
        location = int(form2.vehLocation.data)
        timeLastServiced = datetime.strptime(str(form2.timeLastServiced.data), '%Y-%M-%d')
        registrationTag = str(form2.registrationTag.data)
        vehicleCondition = str(form2.vehCondition.data)
        seatCapacity = int(form2.seatCapacity.data)
        Admin.updateVehicleDetails(vehicleId, vehicleName, makeCompany, modelYear, currentMileage, location, timeLastServiced, registrationTag, vehicleCondition, vehicleType, seatCapacity)
        flash('Vehicle Details Updated Successfully', 'success')
        return redirect(url_for('home_admin'))
    elif form1.validate_on_submit() and formid == 1:
        print('-----------------------------------------------------UpdateVehicleForm')
        vehId = int(form1.vehId.data)
        vehicleObject = Admin.getVehicleDetails(vehId)
        if vehicleObject:
            showForm = "updateVehicleDetails"
            form = UpdateVehicleForm()
            form.vehId.data = vehicleObject.vehicle_id
            form.vehName.data = vehicleObject.vehicle_name
            form.vehCompany.data =  vehicleObject.make_company
            form.vehModel.data =  vehicleObject.model_year
            form.vehMileage.data =  vehicleObject.current_milegae
            form.vehLocation.data =  vehicleObject.Location
            form.timeLastServiced.data =  vehicleObject.last_service
            form.registrationTag.data =  vehicleObject.registration_tag
            form.seatCapacity.data =  vehicleObject.seat_capacity
            form.vehType.default =  vehicleObject.vehicle_type
            form.vehCondition.default =  vehicleObject.vehicle_condition
            return render_template('vehicledetails.html', showForm = showForm, form = form )
        else:
            flash('Enter a valid VehicleID', 'danger')
            showForm = "getVehicleDetails"
            return render_template('vehicledetails.html', showForm = showForm, form = form1)
    return render_template('vehicledetails.html', showForm = showForm, form = form1)

@app.route("/remove-vehicle-details", methods=['GET','POST'])
def removevehicledetails():
    showForm = "removeVehicleDetails"
    form = RemoveVehicleForm()
    if form.validate_on_submit():
        vehicleId = form.vehId.data
        isPresent = Admin.removeVehicleDetails(vehicleId)
        if isPresent:
            flash('Vehicle Details Deleted Successfully', 'success')
            return redirect(url_for('home_admin'))
        else:
            flash('Enter a valid VehicleID To Remove', 'danger')
            return render_template('vehicledetails.html', showForm = showForm, form = form)  #post
    return render_template('vehicledetails.html', showForm = showForm, form = form)  #post

@app.route("/vehicle-pricing", methods=['GET','POST'])
def vehicleprice():
    showForm = "getvehicletype"
    form1 = GetVehicleTypeForm()
    form2 = PriceForm()
    formid = request.args.get('formid', 1, type=int)
    if formid == 2 and form2.is_submitted():
        print(form2.data)
        price_id = int(form2.price_id.data)
        vehicleType = str(form2.vehicle_type.data)
        price = float(form2.price.data)
        firstDiscount = int(form2.FirstDiscount.data)
        secondDiscount = int(form2.SecondDiscount.data)
        thirdDiscount = int(form2.ThirdDiscount.data)
        Pricing.addRow(price_id, vehicleType, price, firstDiscount, secondDiscount, thirdDiscount)
        flash('Vehicle Price Added Successfully', 'success')
        return redirect(url_for('home_admin'))
    elif form1.validate_on_submit() and formid == 1:
        showForm = "addprice"
        form = PriceForm()
        if form1.vehicle_type.data=='SMALLCAR':
            form.price_id.data = 1
        elif form1.vehicle_type.data=='FULLSIZECAR':
            form.price_id.data = 2   
        elif form.vehicle_type.data=='TRUCK':
            form.price_id.data = 3
        elif form.vehicle_type.data=='LUXURYCAR':
            form.price_id.data = 4
        return render_template('vehicledetails.html', showForm = showForm, form=form)
    return render_template('vehicledetails.html', showForm = showForm, form=form1)

@app.route("/vehicle-pricing")
def updatevehiclepricing():
    showForm = "vehiclePricing"
    return render_template('vehicledetails.html', showForm = showForm)

@app.route("/rental-location", methods=['GET', 'POST'])
def rentallocation():
    showForm = "rentalLocation"
    form = VehicleLocationForm()
    if form.validate_on_submit():
        locId = form.locationId.data
        name = form.name.data
        address = form.address.data
        capacity = form.totalcapacity.data
        locObj = vehiclelocation(locId, name, address, capacity)
        vehiclelocation.addRow(locObj)
        flash('Location Details Added Successfully', 'success')
        return redirect(url_for('home_admin'))
    return render_template('vehicledetails.html', showForm = showForm, form = form)

@app.route("/edit-rental-location", methods=['GET', 'POST'])
def editrentallocation():
    showForm = "editrentalLocation"
    form1 = GetLocationForm()
    form2 = UpdateLocationForm()
    formid = request.args.get('formid', 1, type=int)
    if request.method == 'POST' and formid == 2:
        print(form2.locationId.data)
        locId = int(form2.locationId.data)
        name = str(form2.name.data)
        address = str(form2.address.data)
        capacity = int(form2.totalcapacity.data)
        locObj = vehiclelocation(locId, name, address, capacity)
        vehiclelocation.updateRow(locObj)
        flash('Location Details Updated Successfully', 'success')
        return redirect(url_for('home_admin'))
    elif form1.validate_on_submit() and formid == 1:
        locId = int(form1.locationId.data)
        showForm = "updaterentallocation"
        if VehicleLocation.isLocationPresent(locId):
            form = UpdateLocationForm()
            details = vehiclelocation.getLocationDetails(locId)
            form.locationId.data  =  details.location_id
            form.name.data = details.name
            form.address.data = details.address
            form.totalcapacity.data = details.total_capacity
            return render_template('vehicledetails.html', showForm = showForm, form = form )
        else:
            flash('Invalid Location ID', 'danger')
            showForm = "editrentalLocation"
            return render_template('vehicledetails.html', showForm=showForm, form=form1)
    return render_template('vehicledetails.html', showForm = showForm, form = form1)

@app.route("/remove-rental-location", methods=['GET', 'POST'])
def removerentallocation():
    showForm = "getrentalLocationtoremove"
    form1 = GetLocationRemovalForm()
    form2 = RemoveLocationForm()
    formid = request.args.get('formid', 1, type=int)
    if request.method == 'POST' and formid == 2:
        print(form2.locationId.data)
        locId = int(form2.locationId.data)
        vehiclelocation.deleteRow(locId)
        flash('Location Details Removed Successfully', 'success')
        return redirect(url_for('home_admin'))
    elif form1.validate_on_submit() and formid == 1:
        locId = form1.locationId.data
        showForm = "removerentallocation"
        if vehiclelocation.isLocation(locId):
            form = RemoveLocationForm()
            details = vehiclelocation.getLocationDetails(locId)
            form.locationId.data  =  details.location_id
            form.name.data = details.name
            form.address.data = details.address
            form.totalcapacity.data = details.total_capacity
            return render_template('vehicledetails.html', showForm = showForm, form = form)
        else:
            flash('Invalid Location ID To Remove', 'danger')
            showForm = "getrentalLocationtoremove"
            return render_template('vehicledetails.html', showForm=showForm, form=form1)
    return render_template('vehicledetails.html', showForm = showForm, form = form1)

@app.route("/remove-user")
def deleteuser():
    showForm = "deleteuser"
    userList = Admin.listUser()
    return render_template('vehicledetails.html', userList = userList, showForm = showForm) 

@app.route("/remove-user", methods=['POST'])
def deleteuseraction():
    showForm = "deleteuser"
    Admin.removeUser(str(request.form["userName"]))
    userList = Admin.listUser()
    return render_template('vehicledetails.html', userList = userList ,showForm = showForm) 

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/about_user")
def about_user():
    return render_template('about_user.html', title='About')

global book_data

@app.route("/book_user", methods = ['GET', 'POST'])
def book_user():
    global  book_data
    form1 = BookingForm()
    form2 = VehicleSearchForm()
    formid = request.args.get('formid', 1, type=int)
    showform = "search"
    if formid == 2:
        if (book_data):
            b = Booking(form2.data['vehicle_id'], current_user.id, book_data['date_pickup'], book_data['date_drop'], int(book_data['pickup_location']), '')
            b.confirmBooking()
            book_data = None
            flash('Vehicle Booking Successful', 'success')
            return redirect(url_for('home_user'))
    elif form1.validate_on_submit() and formid==1:
        book_data = form1.data
        rows = Search.searchByType(form1.cartype.data)
        if (len(rows) == 0):
            flash('No Vehicle of this type is available with us now', 'danger')
        else:
            rows_2 = Search.searchByLocationandType(int(form1.pickup_location.data), rows)
            if (len(rows_2) == 0):
                #rows = rows_2
                flash('Vehicle of this type is available only in these location', 'danger')
            else:
                rows_3 = Search.searchByAvailability(form1.date_pickup.data, form1.date_drop.data, rows_2)
                if (len(rows_3) > 0):
                    flash('Vehicle(s) is available', 'success')
                    rows = rows_3
                else:
                    flash('Unavailable at this Pickup Time. we are recommending these vehicles', 'danger')
                    for type in VehicleType:
                        if (type.name != form1.cartype.data):
                            rows_4 = Search.searchByType(type.name)
                            if (len(rows_4) > 0):
                                rows = rows_4
                                break
        showform = "vehicles"
        names = []
        if (len(rows) > 0):
            for row in rows:
                names.append(vehiclelocation.getLocationDetails(row.Location).name)
        return render_template('book_user.html', form=form1, form2=form2, showform=showform, results=zip(rows,names))
    return render_template('book_user.html', title='bookings', form=form1, showform=showform)

@app.route("/book")
def book():
    flash('Please Login to Book Vehicles', 'success')
    return redirect(url_for('login'))

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

@app.route("/contact_user")
def contact_user():
    return render_template('contact_user.html', title='Contact')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        customer = User(form.username.data, form.firstname.data, form.lastname.data, form.email.data, form.password.data, form.age.data, form.driverId.data, form.address.data, "WAITING")
        customer.insertRow()
        flash('Your account has been created! Please pay $600 to activate your account', 'success')
        return redirect(url_for('membership'))
    return render_template('register.html', title='Register', form=form)

@app.route('/membership')
def membership():
    return render_template('membership.html', key=stripe_keys['publishable_key'])


@app.route('/payment')
def payment():
    form = FinalPaymentForm()
    form.price.data = float(request.args.get('data'))
    return render_template('payment.html', key=stripe_keys['publishable_key'],form=form)

@app.route('/pay', methods=['POST'])
def pay():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=60000,
        currency='usd',
        description='Membership Fees'
    )
    return redirect(url_for('login'))

@app.route('/finalpay', methods=['GET','POST'])
def finalpay():
    form = FinalPaymentForm()
    global bookid
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    form.price.data = 60000

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=form.price.data,
        currency='usd',
        description='Booking Fee'
    )
    flash('Your Payment successful','success')
    bookings.cancelBooking(bookid)
    return redirect(url_for('home_user'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_user'))
    form = LoginForm()
    if form.email.data == 'admin@gmail.com' and form.password.data == 'password':
        flash('You have been logged in!', 'success')
        return redirect(url_for('home_admin'))

    if form.validate_on_submit():
        email = None
        if (User.isEmailPresent(form.email.data)):
            email = form.email.data
        if (User.authenticateUser(email, form.password.data)):
            if email:
                userobj = User.getRow(email)
                userobj.authenticated = True
                login_user(userobj, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home_user'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'success')
    return render_template('login.html', title='Login', form=form)

@app.route("/vechicle")
def vehicle():
    return render_template('vehicle.html', title='Vehicle')

@app.route("/location")
def location():
    return render_template('location.html', title='Location')

@app.route("/user")
def user():
    return render_template('user.html', title='User')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/user_account")
# @login_required
def user_account():
    return render_template('user_account.html', title='User_Account')