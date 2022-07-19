import os
import re
import secrets
import time
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from apps import app, db, bcrypt
from apps.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from apps.database import User, billinginput, deviceinput, real_data, real_dataSchema, TCN_data_predicted
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, datetime, timedelta
import numpy as np
#import pandas as pd
from colorama import Fore



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)

@app.route("/dashboard/")
@login_required
def dashboard():

    days1 = timedelta(days=1)
    days2 = timedelta(days=2)
    weeks1= timedelta(weeks=1)
    weeks2 = timedelta(weeks=2)
    month1 = timedelta(weeks=4)
    month2 = timedelta(weeks=8)

    today_date = date.today() - days1
    today = today_date.strftime("%Y-%m-%d")

    yesterday_date = date.today() - days2
    yesterday = yesterday_date.strftime("%Y-%m-%d")

    weks_list=[]
    for i in range(1,8):
        weekly_date = date.today() - timedelta(days=i)
        weeklyan = weekly_date.strftime("%Y-%m-%d")
        weks_list.append(weeklyan)
        #weks_list.strftime("%y-%m-%d")

    for i in range(8,15):
        yeswekkly_date = date.today() - timedelta(days=i)
        yesweeklyan = yeswekkly_date.strftime("%Y-%m-%d")


    monthly_date = date.today() - month1
    monthlylyan = monthly_date.strftime("%Y-%m-%d")

    yesmonthly_date = date.today() - month2
    yesmonthlyan = yesmonthly_date.strftime("%Y-%m-%d")

    # tarik data dari database disini buat today
    # today_data = dataall[dataall['Date'] == today_date]
    # tarik data dari database disini buat yesterday
    # yesterday_data = dataall[dataall['Date'] == yesterday]
    #for loop untuk bikin list yg isinya data dari query today & yesterday


    Kwh_kemarin = real_data.query.filter_by(Date = yesterday ).all()
    Kwh_hariIni = real_data.query.filter_by(Date = today ).all()

    kwh_weekly = real_data.query.filter_by(Date = weeklyan).all()
    yeskwh_weekly = real_data.query.filter_by(Date = yesweeklyan).all()

    kwh_monthly = real_data.query.filter_by(Date = monthlylyan).all()
    yeskwh_monthly = real_data.query.filter_by(Date = yesmonthlyan).all()

    today_list = []
    yesterday_list = []
    weekly_list = []
    yesweekly_list = []
    monthly_list = []
    yesmonthly_list = []

    for i in range(len(Kwh_hariIni)):
        today_list.append(Kwh_hariIni[i].Kwh)

    for i in range(len(Kwh_kemarin)):
        yesterday_list.append(Kwh_kemarin[i].Kwh)

    for i in range(len(kwh_weekly)):
        weekly_list.append(kwh_weekly[i].Kwh)

    for i in range(len(yeskwh_weekly)):
        yesweekly_list.append(yeskwh_weekly[i].Kwh)

    for i in range(len(kwh_monthly)):
        monthly_list.append(kwh_monthly[i].Kwh)

    for i in range(len(yeskwh_monthly)):
        yesmonthly_list.append(yeskwh_monthly[i].Kwh)

    rata2_today = np.mean(today_list)
    rata2_yesterday = np.mean(yesterday_list)
    todaykwh = "{:.2f}".format(rata2_today)

    rata2_weekly = np.mean(weekly_list)
    rata2_yesweekly = np.mean(yesweekly_list)
    weekly = "{:.2f}".format(rata2_weekly)

    rata2_monthly = np.mean(monthly_list)
    rata2_yesmonthly = np.mean(yesmonthly_list)
    monthly = "{:.2f}".format(rata2_monthly)

    if (rata2_today >  rata2_yesterday):
        selisih = ((rata2_today - rata2_yesterday)/rata2_today)
        selisih = round(selisih*100)
        selisih = str(selisih) + "% " + "Increase"
        
    elif (rata2_today < rata2_yesterday):
        selisih = ((rata2_today - rata2_yesterday)/rata2_today) 
        selisih = round(selisih*100)
        selisih = abs(selisih)
        selisih = str(selisih) + "% " + "Decrease"
    else:
        selisih = ((rata2_today - rata2_yesterday)/rata2_today)
        selisih = round(selisih*100)
        selisih = print("-")

    if (rata2_weekly >  rata2_yesweekly):
        selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly)
        selisihw = round(selisihw*100)
        selisihw = str(selisihw) + "% " + "Increase"

    elif (rata2_weekly < rata2_yesweekly):
        selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly) 
        selisihw = round(selisihw*100)
        selisihw = abs(selisihw)
        selisihw = str(selisihw) + "% " + "Decrease"
    else:
        selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly)
        selisihw = round(selisihw*100)
        selisihw = print("-")

    if (rata2_monthly >  rata2_yesmonthly):
        selisihm = ((rata2_monthly - rata2_yesmonthly)/rata2_monthly)
        selisihm = round(selisihm*100)
        selisihm = str(selisihm) + "% " + "Increase"

    elif (rata2_monthly < rata2_yesmonthly):
        selisihm = ((rata2_monthly - rata2_yesmonthly)/rata2_monthly) 
        selisihm = round(selisihm*100)
        selisihm = abs(selisihm)
        selisihm = str(selisihm) + "% " + "Decrease"
    else:
        selisihm = ((rata2_monthly - rata2_yesmonthly)/rata2_monthly)
        selisihm = round(selisihm*100)
        selisihm = print("-")


    # selisih = 24
    # realdata = real_data.query.all()
    # labels = real_data.query.with_entities(real_data.Date).all()
    # values = real_data.query.with_entities(real_data.Kwh).all()
    return render_template('dashboard.html', kwh_today=f"{selisih}", rata2_today=rata2_today, rata2_yesterday= rata2_yesterday, todaykwh=f"{todaykwh}", weeklykwh=f"{selisihw}", weekly=f"{weekly}", monthlykwh=f"{selisihm}", monthly=f"{monthly}")


@app.route('/get_data_lineChart')
@login_required
def get_data_lineChart():
    # labels = real_data.query.with_entities(real_data.Date).all()
    # values = real_data.query.with_entities(real_data.Kwh).all()
    
    # labels_data = json.dumps(real_data.serialize_list(labels))
    # values_data = json.dumps(real_data.serialize_list(values))

    # lineChartData = real_data.query.with_entities(real_data.Date, real_data.Time, real_data.Kwh)
    lineChartData = real_data.query.all()
    datetime = []
    kwh = []
    for i in range(len(lineChartData)):
        datetime.append(lineChartData[i].Date + " " + lineChartData[i].Time)
        kwh.append(lineChartData[i].Kwh)
    output_line = {"datetime": datetime, "Kwh" : kwh}
    # lineChartData_schema = real_dataSchema(many=True)
    # output = lineChartData_schema.dump(lineChartData)
    return jsonify(output_line)

@app.route('/api/data')
@login_required
def data():
    query = real_data.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            real_data.Date.like(f'%{search}%'),
            real_data.Time.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['Index', 'Date', 'Time', 'Kwh']:
            col_name = 'Date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(real_data, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [real_data.to_dict() for real_data in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': real_data.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@app.route("/algoritma1")
@login_required
def algoritma1():
    return render_template('algoritma1.html')

@app.route("/algoritma2")
@login_required
def algoritma2():
    return render_template('algoritma2.html')

@app.route("/algoritma3")
@login_required
def algoritma3():
    return render_template('algoritma3.html')

@app.route("/algoritma4")
@login_required
def algoritma4():
    return render_template('algoritma4.html')

@app.route('/get_data_tcnlineChart')
@login_required
def get_data_tcnlineChart():
    # labels = real_data.query.with_entities(real_data.Date).all()
    # values = real_data.query.with_entities(real_data.Kwh).all()
    
    # labels_data = json.dumps(real_data.serialize_list(labels))
    # values_data = json.dumps(real_data.serialize_list(values))

    # lineChartData = real_data.query.with_entities(real_data.Date, real_data.Time, real_data.Kwh)
    lineChartData = TCN_data_predicted.query.all()
    datetime = []
    predictions = []
    for i in range(len(lineChartData)):
        datetime.append(lineChartData[i].DateTime)
        predictions.append(lineChartData[i].Predictions)
    output_line = {"DateTime": datetime, "Predictions" : predictions}
    # lineChartData_schema = real_dataSchema(many=True)
    # output = lineChartData_schema.dump(lineChartData)
    return jsonify(output_line)

@app.route('/api/tcndata')
@login_required
def tcndata():
    query = TCN_data_predicted.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            TCN_data_predicted.DateTime.like(f'%{search}%'),
            TCN_data_predicted.Predictions.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['Date Time', 'Predictions']:
            col_name = 'DateTime'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(TCN_data_predicted, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [TCN_data_predicted.to_dict() for TCN_data_predicted in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': TCN_data_predicted.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route("/clustering")
@login_required
def clustering():
    return render_template('clustering.html')

@app.route("/compare")
@login_required
def compare():
    return render_template('compare.html')


@app.route("/schedule_appliance")
@login_required
def schedule_appliance():
    if current_user.user_type == 'user':
        all_data = deviceinput.query.filter_by(user_id=current_user.id).all()
        all_billing = billinginput.query.filter_by(user_id_bill=current_user.id).all()
    else:
        all_data = deviceinput.query.all()
        all_billing = billinginput.query.all()
    return render_template("scheduling.html", Devices=all_data, Billing=all_billing)
    # return render_template("scheduling.html")

@app.route('/api/billing')
@login_required
def billing():
    query = billinginput.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            billinginput.username.like(f'%{search}%'),
            billinginput.tarif_listrik.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['User ID', 'Username', 'Daya Listrik', 'Tagihan Listrik(RP)']:
            col_name = 'username'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(billinginput, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [billinginput.to_dict() for billinginput in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': billinginput.query.count(),
        'draw': request.args.get('draw', type=int),
    }

# this route is for inserting billing data
# to mysql database via html forms
@app.route('/insertBilling', methods=['POST'])
@login_required
def insertBilling():
    if request.method == 'POST':
        user_id_bill = current_user.id
        username = current_user.username
        tarif_listrik = request.form['tarif_listrik']
        tagihan_listrik = request.form['tagihan_listrik']
 
        my_billing = billinginput(user_id_bill, username, tarif_listrik, tagihan_listrik)
        db.session.add(my_billing)
        db.session.commit()
 
        flash("Billing Inserted Successfully", 'success')
 
        return redirect(url_for('schedule_appliance'))

#this is our update route where we are going to update our billing
@app.route('/updateBilling', methods = ['GET', 'POST'])
@login_required
def updateBilling():
 
    if request.method == 'POST':
        my_billing = billinginput.query.get(request.form.get('billing'))
 
        my_billing.tarif_listrik = request.form['tarif_listrik']
        my_billing.tagihan_listrik = request.form['tagihan_listrik']
 
        db.session.commit()
        flash("Billing Updated Successfully", 'success')
 
        return redirect(url_for('schedule_appliance'))

# This route is for deleting our employee
@app.route('/deleteBilling/<billing>/', methods=['GET', 'POST'])
@login_required
def deleteBilling(billing):
    my_billing = billinginput.query.get(billing)
    db.session.delete(my_billing)
    db.session.commit()
    flash("Billing Deleted Successfully", 'success')
 
    return redirect(url_for('schedule_appliance'))
 
# this route is for inserting device data
# to mysql database via html forms
@app.route('/insertDevice', methods=['POST'])
@login_required
def insertDevice():
    if request.method == 'POST':
        user_id = current_user.id
        username = current_user.username
        device_id = request.form['device_id']
        device_name = request.form['device_name']
        daya_device = request.form['daya_device']
        jumlah_device = request.form['jumlah_device']
        total_daya = float(daya_device)*int(jumlah_device)
        tingkat_prioritas = request.form['prioritas']
 
        my_data = deviceinput(user_id, username, device_id, device_name, daya_device, jumlah_device, total_daya, tingkat_prioritas)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Device Inserted Successfully", 'success')
 
        return redirect(url_for('schedule_appliance'))

@app.route('/api/appliance')
@login_required
def appliance():
    query = deviceinput.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            deviceinput.username.like(f'%{search}%'),
            deviceinput.tarif_listrik.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['User ID', 'Device ID', 'Device Name', 'Daya Device','Tingkat Prioritas', 'Action']:
            col_name = 'user_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(deviceinput, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [deviceinput.to_dict() for deviceinput in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': deviceinput.query.count(),
        'draw': request.args.get('draw', type=int),
    }

#this is our update route where we are going to update our employee
@app.route('/updateDevice', methods = ['GET', 'POST'])
@login_required
def updateDevice():
 
    if request.method == 'POST':
        my_data = deviceinput.query.get(request.form.get('id'))
 
        my_data.device_id = request.form['device_id']
        my_data.device_name = request.form['device_name']
        my_data.daya_device = request.form['daya_device']
        my_data.tingkat_prioritas = request.form['prioritas']
 
        db.session.commit()
        flash("Device Updated Successfully", 'success')
 
        return redirect(url_for('schedule_appliance'))

# This route is for deleting our employee
@app.route('/deleteDevice/<id>/', methods=['GET', 'POST'])
@login_required
def deleteDevice(id):
    my_data = deviceinput.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Device Deleted Successfully", 'success')
 
    return redirect(url_for('schedule_appliance'))

#admin page
@app.route("/admin")
@login_required
def admin():
    user_type = current_user.user_type
    if user_type == 'admin':
        all_data = User.query.all()
        return render_template('admin.html', userData=all_data)
    else:
        flash("Sorry you don't have permission to access this page", 'error')

@app.route('/insertUser', methods=['GET', 'POST'])
@login_required
def insertUser():
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf8')
        username = request.form['username']
        email = request.form['email']
        user_type = request.form['user_type']
        user = User(username=username, email=email, password=hashed_password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {username}!', 'success')
        return redirect(url_for('admin'))

@app.route('/updateUser', methods = ['GET', 'POST'])
@login_required
def updateUser():
 
    if request.method == 'POST':
        my_data = User.query.get(request.form.get('userEdit'))
 
        my_data.username = request.form['username']
        my_data.email = request.form['email']
        my_data.user_type = request.form['user_type']
 
        db.session.commit()
        flash("User Info Updated Successfully", 'success')
 
        return redirect(url_for('admin'))

# This route is for deleting our employee
@app.route('/deleteUser/<id>/', methods=['GET', 'POST'])
@login_required
def deleteUser(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User Deleted Successfully", 'success')
 
    return redirect(url_for('admin'))

    app.register_blueprint(blueprint, url_prefix="/api")

@app.route('/api/admin')
@login_required
def admintable():
    query = User.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            User.username.like(f'%{search}%'),
            User.tarif_listrik.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['User ID', 'Username', 'Email', 'User Type', 'Action']:
            col_name = 'username'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(User, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [User.to_dict() for User in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': User.query.count(),
        'draw': request.args.get('draw', type=int),
    }