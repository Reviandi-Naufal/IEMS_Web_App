import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from Blog import app, db, bcrypt
from Blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from Blog.database import User, billinginput, deviceinput
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

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
    return redirect(url_for('home'))

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

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

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