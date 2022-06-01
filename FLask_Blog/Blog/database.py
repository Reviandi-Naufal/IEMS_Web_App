from datetime import datetime
from Blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='user',)

    #setting __repr__ method, it's to define how the object is printed out whenever it get printed out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"

class billinginput(db.Model):
    user_id_bill = db.Column(db.Integer, primary_key=True)
    tarif_listrik = db.Column(db.String(50))
    tagihan_listrik = db.Column(db.Integer)
 
    def __init__(self, userID, tarifListrik, tagihanListrik):
        self.user_id_bill = userID
        self.tarif_listrik = tarifListrik
        self.tagihan_listrik = tagihanListrik
 
# Creating model table for our CRUD database
class deviceinput(db.Model):
    user_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100))
    daya_device = db.Column(db.Float)
    jumlah_device = db.Column(db.Integer)
    total_daya = db.Column(db.Float)
    tingkat_prioritas = db.Column(db.String(100))
 
    def __init__(self, userID, deviceID, deviceName, daya, jumlah_device, total_daya, prioritas):
        self.user_id = userID
        self.device_id = deviceID
        self.device_name = deviceName
        self.daya_device = daya
        self.jumlah_device = jumlah_device
        self.total_daya = total_daya
        self.tingkat_prioritas = prioritas