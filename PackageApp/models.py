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

#-------------------------------------------------------------
class Parameter(db.Model):  # Tham số
    __tablename__ = "parameter"

    id = Column(Integer,primary_key=True,autoincrement=True)
    number_custommer_max = Column(Integer, nullable=False)
    guest_coefficient = Column(Float, nullable=False)
    surcharge = Column(Integer, nullable=False)
    rental_slips = relationship('RentalSlip', backref="Parameter", lazy=True)
    custommer_type = relationship('CustommerType', backref="Parameter", lazy=True)

    def __str__(self):
        return self.number_custommer_max.__str__() + " người  / " + self.surcharge.__str__() + " %"


# ---------------------------------------------------------------------------------
class RentalSlip(db.Model):  # Phiếu thuê phòng
    __tablename__ = "rentalslip"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hire_start_date = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    bills = relationship('Bill', backref="RentalSlip", lazy=True)
    parameter_amount = Column(Integer, ForeignKey(Parameter.id), nullable=False)
    details = relationship('DetailsRentalSlip', backref="RentalSlip", lazy=True)

    def __str__(self):
        return self.room_id.__str__()


# ---------------------------------------------------------------------------------
class CustommerType(db.Model):  # Loại khách hàng
    __tablename__ = "custommertype"
    id = Column(Integer, primary_key=True, autoincrement=True)
    custommer_type_name = Column(String(50), nullable=False)
    parameter_id = Column(Integer, ForeignKey(Parameter.id),nullable=False)
    details_t = relationship('DetailsRentalSlip', backref="CustommerType", lazy=True)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.custommer_type_name
    """
    STOP >>>?
    """


# ---------------------------------------------------------------------------------
class DetailsRentalSlip(db.Model):  # Chi tiết phiếu thuê phòng
    __tablename__ = "detailsrentalslip"
    id = Column(Integer, primary_key=True, autoincrement=True)
    custommer_name = Column(String(50), nullable=False)
    custommer_type_id = Column(Integer, ForeignKey(CustommerType.id), nullable=False)
    identity_card = Column(String(50), nullable=False)
    address = Column(String(255), nullable=False)
    rental_slip_id = Column(Integer, ForeignKey(RentalSlip.id), nullable=False)

    pass




# ---------------------------------------------------------------------------------
class Bill(db.Model):  # Hóa đơn
    __tablename__ = "bill"
    id = Column(Integer, primary_key=True, autoincrement=True)
    custommer_name = Column(String(50), nullable=False)
    custommer_address = Column(String(255), nullable=False)
    date_of_payment = Column(DateTime, nullable=False, default=0)
    value = Column(Integer, nullable=False, default=0)
    rental_slip_id = Column(Integer, ForeignKey(RentalSlip.id), nullable=False)
    pass


# ---------------------------------------------------------------------------------
class DetailsOfBill(db.Model):  # Chi tiết hóa đơn
    __tablename__ = "detailsofbill"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey(Bill.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    number_of_rental_days = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False, default=0)
    into_money = Column(Integer, nullable=False)
    pass


# ham chay khoi tao database len mysql
if __name__ == "__main__":
    db.create_all()

