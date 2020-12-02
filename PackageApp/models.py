from PackageApp import db, StatusOfRoom, AvailableKindsOfRoom, AvailableTypeOfBed, InteriorDesignStyle, \
    ImportFromCountry
from sqlalchemy import Column, String, Integer, Boolean, Enum, ForeignKey, DateTime,Float
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Khóa chính
    fullname = Column(String(50), nullable=False)
    user_active = Column(Boolean, default=True)  # Trạng thái hoạt động của user
    user_name = Column(String(50), nullable=False)  # Tên đăng nhập
    user_password = Column(String(50), nullable=False)  # Mật khẩu
    user_roles = Column(String(50), nullable=False)  # Phân quyền quản trị

    def get_id(self):
        return self.id

    def __str__(self):
        return self.fullname


# ---------------------------------------------------------------------------
class KindsOfRoom(db.Model):  # Loại phòng
    __tablename__ = "kindsofroom"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Khóa chính
    kor_name = Column(String(50), nullable=False)  # Tên loại phòng
    kor_quality = Column(Enum(AvailableKindsOfRoom), nullable=False)
    interior_design_style = Column(Enum(InteriorDesignStyle), nullable=True) # kiểu thiết kế phòng
    kor_rates = Column(Integer, nullable=False)  # Giá của loại phòng
    description = Column(String(255), nullable=True)  # Mô tả
    rooms = relationship('Room', backref="KindsOfRoom", lazy=True)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.kor_name


# --------------------------------------------------------------------------------
class TypeOfBed(db.Model):  # Kiểu giường nằm trong phòng
    __tablename__ = "typeofbed"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Khóa chính
    tob_name = Column(String(50), nullable=False)  # Tên của loại giường
    tob_quality = Column(Enum(AvailableTypeOfBed), nullable=False)
    import_from_country = Column(Enum(ImportFromCountry), nullable=True) # Giường nhập khẩu từ
    tob_rates = Column(Integer, nullable=False)  # Giá của loại giường
    description = Column(String(255), nullable=True)  # Mô tả
    rooms = relationship('Room', backref="TypeOfBed", lazy=True)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.tob_name


# ---------------------------------------------------------------------------------
class Services(db.Model):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ser_name = Column(String(50), nullable=False)
    ser_rates = Column(Integer, nullable=False)
    description = Column(String(250), nullable=True)
    rooms = relationship('Room', backref="Services", lazy=True)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.ser_name


# --------------------------------------------------------------------------------
class Room(db.Model):  # Phòng
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(50), nullable=False)
    kinds_of_room_id = Column(Integer, ForeignKey(KindsOfRoom.id), nullable=False)
    type_of_bed_id = Column(Integer, ForeignKey(TypeOfBed.id), nullable=False)
    services_id = Column(Integer, ForeignKey(Services.id), nullable=False)
    img_kor = Column(String(50), nullable=True)
    img_tob = Column(String(50), nullable=True)
    room_status = Column(Enum(StatusOfRoom), nullable=True)
    room_amount = Column(Integer, nullable=False)
    notes = Column(String(50), nullable=True)

    rental_slips = relationship('RentalSlip', backref="Room", lazy=True)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.room_name


# Bảng loại khách hàng
class CustommerType(db.Model):
    _tablename__ ="custommertype"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_type_name = Column(String(50), nullable=False)
    coefficient = Column(Float, nullable=False)
    note = Column(String(50), nullable=False)
    rentSlipDetails = relationship('RentalSlip', backref="CustomerType", lazy=True)

    def __str__(self):
        return self.customer_type_name


# Bảng phụ thu
class Surcharge(db.Model):
    __tablename__ = "surcharqe"
    id = Column(Integer,primary_key=True,autoincrement=True)
    surcharge_rate = Column(Integer, nullable=False) # Tỉ lệ phụ thu
    surcharge_amount = Column(Integer, nullable=False) # Số lượng phụ thu

    rentalSlip = relationship('RentalSlip', backref="Surcharge", lazy=True)

    def __str__(self):
        return self.surcharge_amount.__str__() + " người ~ " + self.surcharge_rate.__str__() + " %"


# Bảng phiếu thuê
class RentalSlip(db.Model):
    __tablename__ = "rentalslip"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(50), nullable=False)
    hire_start_date = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    surcharge_id = Column(Integer, ForeignKey(Surcharge.id), nullable=False)
    customer_type_id = Column(Integer, ForeignKey(CustommerType.id), nullable=False)
    identity_card = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    bills = relationship('Bill', backref="RentalSlip", lazy=True)

    def __str__(self):
        return self.id.__str__()


# ---------------------------------------------------------------------------------
class Bill(db.Model):  # Hóa đơn
    __tablename__ = "bill"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_of_payment = Column(Integer, nullable=False, default=0)  # ngày thanh toán
    total_value = Column(Integer, nullable=False, default=0)  # tổng trị giá
    into_money = Column(Integer, nullable=False, default=0)  # Thành tiền
    rentSlip_id = Column(Integer, ForeignKey(RentalSlip.id), nullable=False)

    def __str__(self):
        return self.customer_name


# ---------------------------------------------------------------------------------


# ham chay khoi tao database len mysql
if __name__ == "__main__":
    db.create_all()

