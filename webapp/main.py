# Braden Johnston 20005898
# 159352 AS2 Semester 1 2022

from datetime import timedelta
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = 'super secret key'  # arbitrary
possiblyCancelling = ''


def header(
        page):  # returns bar of menu buttons for easier navigation, inside statements control which buttons are active
    output = """<div class="topnav" id="topnav">"""
    if page == 'welcomeonly':  # home button only, the rest are disabled. Used in login and sign up screens
        return (
                '<div class="topnav" id="topnav"><a href="/welcome">Home</a>' + '<a class="disabled">Book</a>' + '<a class="disabled">Profile</a>' +
                '<a class="rightdisabled">Sign Out</a><i class="fa fa-bars"></i></a></div>')

    if page == 'welcome':  # home button is highlighted
        output += """<a href="/welcome" class="active">Home</a>"""
    else:
        output += """<a href="/welcome" >Home</a>"""
    if page == 'book':  # book button is highlighted
        output += """<a href="/book" class="active">Book</a>"""
    else:
        output += """<a href="/book" >Book</a>"""
    if page == 'profile':  # profile button is highlighted
        output += """<a href="/profile" class="active">Profile</a>"""
    else:
        output += """<a href="/profile" >Profile</a>"""

    output += """<a href="/signout" class="right">Sign Out</a> 
            <a href="javascript:void(0);" class="icon" onclick="myFunction()"><i class="fa fa-bars"></i></a></div>"""

    return output


db = SQLAlchemy(app)

style = """<head>
    <style>
    body {
        background-color: lightblue;
        text-align: center;
    }
    
    .bodytext {
        padding-top: 30px;
        padding-left: 30px;
        font-family: "Gill Sans", sans-serif;
    }
        
    .bodytext.invoice {
        background-color: #e0f8ff;
        height: 80%;
        margin-top: 5%;
        margin-left: 15.6%;
        margin-right: 15.6%;
        padding-left: 2.6%;
        padding-right: 2.6%;
        border: 1px solid grey;
        border-radius: 10px;
    }
    
    .bodytext.invoice span {
        color: green;
        float: right;
        font-size: 20px;
        }
    
    
    .flight {
        text-align: left;
        border-top: 1px solid grey;
        border-bottom: 1px solid grey;
        font-family: 'Courier New', monospace;
    }
    
    .profiletext {
        padding-top: 30px;
        padding-left: 30px;
        font-family: "Gill Sans", sans-serif;
        
    }
    
    .leftcol {
        width: 50%;
        float: left;
        }
    
    .rightcol {
        width: 50%;
        float: right;
    }
    
    .profiletext.flight {
        float: center;
        width: 90%;
        text-align: left;
        border: 1px solid grey;
        font-family: 'Courier New', monospace;
        background-color: #e0f8ff;
        padding-right: 0.52%;
        padding-bottom: 0.52%;
        padding-left: 1%;
        padding-top: 0.1%;
    }
    
    .profiletext.flight span {
        color: green;
        float: right;
        font-size: 20px;
    }
    
    .flight span {
        color: green;
        float: right;
        font-size: 20px;
    }
    
    .flight + .flight {
        border-top: 1px solid transparent
        }
        
    .rightpadding {
        padding-top: 15px;
        text-align: center;
        height: 70%;
        
    }
    
    .money {
        color: green;
        font-weight: bold;
        display:inline;
    }
    
    .button {
          background-color: #1E3684;
          border: none;
          color: white;
          padding: 16px 32px;
          text-align: center;
          font-size: 16px;
          margin: 4px 2px;
          opacity: 0.6;
          transition: 0.3s;
          display: inline-block;
          text-decoration: none;
          cursor: pointer;
        }
        
        .redbutton {
          background-color: #b0040d;
          border: 1px solid black;
          color: white;
          padding: 16px 32px;
          text-align: center;
          font-size: 16px;
          margin: 4px 2px;
          opacity: 0.6;
          transition: 0.3s;
          display: inline-block;
          text-decoration: none;
          cursor: pointer;
        }
        
    .button.sameline {
        display: inline;
        
     }   
        
    .topnav {
          background-color: #010536;
          overflow: hidden;
        }
    .topnav a {
          float: left;
          display: block;
          color: #f2f2f2;
          text-align: center;
          padding: 14px 16px;
          text-decoration: none;
          font-size: 17px;
        }
    .topnav a:hover {
          background-color: #ddd;
          color: black;
        }
    .topnav a.active {
          background-color: #1d44c4;
          color: white;
        }
    .topnav .icon {
          display: none;
        }
    .topnav a.right {
          float: right;
        }
        
    .topnav a.disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }
        
    .topnav a.rightdisabled {
          float: right;
          opacity: 0.6;
          cursor: not-allowed;
        }

        .button:hover {opacity: 1}
        .redbutton:hover {opacity: 1}
    </style>
    <title>Airbitrary Booking</title>
</head>
<body>"""  # absolute mess, my apologies


class Customers(db.Model):  # customers sql table for managing users' data
    _id = db.Column("id", db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    user = db.Column(db.String(100))
    passw = db.Column(db.String(100))
    flights = db.Column(db.String(100))

    def __init__(self, fname, lname, user, passw):
        self.fname = fname
        self.lname = lname
        self.user = user
        self.passw = passw

    def get(self):
        return {'id': self._id, 'fname': self.fname, 'lname': self.lname, 'user': self.user, 'passw': self.passw,
                'flights': self.flights}  # single get function returns all info, requires usage like user.get().get('lname')


class Planes(db.Model):  # planes sql table for referring to planes' data (never altered)
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    title = db.Column(db.String(15))
    passengers = db.Column(db.Integer)

    def __init__(self, name, title, passengers):
        self.name = name
        self.title = title
        self.passengers = passengers

    def get(self):
        return {'id': self._id, 'name': self.name, 'title': self.title, 'passengers': self.passengers}


class Flights(db.Model):  # flights sql table for managing outgoing flights and their data
    _id = db.Column("id", db.Integer, primary_key=True)
    planeid = db.Column(db.Integer)
    startplace = db.Column(db.String(4))
    endplace = db.Column(db.String(4))
    day = db.Column(db.String(10))
    starttime = db.Column(db.String(13))
    endtime = db.Column(db.String(13))
    passengers = db.Column(db.String(15))
    image = db.Column(db.String(25))
    price = db.Column(db.String(5))
    startplacetext = db.Column(db.String(20))
    endplacetext = db.Column(db.String(20))

    def __init__(self, planeid, startplace, endplace, day, starttime, endtime, passengers, image, price, startplacetext,
                 endplacetext):
        self.planeid = planeid
        self.startplace = startplace
        self.endplace = endplace
        self.day = day
        self.starttime = starttime
        self.endtime = endtime
        self.passengers = passengers
        self.image = image
        self.price = price
        self.startplacetext = startplacetext
        self.endplacetext = endplacetext

    def get(self):
        return {'id': self._id, 'planeid': self.planeid, 'startplace': self.startplace, 'endplace': self.endplace,
                'day': self.day, 'starttime': self.starttime, 'endtime': self.endtime, 'passengers': self.passengers,
                'image': self.image, 'price': self.price, 'startplacetext': self.startplacetext,
                'endplacetext': self.endplacetext}


@app.route('/welcome', methods=['GET', 'POST'])  # landing URI can return two different pages
def welcome():
    if "user" not in session:  # one if the user is not logged in
        return header('welcomeonly') + style + '<div class="bodytext">' + """<h1>Hello and welcome to the Airbitrary booking website! (Landing page)</h1><br>
                <form action='login' method="POST" style="display: inline;"><button class="button sameline" type="submit">Login</button></form>
                <form action='signup' method="POST" style="display: inline;"><button class="button sameline" type="submit">Sign up</button></form>
                <br><img class="rightpadding" src="static/landing.jpg">"""

    else:  # and one if they are not
        return header('welcome') + style + '<div class="bodytext">' + (
                '<body><h1>Nice to see you ' + session['user'].get('fname') +
                '!</h1>\nWhat would you like to do?<br>' +
                '<form action="book" method="POST"><button class="button" type="submit">Book a '
                'flight</button></form>' +
                '<form action="status" method="POST">' +
                '<label for="ticket">Check ticket status: </label>' +
                '<input type="input" placeholder="Ticket number" name="ticket" required>' +
                '<br><button class="button" type="submit">Submit</button>' +
                '</form></body>')


@app.route('/login', methods=['GET', 'POST'])
def login():  # login page
    return style + header('welcomeonly') + '<div class="bodytext">' + """<form action='checklogin' method="POST">
                    <div class="container">
                        <label for="uname"><b>Username: </b></label>
                        <input type="text" placeholder="Enter Username" name="uname" required><br><br><br>
                        <label for="psw"><b>Password: </b></label>
                        <input type="password" placeholder="Enter Password" name="psw" required><br><br><br><br>
                        <button class="button" type="submit">Login</button>
                      </div>
                </form>"""


@app.route('/checklogin', methods=['GET', 'POST'])
def checkLogin():  # does the logic for the login process
    user = request.form.get('uname')
    pwd = request.form.get('psw')  # get entered username and password from POST request

    found_user = Customers.query.filter_by(user=user).first()  # find if there is a matching user

    if found_user:  # if there is:
        if found_user.passw == pwd:  # and the password also matches
            session['id'] = found_user.get().get('id')  # set session variables for easy access to current user
            session['user'] = found_user.get()
            return welcome()  # welcome page will be logged-in version
    return login() + "<script>alert('Username/Password combination does not match any recorded user')</script>"  # otherwise let them try again


@app.route('/signup', methods=['GET', 'POST'])
def signup():  # signup page with 4 text inputs for user info
    return header('welcomeonly') + style + '<div class="bodytext">' + """<form action='doSignup' method="POST">
                    <div class="container">
                        <label for="uname"><b>Username: </b></label>
                        <input type="text" name="uname" required><br><br>
                        <label for="psw"><b>Password: </b></label>
                        <input type="password" name="psw" required><br><br>
                        <label for="fname"><b>First Name: </b></label>
                        <input type="text" name="fname" required><br><br>
                        <label for="lname"><b>Last Name: </b></label>
                        <input type="text" name="lname" required><br><br>
                        <button class="button" type="submit">Sign Up</button>
                      </div>
                </form>"""


@app.route('/doSignup', methods=['GET', 'POST'])
def doSignup():  # does the logic for the login process
    user = request.form.get('uname')
    pwd = request.form.get('psw')
    fname = request.form.get('fname')
    lname = request.form.get('lname')  # get entered user info from POST request

    found_user = Customers.query.filter_by(user=user).first()  # see if there is an existing user by that username

    if found_user:  # if there is
        return header(
            'welcome') + signup() + "<script>alert('That username is taken!')</script>"  # alert them and let them try again
    else:
        usr = Customers(fname, lname, user, pwd)  # otherwise create another entry in the customers table
        db.session.add(usr)  # add user to database and commit changes
        db.session.commit()

    return "<h1>Signed up successfully!</h1><br>" + login()


@app.route('/book', methods=['GET', 'POST'])
def book():  # book page with dropdown lists to choose departing and arriving airports
    if 'user' not in session:
        return login()

    return header('book') + style + '<div class="bodytext">' + """<form action="doBook" method="POST">
              <label for="Dairport">Choose a departure airport (from):</label>
              <select name="Dairport" id="Dairport">
                <option value="NZNE">Dairy Flat (NZNE)</option>
                <option value="YSSY">Sydney (YSSY)</option>
                <option value="NZRO">Rotorua (NZRO)</option>
                <option value="NZCI">Tuuta (NZCI)</option>
                <option value="NZTL">Lake Tekapo (NZTL)</option>
                <option value="NZGB">Claris (NZGB)</option>
              </select>
              <br>
              <label for="Aairport">Choose an arrival airport (to):</label>
              <select name="Aairport" id="Aairport">
                <option value="NZNE">Dairy Flat (NZNE)</option>
                <option value="YSSY">Sydney (YSSY)</option>
                <option value="NZRO">Rotorua (NZRO)</option>
                <option value="NZCI">Tuuta (NZCI)</option>
                <option value="NZTL">Lake Tekapo (NZTL)</option>
                <option value="NZGB">Claris (NZGB)</option>
              </select>
              <br><br>
              
              <button class='button' type="submit">Search</button>
            </form>"""


@app.route('/doBook', methods=['GET', 'POST'])
def doBook():  # lists the results found for the POSTed airports
    if 'user' not in session:
        return login()  # send user to login page if they need to login

    results = []  # holds flights need to be displayed
    start = request.form.get('Dairport')
    end = request.form.get('Aairport')  # get desired start and end locations

    for flight in Flights.query.all():  # for all flights
        if flight.get().get('startplace') == start and flight.get().get(
                'endplace') == end:  # if there is a direct route
            planeid = flight.get().get('planeid')  # take it
            for tempplane in Planes.query.all():
                if tempplane.get().get('id') == planeid:
                    plane = tempplane

            if flight.get().get('passengers') is not None:  # and the flight has an empty seat
                if len(flight.get().get('passengers').split(",")) < plane.get().get('passengers'):
                    results.append([flight, plane])  # add flight to the list to show user
            else:
                results.append([flight, plane])

        elif flight.get().get(
                'startplace') == start:  # otherwise if the start location matches and not the end location
            planeid = flight.get().get('planeid')  # add this flight as a possible layover connecting flight
            layover = flight.get().get('endplace')
            for layoverflight in Flights.query.all():  # and then for all flights again
                if layoverflight.get().get('startplace') == layover and layoverflight.get().get(
                        'endplace') == end:  # flight connects the first flight and the desired end location
                    layoverplaneid = layoverflight.get().get('planeid')
                    for tempplane in Planes.query.all():
                        if tempplane.get().get('id') == layoverplaneid:
                            layoverplane = tempplane
                        if tempplane.get().get('id') == planeid:
                            plane = tempplane
                    results.append([flight, plane, layoverflight, layoverplane])  # add flights to the results list

    output = book()
    removing = []
    if len(results) == 0:  # if there are no results
        return book() + '<script>alert("Flights search acquired 0 results.")</script>'

    for result in results:  # check once more for open seats
        removed = False
        if result[0].get().get('passengers'):
            if len(result[0].get().get('passengers').split(',')) >= result[1].get().get('passengers'):
                removing.append(result)
                removed = True
        if len(result) > 2:
            if result[2].get().get('passengers') and not removed:
                if len(result[2].get().get('passengers').split(',')) >= result[3].get().get('passengers'):
                    removing.append(result)

    for remove in removing:
        results.remove(remove)  # remove the item from results list

    if len(results) == 0:
        output += '<br><br><h2>No available flights were found.</h2><br>'

    if len(results) != 0:
        image = results[0][0].get().get('image')
        output += "<div class='bodytext'> <img src='" + image + "'><br><form action='confirmBook' method='POST'>"

        output += '<br><br><h2>' + str(len(results)) + ' Flight(s) found!</h2><br>'  # show how many results there are

    for flight in results:  # for all results
        if len(flight) == 2:  # if it is not a connecting flight
            output += ('<input type="checkbox" id="' + str(flight[0].get().get('id')) + '" name="' +
                       str(flight[0].get().get('id')) + '">' +
                       '<label for="' + str(flight[0].get().get('id')) + flight[0].get().get('day') + '"> ' + flight[
                           0].get().get('startplacetext') + ' to ' +
                       flight[0].get().get('endplacetext') + ' ' + flight[0].get().get('day') + ' ' + flight[
                           0].get().get(
                        'starttime') + ' until ' +
                       flight[0].get().get('endtime') + ' aboard the ' + flight[1].get().get('title') + ' ' +
                       flight[1].get().get('name') + ' - <div class="money">$' + flight[0].get().get(
                        'price') + 'NZD</div></label><br>')  # print it like this, im so sorry about the messy concatenations

        elif len(flight) == 4:  # if it is a multi-legged flight
            image2 = flight[2].get().get('image')
            flightid = str(flight[0].get().get('id')) + '-' + str(flight[2].get().get('id'))
            output += (
                    '<img src="' + image2 + '"><br><input type="checkbox" id="' + flightid + '" name="' + flightid + '">' +
                    '<label for="' + str(flight[0].get().get('id')) + flight[0].get().get('day') + '-' +
                    str(flight[2].get().get('id')) + flight[2].get().get('day') + '"> ' + "CONNECTING flights " +
                    flight[0].get().get('startplacetext') + ' to ' + flight[0].get().get('endplacetext') + ' ' +
                    flight[0].get().get('day') + ' ' + flight[0].get().get('starttime') + ' until ' +
                    flight[0].get().get('endtime') + ' aboard the ' + flight[1].get().get('title') + ' ' +
                    flight[1].get().get('name') + "<br> THEN " + flight[2].get().get('startplacetext') + ' to ' +
                    flight[2].get().get('endplacetext') + ' ' + flight[2].get().get('day') + ' ' +
                    flight[2].get().get('starttime') + ' until ' + flight[2].get().get('endtime') + ' aboard the ' +
                    flight[3].get().get('title') + ' ' + flight[3].get().get('name') +
                    ' - $' + flight[0].get().get('price') + ' + $' + flight[2].get().get(
                'price') + ' = <div class="money">$' + str(
                float(flight[0].get().get('price')) + float(
                    flight[2].get().get('price'))) + 'NZD</div></label><br>')  # print differently

    if len(results) > 0:
        output += "<button class='button' type='submit'>Book</button></form>"  # confirm booking button

    return style + output


@app.route('/confirmBook', methods=['GET', 'POST'])
def confirmBook():
    if 'user' not in session:
        return style + login()  # send user to login page if they need to login

    bookingNum = None
    bookinglist = []
    flightlist = []

    for chosenflights in request.form.to_dict().keys():  # get selected flights to book from selected flights
        if len(chosenflights) == 1:  # if current flight is direct
            flightlist.append(chosenflights)  # add it to flight list
        else:  # otherwise
            for tempflight in chosenflights.split(
                    '-'):  # split the multi-legged flight (stored as 23-10) if 23 and 10 were the two flights
                flightlist.append(tempflight)  # and add them both to the flight list

    for flightnum in flightlist:  # for all flights in list
        flight = Flights.query.filter_by(_id=int(flightnum)).first()  # get the flight object
        if str(flight.get().get('id')) in flightlist:  # it should be
            for plane in Planes.query.all():  # get plane for the given flight
                if plane.get().get('id') == flight.get().get('planeid'):
                    planename = plane.get().get('name')
                    passengers = 0
                    if flight.get().get('passengers') is not None:  # check once again for spare seats on the plane
                        passengers = len(flight.get().get('passengers').split(','))
                        if int(plane.get().get('passengers')) <= passengers:
                            return book() + ('<script>alert("The selected flight (ID ' + str(flight.get().get('id')) +
                                             ') has no more seats available.") </script>')

            bookingNum = (str(flight.get().get('id'))) + '-' + str(session['id']) + '-' + planename + str(
                passengers + 1)  # create booking number for this user for this flight
            bookinglist.append(bookingNum)  # add it to the list of bookings we are currently making
            index = 0
            found = False
            while not found:  # I could have queried for the user a lot easier than this but here we are
                user = Customers.query.all()[index]
                if user.get().get('id') == session['id']:
                    found = True
                index += 1

            if session['user'].get('flights') is not None:  # add flight to users flights, formatted correctly
                setattr(user, 'flights', session['user'].get('flights') + ',' + bookingNum)
            else:
                setattr(user, 'flights', bookingNum)

            if flight.get().get('passengers') is None:  # add passenger to flights passengers, formatted correctly
                setattr(flight, 'passengers', session['user'].get('id'))
            else:
                setattr(flight, 'passengers',
                        str(flight.get().get('passengers')) + ',' + str(session['user'].get('id')))

            db.session.commit()  # commit changes
            session['user'] = user.get()  # user object is slightly different now, so we refresh the reference

    if bookingNum is None:
        return book() + "<script>alert('Please select a flight to book.')</script>"

    return invoice(bookinglist)


@app.route('/invoice', methods=['GET', 'POST'])
def invoice(bookings):  # invoice page, spent a long time trying to implement a download button with, to no avail
    total = 0.0  # keeps a running total of the individual flights for overall total display
    output = (style + header('book') +
              '<div class="bodytext invoice"><h1>Invoice Summary:</h1><br><h2 style="text-align: '
              'left">Flights:</h2><br>')

    for booking in bookings:  # for every booking that the user made
        flight = Flights.query.filter_by(_id=booking.split('-')[0]).first()  # get the flight
        flightdata = flight.get()
        total += float(flightdata.get('price'))
        output += ('<div class="flight"><h3><strong>' + (
                flightdata.get('startplacetext') + '</strong> to <strong>' + flightdata.get(
            'endplacetext')) + '</h3><p style="text-align: right;">Booking number: ' + booking + '</p>' +
                   flightdata.get('starttime') + ' until ' + flightdata.get('endtime') + '<span>$' + flightdata.get(
                    'price') + 'NZD</strong></span></div>')  # display each booking

    output += ('<h3 style="text-align: left;"><strong>Total:<span>$' + str(total) + 'NZD</strong></span></h3>' +
               """<form action="/profile"><button class="button">View Bookings</button></form></div></div>""")  # display total and link a button to the profile page

    return output


@app.route('/status', methods=['GET', 'POST'])
def status():  # shows user the status of a given booking
    if 'user' not in session:
        return login()  # send user to login page if they need to login
    booking = request.form.to_dict().get('ticket')
    bookingSplit = booking.split(
        '-')  # get inputted booking from POST request and split into easier to read bits of information

    for flight in Flights.query.all():  # for all flights
        if flight.get().get('id') == int(bookingSplit[0]):  # if flight matches that on booking number
            for passenger in flight.get().get('passengers').split(
                    ','):  # check if this user is a listed passenger of that flight
                if passenger == str(session['id']):
                    departtime = flight.get().get('day') + ' at ' + flight.get().get('starttime')
                    departplace = flight.get().get('startplace')
                    return ('<div class="bodytext">' + "Your booked flight (" + booking + ")<br>" +
                            "is set to depart from " + departplace + " on " + departtime) + cancel(
                        booking)  # they have a chance to cancel the ticket here

    return welcome() + '<script>alert("Given ticket number either does not exist or does not belong to you.")</script>'


@app.route('/cancel', methods=['GET', 'POST'])
def cancel(booking):
    if 'user' not in session:
        return login()  # send user to login page if they need to login
    global possiblyCancelling
    possiblyCancelling = booking  # global booking updated upon reaching this page, the only path to the cancel code
    return style + '<div class="bodytext">' + """<br>Would you like to cancel this trip?<br>
                        <form action="doCancel" method="POST">
                        <button id='yes' class="button" type="submit" name='yes'>Yes</button>
                        <button id='no' class="button" type="submit" name='no'>No</button></form>"""


@app.route('/doCancel', methods=['GET', 'POST'])
def doCancel():  # cancel code
    if 'user' not in session:
        return login()  # send user to login page if they need to login
    cost = 0  # refund amount
    try:
        if request.form.to_dict()['no']:
            return welcome()  # if they don't want to cancel, send them back to welcome page
    except KeyError:  # if they selected 'yes'
        booking = possiblyCancelling.split('-')  # get the booking to cancel
        for flight in Flights.query.all():  # remove passenger from flight's passengers
            if str(flight.get().get('id')) == booking[0]:
                cost += float(flight.get().get('price'))
                passengerlist = flight.get().get('passengers').split(',')
                setattr(flight, 'passengers', None)
                passengerlist.remove(str(session['id']))
                if '' in passengerlist:
                    passengerlist.remove('')
                passengerstring = ''
                for passenger in passengerlist:
                    passengerstring += passenger
                    if passenger != passengerlist[-1]:
                        passengerstring += ','

                setattr(flight, 'passengers', passengerstring)

            if len(booking) == 4:  # remove from both flights if multi-legged
                if str(flight.get().get('id')) == booking[1]:
                    cost += float(flight.get().get('price'))
                    passengerlist = flight.get().get('passengers').split(',')
                    setattr(flight, 'passengers', None)
                    passengerlist.remove(str(session['id']))
                    if '' in passengerlist:
                        passengerlist.remove('')
                    passengerstring = ''
                    for passenger in passengerlist:
                        passengerstring += passenger
                        if passenger != passengerlist[-1]:
                            passengerstring += ','

                    setattr(flight, 'passengers', passengerstring)

        user = Customers.query.filter_by(_id=session['id']).first()

        flightlist = user.get().get('flights').split(',')
        flightlist.remove(possiblyCancelling)
        flightstring = ''
        if '' in flightlist:  # remove flight from user's flight list
            flightlist.remove('')
        for tempflight in flightlist:
            flightstring += tempflight
            if tempflight != flightlist[-1]:
                flightstring += ','

        setattr(user, 'flights', flightstring)
        session['user'] = user.get()
        db.session.commit()

        return (welcome() + "Ticket '" + possiblyCancelling + "' has been cancelled!<br>" +
                "You will be refunded a total of <div class='money'>$" + str(
                    cost)) + " NZD</div>"  # display refund amount
    return welcome()  # return to welcome page


@app.route('/profile', methods=['GET', 'POST'])
def profile():  # profile page, see bookings, update info, delete account
    if 'user' not in session:
        return login()  # send user to login page if they need to login

    # javascript used for account deletion
    output = ("""<script>function ask() {  
    response = window.confirm("Are you sure you want to delete your account? This is irreversible!"); 
    if(!response){
        e.preventDefault();
    } else {
    window.location.pathname = '/delete'
    }}
                </script>""" + style + header('profile') +
              '<div class="profiletext"><div class="leftcol"><h2 style="text-align:center;">Your Bookings:</h2><br>')

    # LEFT SIDE
    try:  # only throws an exception if there are no flights
        for booking in session['user'].get('flights').split(
                ','):  # display all bookings in a similar style to that of the invoice
            flight = Flights.query.filter_by(_id=booking.split('-')[0]).first()
            flightdata = flight.get()
            output += ('<div class="profiletext flight"><h3><strong>' + (
                    flightdata.get('startplacetext') + '</strong> to <strong>' + flightdata.get(
                'endplacetext')) + '<form action="/status" method="POST"><button name="ticket" style="color:white;background-color:red;display:inline;margin-left:50%;"value="' + booking + '">CANCEL</button></form></h3>' +
                       '<p style="text-align: right;">Booking number: ' + booking + '</p>' + flightdata.get('starttime')
                       + ' until ' + flightdata.get('endtime') + '<span>$' + flightdata.get(
                        'price') + 'NZD</strong></span></div>')

    except AttributeError:
        output += 'Empty! Looks like time to make a booking :D'

    # RIGHT SIDE
    output += ('</div><div class="rightcol"><h2 style="text-align:center;">Update your information:</h2><br>' +
               '<form action="update" method="POST"><label for="uname"><b>Username: </b></label><input type="text" '
               'name="uname" value="' + session['user'].get('user') + '" required><br><br>' +
               '<label for="psw"><b>Password: </b></label><input type="text" name="psw" value="' + session['user'].get(
                'passw') + '" required><br><br>' +
               '<label for="fname"><b>First Name: </b></label><input type="text" name="fname" value="' + session[
                   'user'].get('fname') + '" required><br><br>' +
               '<label for="lname"><b>Last Name: </b></label><input type="text" name="lname" value="' + session[
                   'user'].get('lname') + '" required><br><br>' +
               '<button type="submit" class="button">Update</button></form><br><br><br>' +
               '<button type="submit" onclick="ask()" class="redbutton" >DELETE ACCOUNT</button>')  # allow user to update their profile

    return output + '</div></div>'


@app.route('/update', methods=['GET', 'POST'])
def update():  # user data updating logic
    if 'user' not in session:
        return login()  # send user to login page if they need to login

    data = request.form.to_dict()  # get all data from POST request

    new_fname = data.get('fname')
    new_lname = data.get('lname')
    new_uname = data.get('uname')
    new_psw = data.get('psw')  # store respectively

    user = Customers.query.filter_by(_id=session['id']).first()

    if new_uname != '':  # dict will have an empty key if they did not enter anything for a given input
        setattr(user, 'user', new_uname)
    if new_psw != '':  # if a new password is entered
        setattr(user, 'passw', new_psw)  # change it in the database
    if new_fname != '':
        setattr(user, 'fname', new_fname)
    if new_lname != '':
        setattr(user, 'lname', new_lname)

    db.session.commit()  # commit changes
    session['user'] = user.get()  # refresh user reference

    return profile() + 'Your information has been updated!'  # return them to profile screen


@app.route('/delete', methods=['GET', 'POST'])
def delete():  # delete user code
    for flight in Flights.query.all():
        passengerstring = ''  # remove this user from all existing flights
        try:
            if str(session['id']) in flight.get().get('passengers').split(','):
                for passenger in flight.get().get('passengers').split(','):
                    if passenger != str(session['id']):
                        passengerstring += passenger
                setattr(flight, 'passengers', passengerstring)
        except AttributeError:
            pass

    Customers.query.filter(Customers.user == session['user'].get('user')).delete()  # delete user
    db.session.commit()  # commit changes

    return 'Account successfully deleted!' + signout()  # do signout logic


@app.route('/signout', methods=['GET', 'POST'])
def signout():
    if 'user' in session:
        session.pop('user')  # remove session references
    if 'id' in session:
        session.pop('id')
    return welcome()  # logged out welcome page


app.add_url_rule('/', 'welcome', welcome)
app.add_url_rule('/', 'login', login)
app.add_url_rule('/', 'checklogin', checkLogin)
app.add_url_rule('/', 'signup', signup)
app.add_url_rule('/', 'doSignup', doSignup)
app.add_url_rule('/', 'book', book)
app.add_url_rule('/', 'doBook', doBook)
app.add_url_rule('/', 'confirmBook', confirmBook)
app.add_url_rule('/', 'status', status)
app.add_url_rule('/', 'cancel', cancel)
app.add_url_rule('/', 'doCancel', doCancel)
app.add_url_rule('/', 'signout', signout)
app.add_url_rule('/', 'profile', profile)
app.add_url_rule('/', 'invoice', invoice)
app.add_url_rule('/', 'update', update)
app.add_url_rule('/', 'delete', delete)

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8000)
