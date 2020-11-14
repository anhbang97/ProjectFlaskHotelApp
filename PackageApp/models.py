from PackageApp import db, RoomStatus, admin
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin, current_user, logout_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(50), nullable=False)
    user_active = Column(Boolean,default=True)
    user_name = Column(String(50), nullable=False)
    user_password = Column(String(50), nullable=False)
    user_roles = Column(String(50), nullable=False)

    def __str__(self):
        return self.user_name

#---------------------------------------------------------------------------


class KindsOfRoom(db.Model):
    __tablename__ = "kindsofroom"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kor_name = Column(String(50), nullable= False)
    kor_price = Column(Integer, nullable= False)
    kor_description = Column(String(255), nullable=True)

    room_k = relationship('Room', backref="KindsOfRoom", lazy=True)

    def __str__(self):
        return self.kor_name

#-----------------------------------------------------------------------------


class TypeOfBed(db.Model):
    __tablename__ = "typeofbed"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tob_name = Column(String(50), nullable=False)
    tob_price = Column(Integer, nullable=False)
    tob_description = Column(String(255), nullable=True)

    room_t = relationship('Room', backref="TypeOfBed", lazy=True)

    def __str__(self):
        return self.tob_name
#---------------------------------------------------------------------------


class Room(db.Model):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(50), nullable=False)
    images = Column(String(255), nullable=True)
    room_status = Column(Enum(RoomStatus), nullable= True)
    kor_id = Column(Integer, ForeignKey(KindsOfRoom.id), nullable=False)
    tob_id = Column(Integer, ForeignKey(TypeOfBed.id), nullable=False)

    rental_slip = relationship('RentalSlip', backref="Room", lazy=True)

    def __str__(self):
        return self.room_name
#--------------------------------------------------------------------------------------


class CustommerType(db.Model):
    __tablename__ = "custommertype"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cus_type_name = Column(String(50), nullable=False)
    coefficient = Column(Float, nullable=False)
    description_note = Column(String(255), nullable=True)

    def __str__(self):
        return self.cus_type_name
#--------------------------------------------------------------------------------------


class Surcharge(db.Model):
    __tablename__ = "surcharge"

    id = Column(Integer, primary_key=True, autoincrement= True)
    sur_amount = Column(Integer, nullable= False)
    people_amount = Column(Integer, nullable=False)

    def __str__(self):
        return self.people_amount.__str__() + "người - " + self.sur_amount + "%"

#---------------------------------------------------------------------------------


class RentalSlip(db.Model):
    __tablename__ = "rentalslip"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hire_start_date = Column(DateTime, nullable=False)
    custommer_name = Column(String(50), nullable=False)
    rental_amount = Column(String(50), ForeignKey(Surcharge.id), nullable= False)
    identity_card = Column(Integer, nullable=False)
    address = Column(String(255), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    cus_type_id = Column(Integer, ForeignKey(CustommerType.id), nullable=False)

    bills = relationship('Bill', backref="RentalSlip", lazy=True)

    def __str__(self):
        return self.id.__str__()

#------------------------------------------------------------------------------------


class Bill(db.Model):
    __tablename__ = "bill"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_of_payment = Column(DateTime, nullable=False, default=0)
    total_amount_price = Column(Integer, nullable=False, default=0)
    com_total_price = Column(Integer,  nullable=False, default= 0)
    rental_id = Column(Integer, ForeignKey(RentalSlip.id), nullable=False)

    def __str__(self):
        return self.custommer_name

#--------------------------------------------------------------------------------

#-------------------------- Phần ModelView --------------------------------------


class UserModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_create = True
    can_edit = True
    can_export = True
    pass


class KindsOfRoomModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_create = True
    can_export = True
    pass


class TypeOfBedModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_create = True
    can_export = True
    pass


class RoomModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_create = True
    can_export = True
    pass


class CustommerTypeModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_create = True
    can_export = True
    pass


class SurchargeModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_create = True
    can_export = True
    pass


class RentalSlipModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_create = True
    can_export = True
    pass


class BillModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_create = True
    can_export = True
    pass

#-----------------------------------


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
#--------------------------------------------------------------------------------


admin.add_view(UserModelView(User, db.session))
admin.add_view(KindsOfRoomModelView(KindsOfRoom, db.session))
admin.add_view(TypeOfBedModelView(TypeOfBed, db.session))
admin.add_view(RoomModelView(Room, db.session))
admin.add_view(CustommerTypeModelView(CustommerType, db.session))
admin.add_view(SurchargeModelView(Surcharge, db.session))
admin.add_view(RentalSlipModelView(RentalSlip, db.session))
admin.add_view(BillModelView(Bill, db.session))


#---------------------------------
admin.add_view(AboutUsView(name="About Us"))
admin.add_view(LogoutAdminView(name="Logout"))
# ham chay khoi tao database len mysql
if __name__ == "__main__":
    db.create_all()