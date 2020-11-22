from PackageApp import db, admin, StatusOfRoom,AvailableKindsOfRoom,AvailableTypeOfBed
from sqlalchemy import Column, String, Integer, Boolean, Enum, ForeignKey, DateTime
from flask_login import UserMixin, current_user, logout_user
from sqlalchemy.orm import relationship
from  flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect





class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Khóa chính
    fullname = Column(String(50), nullable=False)
    user_active = Column(Boolean, default=True)  # Trạng thái hoạt động của user
    user_name = Column(String(50), nullable=False)  # Tên đăng nhập
    user_password = Column(String(50), nullable=False)  # Mật khẩu
    user_roles = Column(String(50), nullable=False)  # Phân quyền quản trị

    pass


# ---------------------------------------------------------------------------
class KindsOfRoom(db.Model):  # Loại phòng
    __tablename__ = "kindsofroom"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Khóa chính
    kor_name = Column(String(50), nullable=False)  # Tên loại phòng
    kor_quality = Column(Enum(AvailableKindsOfRoom), nullable=False)
    kor_rates = Column(Integer, nullable=False)  # Giá của loại phòng
    description = Column(String(255), nullable=True)  # Mô tả
    rooms = relationship('Room', backref="KindsOfRoom", lazy=True)
    pass


# --------------------------------------------------------------------------------
class TypeOfBed(db.Model):  # Kiểu giường nằm trong phòng
    __tablename__ = "typeofbed"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Khóa chính
    tob_name = Column(String(50), nullable=False)  # Tên của loại giường
    tob_quality = Column(Enum(AvailableTypeOfBed), nullable=False)
    tob_rates = Column(Integer, nullable=False)  # Giá của loại giường
    description = Column(String(255), nullable=True)  # Mô tả
    rooms = relationship('Room', backref="TypeOfBed", lazy=True)
    pass


# ---------------------------------------------------------------------------------
class Services(db.Model):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ser_name = Column(String(50), nullable=False)
    ser_rates = Column(Integer, nullable=False)
    description = Column(String(50), nullable=True)
    rooms = relationship('Room', backref="Services", lazy=True)
    pass


# --------------------------------------------------------------------------------
class Room(db.Model):  # Phòng
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(50), nullable=False)
    room_number = Column(Integer, nullable=False)
    room_status = Column(Enum(StatusOfRoom), nullable=True)
    img_kor = Column(String(50), nullable=True)
    img_tob = Column(String(50), nullable=True)
    notes = Column(String(50), nullable=True)
    kinds_of_room_id = Column(Integer, ForeignKey(KindsOfRoom.id), nullable=False)
    type_of_bed_id = Column(Integer, ForeignKey(TypeOfBed.id), nullable=False)
    services_id = Column(Integer, ForeignKey(Services.id), nullable=False)
    rental_slips = relationship('RentalSlip', backref="Rooms", lazy=True)
    pass


#-------------------------------------------------------------
class Parameter(db.Model):  # Tham số
    __tablename__ = "parameter"

    id = Column(Integer,primary_key=True,autoincrement=True)
    number_custommer_max = Column(Integer, nullable=False)
    guest_coefficient = Column(Integer, nullable=False)
    surcharge = Column(Integer, nullable=False)
    rental_slips = relationship('RentalSlip', backref="Parameter", lazy=True)
    pass


# ---------------------------------------------------------------------------------
class RentalSlip(db.Model):  # Phiếu thuê phòng
    __tablename__ = "rentalslip"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hire_start_date = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    bills = relationship('Bill', backref="RentalSlip", lazy=True)
    parameter_amount = Column(Integer, ForeignKey(Parameter.id), nullable=False)
    pass


# ---------------------------------------------------------------------------------
class CustommerType(db.Model):  # Loại khách hàng
    __tablename__ = "custommertype"
    id = Column(Integer, primary_key=True, autoincrement=True)
    custommer_type_name = Column(String(50), nullable=False)
    pass


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


# ---------------------------------------------------------------------------------

# -------------------------- Phần ModelView --------------------------------------



class UserModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra

    can_create = True
    can_edit = True
    can_export = True
    column_labels = dict(fullname="Tên người dùng", user_active="Kích hoạt", user_name="Tên đăng nhập",
                         user_password="Mật khẩu", user_roles="Vai trò người dùng")

    pass


class KindsOfRoomModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class TypeOfBedModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class ServicesModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class RoomModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class RentalSlipModeView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class CustommerTypeModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class DetailsRentalSlipModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class BillModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class DetailsOfBillModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


class ParameterModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass
# --------------Class Database View---------------------


# ------------------------------------
class AboutUsView(BaseView):
    @expose("/")
    def __index__(self):
        return self.render("admin/about-us.html")

    def is_accessible(self):
        return current_user.is_authenticated

    pass


class LogoutAdminView(BaseView):
    @expose("/")
    def __index__(self):
        logout_user()
        return redirect("/admin")


# --------------------------------------------------------------------------------


admin.add_view(UserModelView(User, db.session, name="Quản lý người dùng"))
admin.add_view(KindsOfRoomModelView(KindsOfRoom,db.session, name="Quản lý các loại phòng"))
admin.add_view(TypeOfBedModelView(TypeOfBed,db.session,name="Quản lý các loại giường"))
admin.add_view(ServicesModelView(Services,db.session, name="Quản lý các dịch vụ"))
admin.add_view(RoomModelView(Room,db.session,name="Quản lý phòng"))
admin.add_view(CustommerTypeModelView(CustommerType, db.session, name="Quản lý loại khách hàng"))
admin.add_view(RentalSlipModeView(RentalSlip, db.session, name="Quản lý phiếu thuê"))
admin.add_view(DetailsRentalSlipModelView(DetailsRentalSlip, db.session, name="Quản lý chi tiết phiếu thuê"))
admin.add_view(BillModelView(Bill, db.session, name="Quản lý hóa đơn"))
admin.add_view(DetailsOfBillModelView(DetailsOfBill, db.session, name="Quản lý chi tiết hóa đơn"))
admin.add_view(ParameterModelView(Parameter, db.session, name="Quản lý tham số phụ thu"))
# ---------------------------------

admin.add_view(AboutUsView(name="Giới thiệu"))
admin.add_view(LogoutAdminView(name="Đăng xuất"))

# ham chay khoi tao database len mysql
if __name__ == "__main__":
    db.create_all()

