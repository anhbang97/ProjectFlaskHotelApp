from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from wtforms import validators
from flask_login import current_user, logout_user
from markupsafe import Markup

from PackageApp.models import *
from PackageApp import admin, db, dao
from flask import redirect, request, session

import hashlib


# -------------------------- Phần ModelView --------------------------------------


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


# ------
class UserModelView(AuthenticatedView):
    column_display_pk = True  # HIển thị khóa chính ra

    column_labels = dict(id="Mã người dùng", fullname="Tên người dùng", user_active="Kích hoạt",
                         user_name="Tên đăng nhập",
                         user_password="Mật khẩu", user_roles="Vai trò người dùng")
    form_columns = ("fullname", "user_active", "user_name", "user_password", "user_roles")

    def on_model_change(self, form, User, is_created=False):
        User.user_password = hashlib.md5(User.user_password.encode('utf-8')).hexdigest()

    form_widget_args = {
        'user_password': {
            'type': 'password'
        }
    }

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class KindsOfRoomModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    column_labels = dict(id="Mã loại phòng", kor_name="Tên loại phòng", kor_quality="Chất lượng loại phòng",
                         interior_design_style="Kiểu thiết kế", kor_rates="Giá loại phòng",
                         description="Thông tin mô tả")
    form_columns = ("kor_name", "kor_quality", "interior_design_style", "kor_rates", "description")

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class TypeOfBedModelView(ModelView):
    column_display_pk = True  # Hiển thị khóa chính ra
    column_labels = dict(id="Mã loại giường", tob_name="Tên loại giường", tob_quality="Chất lượng loại giường",
                         import_from_country="Nhập từ quốc gia", tob_rates="Giá loại phòng",
                         description="Thông tin mô tả")
    form_columns = ("tob_name", "tob_quality", "import_from_country", "tob_rates", "description")

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class ServicesModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    column_labels = dict(id="Mã dịch vụ", ser_name="Tên dịch vụ", ser_rates="Giá dịch vụ", description="Mô tả thêm")
    form_columns = ("ser_name", "ser_rates", "description")

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class RoomModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra

    column_labels = dict(id="Mã phòng", room_name="Tên phòng", KindsOfRoom="Loại phòng  [Setup]",
                         TypeOfBed="Loại giường  [Setup]",
                         Services="Dịch vụ  [Setup]", img_kor="Hình ảnh loại phòng", img_tob="Hình ảnh loại giường",
                         room_status="Tình trạng phòng", room_amount="Số lượng phòng", notes="Ghi chú")
    form_columns = ("room_name", "KindsOfRoom", "TypeOfBed", "Services", "img_kor", "img_tob", "room_status", "room_amount", "notes")
    form_excluded_columns = ['rental_slips']

    def _room_status_formatter(view, context, model, name):
        if model.room_status:
            status = model.room_status.value
            return status
        else:
            return None

    def base64_img_kor_formatter(view, context, model, name):
        img_kor = getattr(model, name, '')
        if img_kor:
            img = Markup('<img src="data:image/jpg;base64,{}" width="100"/>'.format(model.img_kor))
            return img

    def base64_img_tob_formatter(view, context, model, name):
        img_tob = getattr(model, name, '')
        if img_tob:
            img = Markup('<img src="data:image/jpg;base64,{}" width="100"/>'.format(model.img_tob))
            return img

    column_formatters = {
        'img_kor': base64_img_kor_formatter,
        'img_tob': base64_img_tob_formatter,
        'room_status': _room_status_formatter

     }


# ------
class CustommerTypeModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra

    column_labels = dict(id="Mã loại khách hàng", custommer_type_name="Loại khách hàng", Parameter="Tham số")
    form_columns = ("custommer_type_name", "Parameter")
    form_excluded_columns= ['details_t']

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")

    """
    STOP >>>>> ?
    """


# ------
class RentalSlipModeView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    column_labels = dict(id="Mã phiếu thuê", hire_start_date="Ngày bắt đầu thuê", Room="Phòng thuê",Parameter="Số lượng phụ thu")
    form_columns = ("hire_start_date", "Room", "Parameter")
    form_excluded_columns = ['bills', 'details']

    def on_model_change(self, form, RentalSlip, is_created):
        room = Room.query.get(form.Room.data.id)
        if form.Room.data.room_status == StatusOfRoom.isOccupied:
            raise validators.ValidationError("Phòng đã có người đặt")
        else:
            room.room_status = StatusOfRoom.isOccupied
            db.session.add(room)
            db.session.commit()
    pass


# ------
class DetailsRentalSlipModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    column_labels = dict(id="Mã chi tiết phiếu thuê", custommer_name="Họ tên khách hàng",CustommerType="Loại khách hàng",
                         identity_card="Chứng minh thư", address="Địa chỉ", RentalSlip="Phiếu thuê")

    form_columns = ("custommer_name", "CustommerType", "identity_card", "address", "RentalSlip")
    pass


# ------
class ParameterModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    column_labels = dict(id="Mã tham số phụ thu", number_custommer_max="Số khách hàng",
                         guest_coefficient="Hệ số khách", surcharge= "Phụ phí thu (%)")
    form_columns = ("number_custommer_max", "guest_coefficient", "surcharge")
    form_excluded_columns = ['rental_slips', 'custommer_type']
    pass


# ------
class BillModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass


# ------
class DetailsOfBillModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    pass




# ------
class AboutUsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")


# ------
class LogoutAdminView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


# --------------------------------------------------------------------------------
admin.add_view(KindsOfRoomModelView(KindsOfRoom, db.session, name="Loại phòng"))
admin.add_view(TypeOfBedModelView(TypeOfBed, db.session, name="Loại giường"))
admin.add_view(ServicesModelView(Services, db.session, name="Dịch vụ"))
admin.add_view(RoomModelView(Room, db.session, name="Quản lý phòng"))
admin.add_view(CustommerTypeModelView(CustommerType, db.session, name="Loại khách hàng"))
admin.add_view(RentalSlipModeView(RentalSlip, db.session, name="Phiếu thuê"))
admin.add_view(DetailsRentalSlipModelView(DetailsRentalSlip, db.session, name="Chi tiết phiếu thuê"))
admin.add_view(BillModelView(Bill, db.session, name="Hóa đơn"))
admin.add_view(DetailsOfBillModelView(DetailsOfBill, db.session, name="Chi tiết hóa đơn"))
admin.add_view(ParameterModelView(Parameter, db.session, name="Tham số phụ thu"))
admin.add_view(UserModelView(User, db.session, name="Người dùng"))
admin.add_view(AboutUsView(name="Giới thiệu"))
admin.add_view(LogoutAdminView(name="Đăng xuất"))
