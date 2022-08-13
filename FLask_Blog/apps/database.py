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
    fullname = db.Column(db.String(120), unique=True, nullable=True)
    about = db.Column(db.String(500), unique=True, nullable=True)
    company = db.Column(db.String(150), unique=True, nullable=True)
    job = db.Column(db.String(150), unique=True, nullable=True)
    nim = db.Column(db.Integer, unique=True, nullable=True)
    phone = db.Column(db.Integer, unique=True, nullable=True)

    #setting __repr__ method, it's to define how the object is printed out whenever it get printed out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}','{self.fullname}','{self.about}','{self.company}','{self.job}','{self.nim}','{self.phone}')"
    
    def to_dict(self):
        return {
            'id' : self.id,
            'username': self.username,
            'email': self.email,
            'user_type': self.user_type,
            'fullname' : self.fullname,
            'about' : self.about,
            'company' : self.company,
            'job' : self.job,
            'nim' : self.nim,
            'phone' : self.phone
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
class RNN_data_predictedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RNN_data_predicted
        created_at = auto_field(dump_only=True)

class rnn_price(db.Model):
    Index = db.Column(db.Integer, primary_key=True)
    range_date = db.Column(db.String)
    Total_Kwh = db.Column(db.Float)
    Tarif = db.Column(db.Float)

class GRU_data_predicted(db.Model):
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
class GRU_data_predictedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GRU_data_predicted
        created_at = auto_field(dump_only=True)
class gru_price(db.Model):
    Index = db.Column(db.Integer, primary_key=True)
    range_date = db.Column(db.String)
    Total_Kwh = db.Column(db.Float)
    Tarif = db.Column(db.Float)

class LMU_data_predicted(db.Model):
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
class LMU_data_predictedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LMU_data_predicted
        created_at = auto_field(dump_only=True)

class lmu_price(db.Model):
    Index = db.Column(db.Integer, primary_key=True)
    range_date = db.Column(db.String)
    Total_Kwh = db.Column(db.Float)
    Tarif = db.Column(db.Float)

class TCN_data_predicted(db.Model):
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

class TCN_data_predictedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TCN_data_predicted
        created_at = auto_field(dump_only=True)

class tcn_price(db.Model):
    Index = db.Column(db.Integer, primary_key=True)
    range_date = db.Column(db.String)
    Total_Kwh = db.Column(db.Float)
    Tarif = db.Column(db.Float)
#####################################################################################
# Creating Model Table for Clusttering

#class monitor(db.Model):
#    Id_gedung = db.Column(db.Integer)
#    Kwh = db.Column(db.Float)
#    Date = db.Column(db.Date)

# class Monitoring(db.Model):
#     Gedung = db.Column(db.Integer, primary_key=True)
#     Kwh = db.Column(db.Float)
#     Date = db.Column(db.DateTime)

#class pemantauan(db.Model):
#    Tanggal = db.Column(db.DateTime)
#    Alat = db.Column(db.Integer)
#    Kwh = db.Column(db.Float)

# class Gedung(db.Model):
#     id = db.Column(db. Integer, primary_key=True)
#     pj = db.Column(db.String(45))
#     Nama = db.Column(db.String(45))
#     Lokasi = db.Column(db.String(45))
#     Deleted = db.Column(db.String(45))

class KlasterPerhari(db.Model):
    __tablename__ = "KlasterPerhari"
    DateTime = db.Column(db.String(50), primary_key=True)
    Kwh = db.Column(db.Float)
    old_kwh = db.Column(db.Float)
    delta_kwh = db.Column(db.Float)
    kluster = db.Column(db.Integer)

    def to_dict(self):
        return {
            'DateTime' : self.DateTime,
            'Kwh' : self.Kwh,
            'old_kwh' : self.old_kwh,
            'delta_kwh' : self.delta_kwh,
            'kluster' : self.kluster
        }

class KlasterPerhariSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KlasterPerhari
        created_at = auto_field(dump_only=True)

class KlasterPerbulan(db.Model):
    __tablename__ = "KlasterPerbulan"
    DateTime = db.Column(db.String(50), primary_key=True)
    Kwh = db.Column(db.Float)
    old_kwh = db.Column(db.Float)
    delta_kwh = db.Column(db.Float)
    kluster = db.Column(db.Integer)

    def to_dict(self):
        return {
            'DateTime' : self.DateTime,
            'Kwh' : self.Kwh,
            'old_kwh' : self.old_kwh,
            'delta_kwh' : self.delta_kwh,
            'kluster' : self.kluster
        }

class KlasterPerbulanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KlasterPerbulan
        created_at = auto_field(dump_only=True)

class KlasterPertahun(db.Model):
    __tablename__ = "KlasterPertahun"
    DateTime = db.Column(db.String(50), primary_key=True)
    Kwh = db.Column(db.Float)
    old_kwh = db.Column(db.Float)
    delta_kwh = db.Column(db.Float)
    kluster = db.Column(db.Integer)

    def to_dict(self):
        return {
            'DateTime' : self.DateTime,
            'Kwh' : self.Kwh,
            'old_kwh' : self.old_kwh,
            'delta_kwh' : self.delta_kwh,
            'kluster' : self.kluster
        }

class KlasterPertahunSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KlasterPertahun
        created_at = auto_field(dump_only=True)

class KlasterVirtualPerhari(db.Model):
    __tablename__ = "KlasterVirtualPerhari"
    DateTime = db.Column(db.String(50), primary_key=True)
    Kwh = db.Column(db.Float)
    old_kwh = db.Column(db.Float)
    delta_kwh = db.Column(db.Float)
    kluster = db.Column(db.Integer)

    def to_dict(self):
        return {
            'DateTime' : self.DateTime,
            'Kwh' : self.Kwh,
            'old_kwh' : self.old_kwh,
            'delta_kwh' : self.delta_kwh,
            'kluster' : self.kluster
        }

class KlasterVirtualPerhariSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KlasterVirtualPerhari
        created_at = auto_field(dump_only=True)

class KlasterVirtualPerbulan(db.Model):
    __tablename__ = "KlasterVirtualPerbulan"
    MyUnknownColumn = db.Column(db.Integer)
    DateTime = db.Column(db.String(50), primary_key=True)
    Kwh = db.Column(db.Float)
    old_kwh = db.Column(db.Float)
    delta_kwh = db.Column(db.Float)
    kluster = db.Column(db.Integer)

    def to_dict(self):
        return {
            'MyUnknownColumn' : self.MyUnknownColumn,
            'DateTime' : self.DateTime,
            'Kwh' : self.Kwh,
            'old_kwh' : self.old_kwh,
            'delta_kwh' : self.delta_kwh,
            'kluster' : self.kluster
        }

class KlasterVirtualPerbulanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KlasterVirtualPerbulan
        created_at = auto_field(dump_only=True)

class KlasterVirtualPertahun(db.Model):
    __tablename__ = "KlasterVirtualPertahun"
    DateTime = db.Column(db.String(50), primary_key=True)
    Kwh = db.Column(db.Float)
    old_kwh = db.Column(db.Float)
    delta_kwh = db.Column(db.Float)
    kluster = db.Column(db.Integer)

    def to_dict(self):
        return {
            'DateTime' : self.DateTime,
            'Kwh' : self.Kwh,
            'old_kwh' : self.old_kwh,
            'delta_kwh' : self.delta_kwh,
            'kluster' : self.kluster
        }

class KlasterVirtualPertahunSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KlasterVirtualPertahun
        created_at = auto_field(dump_only=True)

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
    device_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    device_name = db.Column(db.String(100))
    daya_device = db.Column(db.Float)
    jumlah_device = db.Column(db.Integer)
    total_daya = db.Column(db.Float)
    tingkat_prioritas = db.Column(db.String(100))
    device_name_status = db.Column(db.String(100))
    device_name_read = db.Column(db.String(100))
    device_token = db.Column(db.String(100))
 
    def __init__(self, userID, username, deviceName, daya, jumlah_device, total_daya, prioritas, device_status, device_read, device_token):
        self.user_id = userID
        self.username = username
        self.device_name = deviceName
        self.daya_device = daya
        self.jumlah_device = jumlah_device
        self.total_daya = total_daya
        self.tingkat_prioritas = prioritas
        self.device_name_status = device_status
        self.device_name_read = device_read
        self.device_token = device_token

    def to_dict(self):
        return {
            'user_id' : self.user_id,
            'username' : self.username,
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

class device_usage_duration(db.Model):
    user_id = db.Column(db.Integer)
    device_id = db.Column(db.Integer, nullable=False, primary_key=True)
    device_name = db.Column(db.String(50), nullable=False)
    duration_scheduled = db.Column(db.String(50), nullable=False)
    duration_used = db.Column(db.String(50), nullable=False)
    duration_left = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, device_id, device_name, duration_scheduled, duration_left):
        self.user_id = user_id
        self.device_id  = device_id
        self.device_name = device_name
        self.duration_scheduled = duration_scheduled
        self.duration_used = duration_used
        self.duration_left = duration_left
    
    def to_dict(self):
        return {
            'user_id' : self.user_id,
            'device_id' : self.device_id,
            'device_name' : self.device_name,
            'duration_scheduled' : self.duration_scheduled,
            'duration_used' : self.duration_used,
            'duration_left' : self.duration_left,
        }

class device_usage_durationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = device_usage_duration
        created_at = auto_field(dump_only=True)