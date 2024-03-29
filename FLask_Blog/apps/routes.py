# from asyncio.windows_events import NULL
import json
import os
import re
import secrets
import time
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from apps import app, db, bcrypt
from apps.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from apps.database import User, billinginput, deviceinput, real_data, real_dataSchema, TCN_data_predicted, TCN_data_predictedSchema,device_usage_duration, tcn_price, GRU_data_predicted, GRU_data_predictedSchema, RNN_data_predicted, RNN_data_predictedSchema, rnn_price, LMU_data_predicted, LMU_data_predictedSchema, lmu_price, gru_price, KlasterGdNPerhari, KlasterGdNPerhariSchema, KlasterVirtualPerhari, KlasterVirtualPerhariSchema, KlasterGdNPerbulan, KlasterGdNPerbulanSchema, KlasterVirtualPerbulan, KlasterVirtualPerbulanSchema, KlastergdNPertahun, KlastergdNPertahunSchema, KlasterVirtualPertahun, KlasterVirtualPertahunSchema
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date, datetime, timedelta
# import _overlapped
import numpy as np
import pandas as pd
from colorama import Fore
import sys
import babel.numbers

def Parsing_Data(data):
    # Feature Selection
    Data_pakai = data
    DateTime = Data_pakai['Date'] + ' ' + Data_pakai['Time']
    Data_pakai['DateTime'] = DateTime
    Data_pakai = Data_pakai.drop(columns="Date")
    Data_pakai = Data_pakai.drop(columns="Time")

    # Parsing DateTime
    format = '%Y-%m-%d %H:%M:%S'
    Data_pakai['DateTime'] = pd.to_datetime(Data_pakai['DateTime'], format=format, errors='coerce')
    Data_pakai = Data_pakai.set_index(Data_pakai['DateTime'])
    Data_pakai.drop(['DateTime'], axis=1, inplace=True)

    return Data_pakai

def date_time_split(data):
    Data_split = data
    Data_split.reset_index(inplace=True)
    Data_split[['Date', 'Time']] = Data_split['DateTime'].astype(str).str.split(" ", expand=True)
    Data_split = Data_split.drop(columns='DateTime')
    Data_split = Data_split.drop(columns=['Kwh','index'])
    return Data_split

def concat_date(bulan):
    range_date_bulan = bulan.reset_index()
    range_date_bulan = date_time_split(range_date_bulan)
    for i in range_date_bulan['Date'][:1]:
        first_date = i
    for j in range_date_bulan['Date'][-1:]:
        last_date = j
    month_range = str(first_date)+ ' -> '+ str(last_date)
    return month_range


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
        current_user.fullname = form.fullname.data
        current_user.company = form.company.data
        current_user.job = form.job.data
        current_user.nim = form.nim.data
        current_user.phone = form.phone.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.fullname.data = current_user.fullname
        form.company.data = current_user.company
        form.job.data = current_user.job
        form.nim.data = current_user.nim
        form.phone.data = current_user.phone
        form.about.data = current_user.about
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)

# @app.route('/updateProfile', methods = ['GET', 'POST'])
# @login_required
# def updateprofile():
#  
    # if request.method == 'POST':
        # my_data = User.query.get(request.form.get('userEdit'))
#  
        # my_data.username = request.form['username']
# 
        # my_data.email = request.form['email']
#  
        # db.session.commit()
        # flash("User Info Updated Successfully", 'success')
#  
        # return redirect(url_for('account'))

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

    weekly_date = date.today() - weeks1
    weeklyan = weekly_date.strftime("%Y-%m-%d")

    yeswekkly_date = date.today() - weeks2
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

    kwh_weekly = real_data.query.filter(real_data.Date >= weeklyan).all()
    yeskwh_weekly = real_data.query.filter(real_data.Date >= yesweeklyan).all()

    kwh_monthly = real_data.query.filter(real_data.Date >= monthlylyan).all()
    yeskwh_monthly = real_data.query.filter(real_data.Date >= yesmonthlyan).all()

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

    rata2_today = np.sum(today_list)
    rata2_yesterday = np.sum(yesterday_list)
    todaykwh = "{:.2f}".format(rata2_today)

    rata2_weekly = np.sum(weekly_list)
    rata2_yesweekly = np.sum(yesweekly_list)
    weekly = "{:.2f}".format(rata2_weekly)
    # weekly = weekly/len(weekly)

    rata2_monthly = np.sum(monthly_list)
    rata2_yesmonthly = np.sum(yesmonthly_list)
    monthly = "{:.2f}".format(rata2_monthly)

    if (rata2_today >  rata2_yesterday):
        selisih = ((rata2_today - rata2_yesterday)/rata2_today)
        selisih = round(selisih*100)
        selisih = str(selisih) + "% " 
        
    elif (rata2_today < rata2_yesterday):
        selisih = ((rata2_today - rata2_yesterday)/rata2_today) 
        selisih = round(selisih*100)
        selisih = abs(selisih)
        selisih = str(selisih) + "% "
    else:
        selisih = ((rata2_today - rata2_yesterday)/rata2_today)
        selisih = round(selisih*100)
        selisih = print("-")

    if (rata2_weekly >  rata2_yesweekly):
        selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly)
        selisihw = round(selisihw*100)
        selisihw = str(selisihw) + "% " 

    elif (rata2_weekly < rata2_yesweekly):
        selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly) 
        selisihw = round(selisihw*100)
        selisihw = abs(selisihw)
        selisihw = str(selisihw) + "% " 
    else:
        selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly)
        selisihw = selisihw*100
        selisihw = print("-")

    if (rata2_monthly >  rata2_yesmonthly):
        selisihm = ((rata2_monthly - rata2_yesmonthly)/rata2_monthly)
        selisihm = round(selisihm*100)
        selisihm = str(selisihm) + "% "

    elif (rata2_monthly < rata2_yesmonthly):
        selisihm = ((rata2_monthly - rata2_yesmonthly)/rata2_monthly) 
        selisihm = round(selisihm*100)
        selisihm = abs(selisihm)
        selisihm = str(selisihm) + "% "
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
    # output_line_filter = {}
    from_date = request.args.get('searchByFromdateLc')
    to_date = request.args.get('searchByTodateLc')
    # print(f'data linechart: from date type = {type(from_date)}, to date type = {type(to_date)}', file=sys.stderr)

    if from_date != None and to_date != None:
        lineChartData = real_data.query.filter(db.and_(
            real_data.Date >= from_date,
            real_data.Date <= to_date,
        )).all()
    else:
        lineChartData = real_data.query.all()

    datetime = []
    kwh = []
    for i in range(len(lineChartData)):
        datetime.append(lineChartData[i].Date + " " + lineChartData[i].Time)
        kwh.append(lineChartData[i].Kwh)
    output_line = {"datetime": datetime, "Kwh" : kwh}
    return jsonify(output_line)

def calculate_percentage(val, total):
   """Calculates the percentage of a value over a total"""
   percent = np.round((np.divide(val, total) * 100), 2)
   return percent

@app.route('/get_piechart_data')
def get_piechart_data():
   contract_labels = ['Kwh', 'Date', 'Time']
   _ = real_data.groupby('Date').size().values
   class_percent = calculate_percentage(_, np.sum(_)) #Getting the value counts and total

   piechart_data= []
   real_data(piechart_data, class_percent, contract_labels)
   return jsonify(piechart_data)

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

    # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            real_data.Date >= from_date,
            real_data.Date <= to_date,
        ))
    total_filtered = query.count()
    # print(f'data : {from_date}', file=sys.stderr)

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

@app.route("/algoritma1") #RNN
@login_required
def algoritma1():
    rnn_price_data = rnn_price.query.all()
    
    #Predict satu bulan kedepan
    one_month_price_data = rnn_price_data[0].Tarif
    one_month_price = babel.numbers.format_currency(one_month_price_data, "IDR", locale='id_ID')
    one_month_kwh_data = rnn_price_data[0].Total_Kwh
    one_month_kwh_data = "{:.2f}".format(one_month_kwh_data)
    one_month_range = rnn_price_data[0].range_date
        
    #Predict dua bulan kedepan
    two_month_price_data = rnn_price_data[1].Tarif
    two_month_price = babel.numbers.format_currency(two_month_price_data, "IDR", locale='id_ID')
    two_month_kwh_data = rnn_price_data[1].Total_Kwh
    two_month_kwh_data = "{:.2f}".format(two_month_kwh_data)
    two_month_range = rnn_price_data[1].range_date
        
    #Predict tiga bulan kedepan
    three_month_price_data = rnn_price_data[2].Tarif
    three_month_price = babel.numbers.format_currency(three_month_price_data, "IDR", locale='id_ID')
    three_month_kwh_data = rnn_price_data[2].Total_Kwh
    three_month_kwh_data = "{:.2f}".format(three_month_kwh_data)
    three_month_range = rnn_price_data[2].range_date
        
    #Predict empat bulan kedepan
    four_month_price_data = rnn_price_data[3].Tarif
    four_month_price = babel.numbers.format_currency(four_month_price_data, "IDR", locale='id_ID')
    four_month_kwh_data = rnn_price_data[3].Total_Kwh
    four_month_kwh_data = "{:.2f}".format(four_month_kwh_data)
    four_month_range = rnn_price_data[3].range_date
        
    #Predict lima bulan kedepan
    five_month_price_data = rnn_price_data[4].Tarif
    five_month_price = babel.numbers.format_currency(five_month_price_data, "IDR", locale='id_ID')
    five_month_kwh_data = rnn_price_data[4].Total_Kwh
    five_month_kwh_data = "{:.2f}".format(five_month_kwh_data)
    five_month_range = rnn_price_data[4].range_date
        
    #Predict enam bulan kedepan
    six_month_price_data = rnn_price_data[5].Tarif
    six_month_price = babel.numbers.format_currency(six_month_price_data, "IDR", locale='id_ID')
    six_month_kwh_data = rnn_price_data[5].Total_Kwh
    six_month_kwh_data = "{:.2f}".format(six_month_kwh_data)
    six_month_range = rnn_price_data[5].range_date
        
    return render_template('algoritma1.html', one_month_price=one_month_price, one_month_kwh_data=one_month_kwh_data, one_month_range=one_month_range,two_month_price=two_month_price, two_month_kwh_data=two_month_kwh_data, two_month_range=two_month_range,three_month_price=three_month_price,three_month_kwh_data=three_month_kwh_data, three_month_range=three_month_range,four_month_price=four_month_price, four_month_kwh_data=four_month_kwh_data, four_month_range=four_month_range, five_month_price=five_month_price, five_month_kwh_data=five_month_kwh_data, five_month_range=five_month_range, six_month_price=six_month_price, six_month_kwh_data=six_month_kwh_data, six_month_range=six_month_range)

@app.route('/get_data_rnnlineChart')
@login_required
def get_data_rnnlineChart():
    lineChartDataRNN = RNN_data_predicted.query.all()

    datetime = []
    kwh = []
    for i in range(len(lineChartDataRNN)):
        datetime.append(lineChartDataRNN[i].Date + " " + lineChartDataRNN[i].Time)
        kwh.append(lineChartDataRNN[i].Kwh)
    output_line_rnn = {"datetime": datetime, "Kwh" : kwh}
    
    return jsonify(output_line_rnn)

@app.route('/api/rnndata')
@login_required
def rnndata():
    query = RNN_data_predicted.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            RNN_data_predicted.DateTime.like(f'%{search}%'),
            RNN_data_predicted.Kwh.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            RNN_data_predicted.Date >= from_date,
            RNN_data_predicted.Date <= to_date,
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
        col = getattr(RNN_data_predicted, col_name)
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
        'data': [RNN_data_predicted.to_dict() for RNN_data_predicted in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': RNN_data_predicted.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route("/algoritma2") #GRU
@login_required


def algoritma2():
    gru_price_data = gru_price.query.all()
    
    #Predict satu bulan kedepan
    one_month_price_data = gru_price_data[0].Tarif
    one_month_price = babel.numbers.format_currency(one_month_price_data, "IDR", locale='id_ID')
    one_month_kwh_data = gru_price_data[0].Total_Kwh
    one_month_kwh_data = "{:.2f}".format(one_month_kwh_data)
    one_month_range = gru_price_data[0].range_date
        
    #Predict dua bulan kedepan
    two_month_price_data = gru_price_data[1].Tarif
    two_month_price = babel.numbers.format_currency(two_month_price_data, "IDR", locale='id_ID')
    two_month_kwh_data = gru_price_data[1].Total_Kwh
    two_month_kwh_data = "{:.2f}".format(two_month_kwh_data)
    two_month_range = gru_price_data[1].range_date
        
    #Predict tiga bulan kedepan
    three_month_price_data = gru_price_data[2].Tarif
    three_month_price = babel.numbers.format_currency(three_month_price_data, "IDR", locale='id_ID')
    three_month_kwh_data = gru_price_data[2].Total_Kwh
    three_month_kwh_data = "{:.2f}".format(three_month_kwh_data)
    three_month_range = gru_price_data[2].range_date
        
    #Predict empat bulan kedepan
    four_month_price_data = gru_price_data[3].Tarif
    four_month_price = babel.numbers.format_currency(four_month_price_data, "IDR", locale='id_ID')
    four_month_kwh_data = gru_price_data[3].Total_Kwh
    four_month_kwh_data = "{:.2f}".format(four_month_kwh_data)
    four_month_range = gru_price_data[3].range_date
        
    #Predict lima bulan kedepan
    five_month_price_data = gru_price_data[4].Tarif
    five_month_price = babel.numbers.format_currency(five_month_price_data, "IDR", locale='id_ID')
    five_month_kwh_data = gru_price_data[4].Total_Kwh
    five_month_kwh_data = "{:.2f}".format(five_month_kwh_data)
    five_month_range = gru_price_data[4].range_date
        
    #Predict enam bulan kedepan
    six_month_price_data = gru_price_data[5].Tarif
    six_month_price = babel.numbers.format_currency(six_month_price_data, "IDR", locale='id_ID')
    six_month_kwh_data = gru_price_data[5].Total_Kwh
    six_month_kwh_data = "{:.2f}".format(six_month_kwh_data)
    six_month_range = gru_price_data[5].range_date
        
    return render_template('algoritma2.html', one_month_price=one_month_price, one_month_kwh_data=one_month_kwh_data, one_month_range=one_month_range,two_month_price=two_month_price, two_month_kwh_data=two_month_kwh_data, two_month_range=two_month_range,three_month_price=three_month_price,three_month_kwh_data=three_month_kwh_data, three_month_range=three_month_range,four_month_price=four_month_price, four_month_kwh_data=four_month_kwh_data, four_month_range=four_month_range, five_month_price=five_month_price, five_month_kwh_data=five_month_kwh_data, five_month_range=five_month_range, six_month_price=six_month_price, six_month_kwh_data=six_month_kwh_data, six_month_range=six_month_range)
    

@app.route('/get_data_grulineChart')
@login_required
def get_data_grulineChart():
    lineChartDataGRU = GRU_data_predicted.query.all()

    datetime = []
    kwh = []
    for i in range(len(lineChartDataGRU)):
        datetime.append(lineChartDataGRU[i].Date + " " + lineChartDataGRU[i].Time)
        kwh.append(lineChartDataGRU[i].Kwh)
    output_line_gru = {"datetime": datetime, "Kwh" : kwh}
    
    return jsonify(output_line_gru)

@app.route('/api/grudata')
@login_required

def grudata():
    query = GRU_data_predicted.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            GRU_data_predicted.DateTime.like(f'%{search}%'),
            GRU_data_predicted.Kwh.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            GRU_data_predicted.Date >= from_date,
            GRU_data_predicted.Date <= to_date,
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
        col = getattr(GRU_data_predicted, col_name)
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
        'data': [GRU_data_predicted.to_dict() for GRU_data_predicted in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': GRU_data_predicted.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route("/algoritma3") #LMU
@login_required
def algoritma3():
    lmu_price_data = lmu_price.query.all()
    
    #Predict satu bulan kedepan
    one_month_price_data = lmu_price_data[0].Tarif
    one_month_price = babel.numbers.format_currency(one_month_price_data, "IDR", locale='id_ID')
    one_month_kwh_data = lmu_price_data[0].Total_Kwh
    one_month_kwh_data = "{:.2f}".format(one_month_kwh_data)
    one_month_range = lmu_price_data[0].range_date
    
    #Predict dua bulan kedepan
    two_month_price_data = lmu_price_data[1].Tarif
    two_month_price = babel.numbers.format_currency(two_month_price_data, "IDR", locale='id_ID')
    two_month_kwh_data = lmu_price_data[1].Total_Kwh
    two_month_kwh_data = "{:.2f}".format(two_month_kwh_data)
    two_month_range = lmu_price_data[1].range_date
    
    #Predict tiga bulan kedepan
    three_month_price_data = lmu_price_data[2].Tarif
    three_month_price = babel.numbers.format_currency(three_month_price_data, "IDR", locale='id_ID')
    three_month_kwh_data = lmu_price_data[2].Total_Kwh
    three_month_kwh_data = "{:.2f}".format(three_month_kwh_data)
    three_month_range = lmu_price_data[2].range_date
    
    #Predict empat bulan kedepan
    four_month_price_data = lmu_price_data[3].Tarif
    four_month_price = babel.numbers.format_currency(four_month_price_data, "IDR", locale='id_ID')
    four_month_kwh_data = lmu_price_data[3].Total_Kwh
    four_month_kwh_data = "{:.2f}".format(four_month_kwh_data)
    four_month_range = lmu_price_data[3].range_date
    
    #Predict lima bulan kedepan
    five_month_price_data = lmu_price_data[4].Tarif
    five_month_price = babel.numbers.format_currency(five_month_price_data, "IDR", locale='id_ID')
    five_month_kwh_data = lmu_price_data[4].Total_Kwh
    five_month_kwh_data = "{:.2f}".format(five_month_kwh_data)
    five_month_range = lmu_price_data[4].range_date
    
    #Predict enam bulan kedepan
    six_month_price_data = lmu_price_data[5].Tarif
    six_month_price = babel.numbers.format_currency(six_month_price_data, "IDR", locale='id_ID')
    six_month_kwh_data = lmu_price_data[5].Total_Kwh
    six_month_kwh_data = "{:.2f}".format(six_month_kwh_data)
    six_month_range = lmu_price_data[5].range_date
    
    return render_template('algoritma3.html', one_month_price=one_month_price, one_month_kwh_data=one_month_kwh_data, one_month_range=one_month_range,two_month_price=two_month_price, two_month_kwh_data=two_month_kwh_data, two_month_range=two_month_range,three_month_price=three_month_price,three_month_kwh_data=three_month_kwh_data, three_month_range=three_month_range,four_month_price=four_month_price, four_month_kwh_data=four_month_kwh_data, four_month_range=four_month_range, five_month_price=five_month_price, five_month_kwh_data=five_month_kwh_data, five_month_range=five_month_range, six_month_price=six_month_price, six_month_kwh_data=six_month_kwh_data, six_month_range=six_month_range)

@app.route('/get_data_lmulineChart')
@login_required
def get_data_lmulineChart():
    lineChartDataLMU = LMU_data_predicted.query.all()

    datetime = []
    kwh = []
    for i in range(len(lineChartDataLMU)):
        datetime.append(lineChartDataLMU[i].Date + " " + lineChartDataLMU[i].Time)
        kwh.append(lineChartDataLMU[i].Kwh)
    output_line_lmu = {"datetime": datetime, "Kwh" : kwh}
    
    return jsonify(output_line_lmu)

@app.route('/api/lmudata')
@login_required
def lmudata():
    query = LMU_data_predicted.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            LMU_data_predicted.DateTime.like(f'%{search}%'),
            LMU_data_predicted.Kwh.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            LMU_data_predicted.Date >= from_date,
            LMU_data_predicted.Date <= to_date,
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
        col = getattr(LMU_data_predicted, col_name)
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
        'data': [LMU_data_predicted.to_dict() for LMU_data_predicted in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': LMU_data_predicted.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route("/algoritma4") #TCN
@login_required
def algoritma4():
    tcn_price_data = tcn_price.query.all()
    # df_predict = pd.read_sql_table('TCN_data_predicted',TCN_data_predicted.query.all(),columns=['Date','Time','Kwh'])
    # df_predict = Parsing_Data(df_predict)

    # hari_1 = df_predict[:24]
    # hari_2 = df_predict[24:48]
    # minggu_1 = df_predict[:168]
    # minggu_2 = df_predict[168:336]
    # bulan_1 = df_predict[:720]
    # bulan_2 = df_predict[720:1440]

    # range_date_list = []
    # range_date_list.append(concat_date(hari_1))
    # range_date_list.append(concat_date(hari_2))
    # range_date_list.append(concat_date(minggu_1))
    # range_date_list.append(concat_date(minggu_2))
    # range_date_list.append(concat_date(bulan_1))
    # range_date_list.append(concat_date(bulan_2))

    # total_kwh = []
    # total_kwh_hari_1 = float(hari_1.sum())
    # total_kwh_hari_2 = float(hari_2.sum())
    # total_kwh_minggu_1 = float(minggu_1.sum())
    # total_kwh_minggu_2 = float(minggu_2.sum())
    # total_kwh_bulan_1 = float(bulan_1.sum())
    # total_kwh_bulan_2 = float(bulan_2.sum())

    # total_kwh.append(total_kwh_hari_1)
    # total_kwh.append(total_kwh_hari_2)
    # total_kwh.append(total_kwh_minggu_1)
    # total_kwh.append(total_kwh_minggu_2)
    # total_kwh.append(total_kwh_bulan_1)
    # total_kwh.append(total_kwh_bulan_2)

    # days1 = timedelta(days=1)
    # days2 = timedelta(days=2)
    # weeks1= timedelta(weeks=1)
    # weeks2 = timedelta(weeks=2)
    # month1 = timedelta(weeks=4)
    # month2 = timedelta(weeks=8)
    # 
    # today_date = date.today() + days1
    # today = today_date.strftime("%Y-%m-%d")

    # yesterday_date = date.today() + days2
    # yesterday = yesterday_date.strftime("%Y-%m-%d")

    # weekly_date = date.today() + weeks1
    # weeklyan = weekly_date.strftime("%Y-%m-%d")

    # yeswekkly_date = date.today() + weeks2
    # yesweeklyan = yeswekkly_date.strftime("%Y-%m-%d")

    # monthly_date = date.today() + month1
    # monthlylyan = monthly_date.strftime("%Y-%m-%d")

    # yesmonthly_date = date.today() + month2
    # yesmonthlyan = yesmonthly_date.strftime("%Y-%m-%d")

    # Kwh_kemarin = TCN_data_predicted.query.filter_by(Date = yesterday ).all()
    # Kwh_hariIni = TCN_data_predicted.query.filter_by(Date = today ).all()

    # kwh_weekly = TCN_data_predicted.query.filter(TCN_data_predicted.Date <= weeklyan).all()
    # yeskwh_weekly = TCN_data_predicted.query.filter(TCN_data_predicted.Date <= yesweeklyan).all()

    # kwh_monthly = TCN_data_predicted.query.filter(TCN_data_predicted.Date <= monthlylyan).all()
    # yeskwh_monthly = TCN_data_predicted.query.filter(TCN_data_predicted.Date <= yesmonthlyan).all()

    # today_list = []
    # yesterday_list = []
    # weekly_list = []
    # yesweekly_list = []
    # monthly_list = []
    # yesmonthly_list = []

    # for i in range(len(Kwh_hariIni)):
        # today_list.append(Kwh_hariIni[i].Kwh)
    # for i in range(len(Kwh_kemarin)):
        # yesterday_list.append(Kwh_kemarin[i].Kwh)
    # for i in range(len(kwh_weekly)):
        # weekly_list.append(kwh_weekly[i].Kwh)
    # for i in range(len(yeskwh_weekly)):
        # yesweekly_list.append(yeskwh_weekly[i].Kwh)
    # for i in range(len(kwh_monthly)):
        # monthly_list.append(kwh_monthly[i].Kwh)
    # for i in range(len(yeskwh_monthly)):
        # yesmonthly_list.append(yeskwh_monthly[i].Kwh)

    # rata2_today = np.sum(today_list)
    # rata2_yesterday = np.sum(yesterday_list)
    # todaykwh = "{:.2f}".format(rata2_today)

    # rata2_weekly = np.sum(weekly_list)
    # rata2_yesweekly = np.sum(yesweekly_list)
    # weekly = "{:.2f}".format(rata2_weekly)

    # rata2_monthly = np.sum(monthly_list)
    # rata2_yesmonthly = np.sum(yesmonthly_list)
    # monthly = "{:.2f}".format(rata2_monthly)
    # 
    # if (rata2_today >  rata2_yesterday):
        # selisih = ((rata2_today - rata2_yesterday)/rata2_today)
        # selisih = round(selisih*100)
        # selisih = str(selisih) + "% " 

    # elif (rata2_today < rata2_yesterday):
        # selisih = ((rata2_today - rata2_yesterday)/rata2_today) 
        # selisih = round(selisih*100)
        # selisih = abs(selisih)
        # selisih = str(selisih) + "% "
    # else:
        # selisih = ((rata2_today - rata2_yesterday)/rata2_today)
        # selisih = round(selisih*100)
        # selisih = print("-")
    # if (rata2_weekly >  rata2_yesweekly):
        # selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly)
        # selisihw = round(selisihw*100)
        # selisihw = str(selisihw) + "% " 
    # elif (rata2_weekly < rata2_yesweekly):
        # selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly) 
        # selisihw = round(selisihw*100)
        # selisihw = abs(selisihw)
        # selisihw = str(selisihw) + "% " 
    # else:
        # selisihw = ((rata2_weekly - rata2_yesweekly)/rata2_weekly)
        # selisihw = selisihw*100
        # selisihw = print("-")
    # if (rata2_monthly >  rata2_yesmonthly):
        # selisihm = ((rata2_monthly - rata2_yesmonthly)/rata2_monthly)
        # selisihm = round(selisihm*100)
        # selisihm = str(selisihm) + "% "
    # elif (rata2_monthly < rata2_yesmonthly):
        # selisihm = ((rata2_monthly - rata2_yesmonthly)/rata2_monthly) 
        # selisihm = round(selisihm*100)
        # selisihm = abs(selisihm)
        # selisihm = str(selisihm) + "% "
    # else:
        # selisihm = ((rata2_monthly - rata2_yesmonthly)/rata2_monthly)
        # selisihm = round(selisihm*100)
        # selisihm = print("-")

    #Predict satu bulan kedepan
    one_month_price_data = tcn_price_data[0].Tarif
    one_month_price = babel.numbers.format_currency(one_month_price_data, "IDR", locale='id_ID')
    one_month_kwh_data = tcn_price_data[0].Total_Kwh
    one_month_kwh_data = "{:.2f}".format(one_month_kwh_data)
    one_month_range = tcn_price_data[0].range_date

    #Predict dua bulan kedepan
    two_month_price_data = tcn_price_data[1].Tarif
    two_month_price = babel.numbers.format_currency(two_month_price_data, "IDR", locale='id_ID')
    two_month_kwh_data = tcn_price_data[1].Total_Kwh
    two_month_kwh_data = "{:.2f}".format(two_month_kwh_data)
    two_month_range = tcn_price_data[1].range_date

    #Predict tiga bulan kedepan
    three_month_price_data = tcn_price_data[2].Tarif
    three_month_price = babel.numbers.format_currency(three_month_price_data, "IDR", locale='id_ID')
    three_month_kwh_data = tcn_price_data[2].Total_Kwh
    three_month_kwh_data = "{:.2f}".format(three_month_kwh_data)
    three_month_range = tcn_price_data[2].range_date

    #Predict empat bulan kedepan
    four_month_price_data = tcn_price_data[3].Tarif
    four_month_price = babel.numbers.format_currency(four_month_price_data, "IDR", locale='id_ID')
    four_month_kwh_data = tcn_price_data[3].Total_Kwh
    four_month_kwh_data = "{:.2f}".format(four_month_kwh_data)
    four_month_range = tcn_price_data[3].range_date

    #Predict lima bulan kedepan
    five_month_price_data = tcn_price_data[4].Tarif
    five_month_price = babel.numbers.format_currency(five_month_price_data, "IDR", locale='id_ID')
    five_month_kwh_data = tcn_price_data[4].Total_Kwh
    five_month_kwh_data = "{:.2f}".format(five_month_kwh_data)
    five_month_range = tcn_price_data[4].range_date

    #Predict enam bulan kedepan
    six_month_price_data = tcn_price_data[5].Tarif
    six_month_price = babel.numbers.format_currency(six_month_price_data, "IDR", locale='id_ID')
    six_month_kwh_data = tcn_price_data[5].Total_Kwh
    six_month_kwh_data = "{:.2f}".format(six_month_kwh_data)
    six_month_range = tcn_price_data[5].range_date
 
    return render_template('algoritma4.html',one_month_price=one_month_price, one_month_kwh_data=one_month_kwh_data, one_month_range=one_month_range,two_month_price=two_month_price, two_month_kwh_data=two_month_kwh_data, two_month_range=two_month_range,three_month_price=three_month_price,three_month_kwh_data=three_month_kwh_data, three_month_range=three_month_range,four_month_price=four_month_price, four_month_kwh_data=four_month_kwh_data, four_month_range=four_month_range, five_month_price=five_month_price, five_month_kwh_data=five_month_kwh_data, five_month_range=five_month_range, six_month_price=six_month_price, six_month_kwh_data=six_month_kwh_data, six_month_range=six_month_range)
    # return render_template('algoritma4.html',kwh_today=f"{selisih}", rata2_today=rata2_today, rata2_yesterday= rata2_yesterday, todaykwh=f"{todaykwh}", weeklykwh=f"{selisihw}", weekly=f"{weekly}", monthlykwh=f"{selisihm}", monthly=f"{monthly}",one_month_price=one_month_price, one_month_kwh_data=one_month_kwh_data, one_month_range=one_month_range,two_month_price=two_month_price, two_month_kwh_data=two_month_kwh_data, two_month_range=two_month_range,three_month_price=three_month_price,three_month_kwh_data=three_month_kwh_data, three_month_range=three_month_range,four_month_price=four_month_price, four_month_kwh_data=four_month_kwh_data, four_month_range=four_month_range, five_month_price=five_month_price, five_month_kwh_data=five_month_kwh_data, five_month_range=five_month_range, six_month_price=six_month_price, six_month_kwh_data=six_month_kwh_data, six_month_range=six_month_range)

@app.route('/get_data_tcnlineChart')
@login_required
def get_data_tcnlineChart():
    lineChartDataTCN = TCN_data_predicted.query.all()

    datetime = []
    kwh = []
    for i in range(len(lineChartDataTCN)):
        datetime.append(lineChartDataTCN[i].Date + " " + lineChartDataTCN[i].Time)
        kwh.append(lineChartDataTCN[i].Kwh)
    output_line_tcn = {"datetime": datetime, "Kwh" : kwh}
    # print(f'data linechartTCN: {output_line_tcn}', file=sys.stderr)
    return jsonify(output_line_tcn)

@app.route('/api/tcndata')
@login_required
def tcndata():
    query = TCN_data_predicted.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            TCN_data_predicted.DateTime.like(f'%{search}%'),
            TCN_data_predicted.Kwh.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            TCN_data_predicted.Date >= from_date,
            TCN_data_predicted.Date <= to_date,
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

@app.route("/gedungN")
@login_required
def clusteringn():
    # clusday= KlasterGdNPerhari.query.all()

    # normal0 = KlasterGdNPerhari.query.filter(KlasterGdNPerhari.kluster == 0).all()
    # rendah1 = KlasterGdNPerhari.query.filter(KlasterGdNPerhari.kluster == 1).all()
    # tinggi2 = KlasterGdNPerhari.query.filter(KlasterGdNPerhari.kluster == 2).all()

    # normallist = []
    # rendahlist = []
    # tinggilist = []

    # for i in range(len(normal0)):
        # normallist.append(normal0[i].kluster)
    # for i in range(len(rendah1)):
        # rendahlist.append(rendah1[i].kluster)
    # for i in range(len(tinggi2)):
        # tinggilist.append(tinggi2[i].kluster)

    # Normal = len(normallist)
    # Rendah = len(rendahlist)
    # Tinggi = len(tinggilist)

    return render_template('clusteringn.html')

@app.route("/gedungOdanP")
@login_required
def clusteringop():
    return render_template('clusteringop.html')

@app.route('/api/clusterperhari')
@login_required
def clusterperhari():
    query = KlasterGdNPerhari.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            KlasterGdNPerhari.Date.like(f'%{search}%'),
            KlasterGdNPerhari.kluster.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            KlasterGdNPerhari.Date >= from_date,
            KlasterGdNPerhari.Date <= to_date,
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
        if col_name not in ['Date', 'Time', 'Kwh', 'kluster']:
            col_name = 'Date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(KlasterGdNPerhari, col_name)
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
        'data': [KlasterGdNPerhari.to_dict() for KlasterGdNPerhari in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': KlasterGdNPerhari.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/clusterVirtualperhari')
@login_required
def clusterVirtualperhari():
    query = KlasterVirtualPerhari.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            KlasterVirtualPerhari.Date.like(f'%{search}%'),
            KlasterVirtualPerhari.kluster.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            KlasterVirtualPerhari.Date >= from_date,
            KlasterVirtualPerhari.Date <= to_date,
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
        if col_name not in ['Date', 'Time', 'Kwh', 'old_kwh', 'delta_kwh', 'kluster']:
            col_name = 'Date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(KlasterVirtualPerhari, col_name)
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
        'data': [KlasterVirtualPerhari.to_dict() for KlasterVirtualPerhari in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': KlasterVirtualPerhari.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/clusterperbulan')
@login_required
def clusterperbulan():
    query = KlasterGdNPerbulan.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            KlasterGdNPerbulan.Date.like(f'%{search}%'),
            KlasterGdNPerbulan.kluster.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            KlasterGdNPerbulan.Date >= from_date,
            KlasterGdNPerbulan.Date <= to_date,
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
        if col_name not in ['Date', 'Kwh', 'kluster']:
            col_name = 'Date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(KlasterGdNPerbulan, col_name)
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
        'data': [KlasterGdNPerbulan.to_dict() for KlasterGdNPerbulan in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': KlasterGdNPerbulan.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/clusterVirtualperbulan')
@login_required
def clusterVirtualperbulan():
    query = KlasterVirtualPerbulan.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            KlasterVirtualPerbulan.Date.like(f'%{search}%'),
            KlasterVirtualPerbulan.kluster.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # # filter by date
    # from_date = request.args.get('searchByFromdate')
    # to_date = request.args.get('searchByTodate')
    # if from_date and to_date:
    #     query = query.filter(db.and_(
    #         KlasterPerhari.Date >= from_date,
    #         KlasterPerhari.Date <= to_date,
    #     ))
    # total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['Date', 'Kwh', 'old_kwh', 'delta_kwh', 'kluster']:
            col_name = 'DateTime'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(KlasterVirtualPerbulan, col_name)
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
        'data': [KlasterVirtualPerbulan.to_dict() for KlasterVirtualPerbulan in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': KlasterVirtualPerbulan.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@app.route('/api/clusterpertahun')
@login_required
def clusterpertahun():
    query = KlastergdNPertahun.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            KlastergdNPertahun.Date.like(f'%{search}%'),
            KlastergdNPertahun.kluster.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # # filter by date
    from_date = request.args.get('searchByFromdate')
    to_date = request.args.get('searchByTodate')
    if from_date and to_date:
        query = query.filter(db.and_(
            KlastergdNPertahun.Date >= from_date,
            KlastergdNPertahun.Date <= to_date,
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
        if col_name not in ['Date', 'Kwh', 'kluster']:
            col_name = 'Date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(KlastergdNPertahun, col_name)
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
        'data': [KlastergdNPertahun.to_dict() for KlastergdNPertahun in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': KlastergdNPertahun.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/clustervirtualpertahun')
@login_required
def clustervirtualpertahun():
    query = KlasterVirtualPertahun.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            KlasterVirtualPertahun.Date.like(f'%{search}%'),
            KlasterVirtualPertahun.kluster.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # # filter by date
    # from_date = request.args.get('searchByFromdate')
    # to_date = request.args.get('searchByTodate')
    # if from_date and to_date:
    #     query = query.filter(db.and_(
    #         KlasterPerhari.Date >= from_date,
    #         KlasterPerhari.Date <= to_date,
    #     ))
    # total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['Date', 'Kwh', 'old_kwh', 'delta_kwh', 'kluster']:
            col_name = 'Date'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(KlasterVirtualPertahun, col_name)
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
        'data': [KlasterVirtualPertahun.to_dict() for KlasterVirtualPertahun in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': KlasterVirtualPertahun.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/get_data_clusteringGdNPerhari')
@login_required
def get_data_clusteringGdNperhari():
    normal0 = KlasterGdNPerhari.query.filter(KlasterGdNPerhari.kluster == 0).all()
    rendah1 = KlasterGdNPerhari.query.filter(KlasterGdNPerhari.kluster == 1).all()
    tinggi2 = KlasterGdNPerhari.query.filter(KlasterGdNPerhari.kluster == 2).all()
    
    normallist = []
    rendahlist = []
    tinggilist = []
    
    for i in range(len(normal0)):
        normallist.append(normal0[i].kluster)
    for i in range(len(rendah1)):
        rendahlist.append(rendah1[i].kluster)
    for i in range(len(tinggi2)):
        tinggilist.append(tinggi2[i].kluster)
    
    Normal = len(normallist)
    Rendah = len(rendahlist)
    Tinggi = len(tinggilist)

    output_clus_day = {"Normal":Normal, "Rendah":Rendah, "Tinggi":Tinggi}
    return jsonify(output_clus_day)

@app.route('/get_data_clusteringGdNPerbulan')
@login_required
def get_data_clusteringGdNPerbulan():
    normal0 = KlasterGdNPerbulan.query.filter(KlasterGdNPerbulan.kluster == 0).all()
    rendah1 = KlasterGdNPerbulan.query.filter(KlasterGdNPerbulan.kluster == 1).all()
    tinggi2 = KlasterGdNPerbulan.query.filter(KlasterGdNPerbulan.kluster == 2).all()

    normallist = []
    rendahlist = []
    tinggilist = []

    for i in range(len(normal0)):
        normallist.append(normal0[i].kluster)
    for i in range(len(rendah1)):
        rendahlist.append(rendah1[i].kluster)
    for i in range(len(tinggi2)):
        tinggilist.append(tinggi2[i].kluster)

    Normal = len(normallist)
    Rendah = len(rendahlist)
    Tinggi = len(tinggilist)

    output_clus_month = {"Normal":Normal, "Rendah":Rendah, "Tinggi":Tinggi}
    return jsonify(output_clus_month)

@app.route('/get_data_clusteringgdNPertahun')
@login_required
def get_data_clusteringgdNPertahun():
    normal0 = KlastergdNPertahun.query.filter(KlastergdNPertahun.kluster == 0).all()
    rendah1 = KlastergdNPertahun.query.filter(KlastergdNPertahun.kluster == 1).all()
    tinggi2 = KlastergdNPertahun.query.filter(KlastergdNPertahun.kluster == 2).all()

    normallist = []
    rendahlist = []
    tinggilist = []

    for i in range(len(normal0)):
        normallist.append(normal0[i].kluster)
    for i in range(len(rendah1)):
        rendahlist.append(rendah1[i].kluster)
    for i in range(len(tinggi2)):
        tinggilist.append(tinggi2[i].kluster)

    Normal = len(normallist)
    Rendah = len(rendahlist)
    Tinggi = len(tinggilist)

    output_clus_year = {"Normal":Normal, "Rendah":Rendah, "Tinggi":Tinggi}
    return jsonify(output_clus_year)

@app.route('/get_data_clusteringVGdNPerhari')
@login_required
def get_data_clusteringVGdNperhari():
    normal0 = KlasterVirtualPerhari.query.filter(KlasterVirtualPerhari.kluster == 0).all()
    rendah1 = KlasterVirtualPerhari.query.filter(KlasterVirtualPerhari.kluster == 1).all()
    tinggi2 = KlasterVirtualPerhari.query.filter(KlasterVirtualPerhari.kluster == 2).all()
    
    normallist = []
    rendahlist = []
    tinggilist = []
    
    for i in range(len(normal0)):
        normallist.append(normal0[i].kluster)
    for i in range(len(rendah1)):
        rendahlist.append(rendah1[i].kluster)
    for i in range(len(tinggi2)):
        tinggilist.append(tinggi2[i].kluster)
    
    Normal = len(normallist)
    Rendah = len(rendahlist)
    Tinggi = len(tinggilist)

    output_vclus_day = {"Normal":Normal, "Rendah":Rendah, "Tinggi":Tinggi}
    return jsonify(output_vclus_day)

@app.route('/get_data_clusteringVGdNPerbulan')
@login_required
def get_data_clusteringVGdNPerbulan():
    normal0 = KlasterVirtualPerbulan.query.filter(KlasterVirtualPerbulan.kluster == 0).all()
    rendah1 = KlasterVirtualPerbulan.query.filter(KlasterVirtualPerbulan.kluster == 1).all()
    tinggi2 = KlasterVirtualPerbulan.query.filter(KlasterVirtualPerbulan.kluster == 2).all()

    normallist = []
    rendahlist = []
    tinggilist = []

    for i in range(len(normal0)):
        normallist.append(normal0[i].kluster)
    for i in range(len(rendah1)):
        rendahlist.append(rendah1[i].kluster)
    for i in range(len(tinggi2)):
        tinggilist.append(tinggi2[i].kluster)

    Normal = len(normallist)
    Rendah = len(rendahlist)
    Tinggi = len(tinggilist)

    output_vclus_month = {"Normal":Normal, "Rendah":Rendah, "Tinggi":Tinggi}
    return jsonify(output_vclus_month)

@app.route('/get_data_clusteringvgdNPertahun')
@login_required
def get_data_clusteringvgdNPertahun():
    normal0 = KlasterVirtualPertahun.query.filter(KlasterVirtualPertahun.kluster == 0).all()
    rendah1 = KlasterVirtualPertahun.query.filter(KlasterVirtualPertahun.kluster == 1).all()
    tinggi2 = KlasterVirtualPertahun.query.filter(KlasterVirtualPertahun.kluster == 2).all()

    normallist = []
    rendahlist = []
    tinggilist = []

    for i in range(len(normal0)):
        normallist.append(normal0[i].kluster)
    for i in range(len(rendah1)):
        rendahlist.append(rendah1[i].kluster)
    for i in range(len(tinggi2)):
        tinggilist.append(tinggi2[i].kluster)

    Normal = len(normallist)
    Rendah = len(rendahlist)
    Tinggi = len(tinggilist)

    output_vclus_year = {"Normal":Normal, "Rendah":Rendah, "Tinggi":Tinggi}
    return jsonify(output_vclus_year)

@app.route('/get_data_comclustering')
@login_required
def get_data_comclustering():
    clusday     = KlasterGdNPerhari.query
    vclusday    = KlasterVirtualPerhari.query
    clusmonth   = KlasterPerbulan.query
    vclusmonth  = KlasterVirtualPerbulan.query
    clusyear    = KlastergdNPertahun.query
    vclusyear   = KlasterVirtualPertahun.query

    datetime    = []
    kwhdclus    = []
    kwhvdclus   = []
    kwhmclus    = []
    kwhvmclus   = []
    kwhyclus    = []
    kwhvyclus   = []

    for i in range(len(clusday)):
        kwhdclus.append(clusday[i].kluster)
    for i in range(len(vclusday)):
        kwhvdclus.append(vclusday[i].kluster)
    for i in range(len(clusmonth)):
        kwhmclus.append(clusmonth[i].kluster)
    for i in range(len(vclusmonth)):
        kwhvmclus.append(vclusmonth[i].kluster)
    for i in range(len(clusyear)):
        kwhyclus.append(clusyear[i].kluster)
    for i in range(len(vclusyear)):
        kwhvyclus.append(vclusyear[i].kluster)

    output_dought_com = {"datetime": datetime, "kwhdclus": kwhdclus, "kwhvdclus": kwhvdclus, "kwhmclus": kwhmclus, "kwhvmclus": kwhvmclus, "kwhyclus": kwhyclus, "kwhvyclus": kwhvyclus}

    return jsonify(output_dought_com)



@app.route("/compare")
@login_required
def compare():
    return render_template('compare.html')

@app.route('/get_data_compstacklineChart')
@login_required
def get_data_compstacklineChart():
    lineChartDataRNN = RNN_data_predicted.query.all()
    lineChartDataGRU = GRU_data_predicted.query.all()
    lineChartDataLMU = LMU_data_predicted.query.all()
    lineChartDataTCN = TCN_data_predicted.query.all()

    datetime = []
    kwhrnn = []
    kwhgru = []
    kwhlmu = []
    kwhtcn = []

    # if datetime.append(lineChartDataRNN[i].Date + " " + lineChartDataRNN[i].Time) != True:
        # for i in range(len(lineChartDataRNN)):
            # datetime.append(lineChartDataRNN[i].Date + " " + lineChartDataRNN[i].Time)
            # kwhrnn.append(lineChartDataRNN[i].Kwh)
        # for i in range(len(lineChartDataGRU)):
            # kwhgru.append(lineChartDataGRU[i].Kwh)
        # for i in range(len(lineChartDataLMU)):
            # kwhlmu.append(lineChartDataLMU[i].Kwh)
        # for i in range(len(lineChartDataTCN)):    
            # kwhtcn.append(lineChartDataTCN[i].Kwh)
    # elif datetime.append(lineChartDataGRU[i].Date + " " + lineChartDataGRU[i].Time) != True:
        # for i in range(len(lineChartDataGRU)):
            # datetime.append(lineChartDataGRU[i].Date + " " + lineChartDataGRU[i].Time)
            # kwhgru.append(lineChartDataGRU[i].Kwh)
        # for i in range(len(lineChartDataRNN)):
            # kwhrnn.append(lineChartDataRNN[i].Kwh)
        # for i in range(len(lineChartDataLMU)):
            # kwhlmu.append(lineChartDataLMU[i].Kwh)
        # for i in range(len(lineChartDataTCN)):    
            # kwhtcn.append(lineChartDataTCN[i].Kwh)
    # elif datetime.append(lineChartDataLMU[i].Date + " " + lineChartDataLMU[i].Time) != True:
    for i in range(len(lineChartDataLMU)):
        datetime.append(lineChartDataLMU[i].Date + " " + lineChartDataLMU[i].Time)
        kwhlmu.append(lineChartDataLMU[i].Kwh)
    for i in range(len(lineChartDataRNN)):
        kwhrnn.append(lineChartDataRNN[i].Kwh)
    for i in range(len(lineChartDataGRU)):
        kwhgru.append(lineChartDataGRU[i].Kwh)
    for i in range(len(lineChartDataTCN)):
        kwhtcn.append(lineChartDataTCN[i].Kwh) 
    # elif datetime.append(lineChartDataGRU[i].Date + " " + lineChartDataGRU[i].Time) != True:
        # for i in range(len(lineChartDataTCN)):
            # datetime.append(lineChartDataTCN[i].Date + " " + lineChartDataTCN[i].Time)
            # kwhtcn.append(lineChartDataTCN[i].Kwh)
        # for i in range(len(lineChartDataRNN)):
            # kwhrnn.append(lineChartDataRNN[i].Kwh)
        # for i in range(len(lineChartDataGRU)):
            # kwhgru.append(lineChartDataGRU[i].Kwh)
        # for i in range(len(lineChartDataLMU)):
            # kwhlmu.append(lineChartDataLMU[i].Kwh)
    # else:
        # print("error")
    
    output_line_com = {"datetime": datetime, "Kwhrnn" : kwhrnn, "Kwhgru" : kwhgru, "Kwhlmu" : kwhlmu, "Kwhtcn" : kwhtcn}
    
    return jsonify(output_line_com)


@app.route("/schedule_appliance")
@login_required
def schedule_appliance():
    user_type = current_user.user_type
    user_id = current_user.id
    if user_type == 'user':
        all_data = deviceinput.query.filter_by(user_id=user_id).all()
        all_billing = billinginput.query.filter_by(user_id_bill=user_id).all()
    else:
        all_data = deviceinput.query.all()
        all_billing = billinginput.query.all()
    return render_template("scheduling.html", Devices=all_data, Billing=all_billing)
    # return render_template("scheduling.html")

# @app.route('/api/billing')
# @login_required
# def billing():
#     query = billinginput.query

#     # search filter
#     search = request.args.get('search[value]')
#     if search:
#         query = query.filter(db.or_(
#             billinginput.username.like(f'%{search}%'),
#             billinginput.tarif_listrik.like(f'%{search}%')
#         ))
#     total_filtered = query.count()

#     # sorting
#     order = []
#     i = 0
#     while True:
#         col_index = request.args.get(f'order[{i}][column]')
#         if col_index is None:
#             break
#         col_name = request.args.get(f'columns[{col_index}][data]')
#         if col_name not in ['User ID', 'Username', 'Daya Listrik', 'Tagihan Listrik(RP)']:
#             col_name = 'username'
#         descending = request.args.get(f'order[{i}][dir]') == 'desc'
#         col = getattr(billinginput, col_name)
#         if descending:
#             col = col.desc()
#         order.append(col)
#         i += 1
#     if order:
#         query = query.order_by(*order)

#     # pagination
#     start = request.args.get('start', type=int)
#     length = request.args.get('length', type=int)
#     query = query.offset(start).limit(length)

#     # response
#     return {
#         'data': [billinginput.to_dict() for billinginput in query],
#         'recordsFiltered': total_filtered,
#         'recordsTotal': billinginput.query.count(),
#         'draw': request.args.get('draw', type=int),
#     }

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
        my_billing = billinginput.query.get(request.form.get('billingUpdate'))
 
        my_billing.tarif_listrik = request.form['tarif_listrik']
        my_billing.tagihan_listrik = request.form['tagihan_listrik']
 
        db.session.commit()
        flash("Billing Updated Successfully", 'success')

        # if current_user.user_type == 'user':
        #     all_data = deviceinput.query.filter_by(user_id=current_user.id).all()
        #     all_billing = billinginput.query.filter_by(user_id_bill=current_user.id).all()
        # else:
        #     all_data = deviceinput.query.all()
        #     all_billing = billinginput.query.all()
        # return render_template("scheduling.html", Devices=all_data, Billing=all_billing)
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
        device_name = request.form['device_name']
        daya_device = request.form['daya_device']
        jumlah_device = request.form['jumlah_device']
        total_daya = float(daya_device)*int(jumlah_device)
        tingkat_prioritas = request.form['prioritas']
        device_status = request.form['device_status']
        device_read = request.form['device_read']
        device_token = request.form['device_token']
 
        my_data = deviceinput(user_id, username, device_name, daya_device, jumlah_device, total_daya, tingkat_prioritas, device_status, device_read, device_token)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Device Inserted Successfully", 'success')
 
        return redirect(url_for('schedule_appliance'))

# @app.route('/api/appliance')
# @login_required
# def appliance():
#     query = deviceinput.query

#     # search filter
#     search = request.args.get('search[value]')
#     if search:
#         query = query.filter(db.or_(
#             deviceinput.username.like(f'%{search}%'),
#             deviceinput.tarif_listrik.like(f'%{search}%')
#         ))
#     total_filtered = query.count()

#     # sorting
#     order = []
#     i = 0
#     while True:
#         col_index = request.args.get(f'order[{i}][column]')
#         if col_index is None:
#             break
#         col_name = request.args.get(f'columns[{col_index}][data]')
#         if col_name not in ['User ID', 'Device ID', 'Device Name', 'Daya Device','Tingkat Prioritas', 'Action']:
#             col_name = 'user_id'
#         descending = request.args.get(f'order[{i}][dir]') == 'desc'
#         col = getattr(deviceinput, col_name)
#         if descending:
#             col = col.desc()
#         order.append(col)
#         i += 1
#     if order:
#         query = query.order_by(*order)

#     # pagination
#     start = request.args.get('start', type=int)
#     length = request.args.get('length', type=int)
#     query = query.offset(start).limit(length)

#     # response
#     return {
#         'data': [deviceinput.to_dict() for deviceinput in query],
#         'recordsFiltered': total_filtered,
#         'recordsTotal': deviceinput.query.count(),
#         'draw': request.args.get('draw', type=int),
#     }

#this is our update route where we are going to update our employee
@app.route('/updateDevice', methods = ['GET', 'POST'])
@login_required
def updateDevice():
 
    if request.method == 'POST':
        my_data = deviceinput.query.get(request.form.get('applianceUpdate'))
 
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

@app.route('/api/dataTimer')
@login_required
def dataTimer():
    query = device_usage_duration.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            device_usage_duration.user_id.like(f'%{search}%'),
            device_usage_duration.device_id.like(f'%{search}%'),
            device_usage_duration.device_name.like(f'%{search}%')
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
        if col_name not in ['user_id', 'device_id', 'device_name', 'duration_scheduled', 'duration_left']:
            col_name = 'device_id'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(device_usage_duration, col_name)
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
        'data': [device_duration.to_dict() for device_duration in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': device_usage_duration.query.count(),
        'draw': request.args.get('draw', type=int),
    }

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