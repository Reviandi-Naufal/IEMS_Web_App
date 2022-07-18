from datetime import datetime
from apps import db, ma, login_manager, app
from flask_login import UserMixin
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#####################################################################################
# Creating Model Tabel for User
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
    
    def to_dict(self):
        return {
            'id' : self.id,
            'username': self.username,
            'email': self.email,
            'user_type': self.user_type,
        }

#####################################################################################
# Creating Model table for Actual Data
class real_data(db.Model):
    Index = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Text)
    Time = db.Column(db.Text)
    Kwh = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'Index' : self.Index,
            'Date' : self.Date,
            'Time' : self.Time,
            'Kwh' : self.Kwh
        }
        
class real_dataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = real_data
        created_at = auto_field(dump_only=True)


#####################################################################################
# Creating Model table for Prediction
class RNN_data_predicted(db.Model):
    DateTime = db.Column(db.DateTime, primary_key=True)
    Kwh = db.Column(db.Float)
    Predictions = db.Column(db.Float)

class GRU_data_predicted(db.Model):
    DateTime = db.Column(db.DateTime, primary_key=True)
    Kwh = db.Column(db.Float)
    Predictions = db.Column(db.Float)

class LMU_data_predicted(db.Model):
    DateTime = db.Column(db.DateTime, primary_key=True)
    Kwh = db.Column(db.Float)
    Predictions = db.Column(db.Float)

class TCN_data_predicted(db.Model):
    DateTime = db.Column(db.DateTime, primary_key=True)
    Predictions = db.Column(db.Float)

    def to_dict(self):
        return {
            'DateTime' : self.DateTime,
            'Predictions' : self.Predictions
        }


#####################################################################################
# Creating Model Table for Clusttering

#class monitor(db.Model):
#    Id_gedung = db.Column(db.Integer)
#    Kwh = db.Column(db.Float)
#    Date = db.Column(db.Date)

class Monitoring(db.Model):
    Gedung = db.Column(db.Integer, primary_key=True)
    Kwh = db.Column(db.Float)
    Date = db.Column(db.DateTime)

#class pemantauan(db.Model):
#    Tanggal = db.Column(db.DateTime)
#    Alat = db.Column(db.Integer)
#    Kwh = db.Column(db.Float)

class Gedung(db.Model):
    id = db.Column(db. Integer, primary_key=True)
    pj = db.Column(db.String(45))
    Nama = db.Column(db.String(45))
    Lokasi = db.Column(db.String(45))
    Deleted = db.Column(db.String(45))

#####################################################################################

class billinginput(db.Model):
    user_id_bill = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    tarif_listrik = db.Column(db.String(50))
    tagihan_listrik = db.Column(db.Integer)
 
    def __init__(self, userID, username, tarifListrik, tagihanListrik):
        self.user_id_bill = userID
        self.username = username
        self.tarif_listrik = tarifListrik
        self.tagihan_listrik = tagihanListrik

    def to_dict(self):
        return {
            'user_id_bill' : self.user_id_bill,
            'username' : self.username,
            'tarif_listrik' : self.tarif_listrik,
            'tagihan_listrik' : self.tagihan_listrik
        }

# Creating model table for our CRUD database
class deviceinput(db.Model):
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(20), nullable=False)
    device_id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(100))
    daya_device = db.Column(db.Float)
    jumlah_device = db.Column(db.Integer)
    total_daya = db.Column(db.Float)
    tingkat_prioritas = db.Column(db.String(100))
 
    def __init__(self, userID, username, deviceID, deviceName, daya, jumlah_device, total_daya, prioritas):
        self.user_id = userID
        self.username = username
        self.device_id = deviceID
        self.device_name = deviceName
        self.daya_device = daya
        self.jumlah_device = jumlah_device
        self.total_daya = total_daya
        self.tingkat_prioritas = prioritas

    def to_dict(self):
        return {
            'user_id' : self.user_id,
            'username' : self.username,
            'device_id' : self.device_id,
            'device_name' : self.device_name,
            'daya_device' : self.daya_device,
            'jumlah_device' : self.jumlah_device,
            'total_daya' : self.total_daya,
            'tingkat_prioritas' : self.tingkat_prioritas,

        }

class device_status(db.Model):
    device_id = db.Column(db.Integer, nullable=False, primary_key=True)
    slca_name = db.Column(db.String(50))
    device_status = db.Column(db.Integer, nullable=False)

    def __init__(self, device_id, slca_name, device_status):
        self.user_id_bill = userID
        self.tarif_listrik = tarifListrik
        self.tagihan_listrik = tagihanListrik

class hasil_penjadwalan(db.Model):
    user_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer, nullable=False, primary_key=True)
    durasi = db.Column(db.Integer)
    tanggal = db.Column(db.String(50), nullable=False)
    waktu = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, device_id, durasi, tanggal, waktu):
        self.user_id = user_id
        self.device_id  = device_id
        self.device_id = device_id
        self.durasi = durasi
        self.tanggal = tanggal
        self.waktu = waktu