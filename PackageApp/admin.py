from datetime import date, datetime

from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from wtforms import validators
from flask_login import current_user, logout_user
from markupsafe import Markup
from urllib import request
from PackageApp.models import *
from PackageApp import admin, db, dao
from flask import redirect, request, session

import hashlib, math


# -------------------------- Phần ModelView --------------------------------------

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


# ------
class UserModelView(AuthenticatedView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_view_details = True
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
    can_view_details = True
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
    can_view_details = True
    column_labels = dict(id="Mã loại giường", tob_name="Tên loại giường", tob_quality="Chất lượng loại giường",
                         import_from_country="Nhập từ quốc gia", tob_rates="Giá loại giường [Setuped]",
                         description="Thông tin mô tả")
    form_columns = ("tob_name", "tob_quality", "import_from_country", "tob_rates", "description")

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class ServicesModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_view_details = True
    column_labels = dict(id="Mã dịch vụ", ser_name="Tên dịch vụ", ser_rates="Giá dịch vụ", description="Mô tả thêm")
    form_columns = ("ser_name", "ser_rates", "description")

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class RoomModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_view_details = True
    column_labels = dict(id="Mã phòng", room_name="Tên phòng", KindsOfRoom="Loại phòng  [Setup]",
                         TypeOfBed="Loại giường  [Setup]", Services="Dịch vụ  [Setup]",
                         img_kor="Hình ảnh loại phòng", img_tob="Hình ảnh loại giường",
                         room_status="Tình trạng phòng", room_amount="Số lượng phòng", notes="Ghi chú")
    form_columns = ("room_name", "KindsOfRoom", "TypeOfBed", "Services", "img_kor", "img_tob", "room_status",
                    "room_amount", "notes")
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

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class SurchargeModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_view_details = True
    column_list = ["surcharge_amount", "surcharge_rate"]
    column_labels = {
        "surcharge_amount": "Số lượng phụ thu",
        "surcharge_rate": "Tỷ lệ Phụ thu theo (%)"
    }
    form_excluded_columns = ['rentalSlip']

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


class CustommerTypeModelView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_view_details = True
    form_columns = ('customer_type_name', 'coefficient', 'note')
    column_labels = {
        "id": "Mã loại khách",
        "customer_type_name": "Loại khách hàng",
        "coefficient": "Hệ số loại khách",
        "note": "Ghi chú thêm"}

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


class RentalSlipModeView(ModelView):
    column_display_pk = True  # HIển thị khóa chính ra
    can_view_details = True
    column_labels = {
        "id": "Mã phiếu",
        "Room": "Phòng thuê",
        "hire_start_date": "Ngày thuê",
        "customer_name": "Khách thuê",
        "Surcharge": "SL và PT khi thuê",
        "CustommerType": "Loại khách",
        "identity_card": "Chứng minh thư",
        "address": "Địa chỉ"}
    form_excluded_columns = ['bills']

    def on_model_change(self, form, RentalSlip, is_created):
        room = Room.query.get(form.Room.data.id)
        if form.Room.data.room_status == StatusOfRoom.isOccupied:
            raise validators.ValidationError("Phòng đã có người đặt")

        else:
            room.room_status = StatusOfRoom.isOccupied
            db.session.add(room)
            db.session.commit()

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class BillModelView(AuthenticatedView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_labels = {
        "id": "Mã hóa đơn",
        "date_of_payment": "Số ngày thanh toán",
        "total_value": "Tổng trị giá",
        "into_money": "Thành tiền",
        "RentalSlip": "Mã phiếu thuê"
    }
    form_excluded_columns = ['date_of_payment', 'total_value', 'into_money']

    def on_model_change(self, form, Bill, is_created):
        room = Room.query.get(form.RentalSlip.data.room_id)
        if form.RentalSlip.data.Room.room_status == StatusOfRoom.isOccupied:
            room.room_status = StatusOfRoom.isVacant
            db.session.add(room)
            db.session.commit()

        if (datetime.now() - form.RentalSlip.data.hire_start_date).days == 0:
            payment_by_invoice = (datetime.now().hour - form.RentalSlip.data.hire_start_date.hour)
        else:
            payment_by_invoice = (datetime.now() - form.RentalSlip.data.hire_start_date).days * 24
            price_by_time = (payment_by_invoice * form.RentalSlip.data.Room.KindsOfRoom.kor_rates +
                             form.RentalSlip.data.Room.TypeOfBed.tob_rates +
                             form.RentalSlip.data.Room.Services.ser_rates)

        Bill.date_of_payment = payment_by_invoice / 24  # so ngay
        Bill.total_value = price_by_time
        if (form.RentalSlip.data.Surcharge.surcharge_rate == 0
                and form.RentalSlip.data.CustommerType.coefficient == 0):
            Bill.into_money = price_by_time
        else:
            if form.RentalSlip.data.Surcharge.surcharge_rate != 0 \
                    and form.RentalSlip.data.CustommerType.coefficient == 0:
                Bill.into_money = price_by_time + (price_by_time *
                                                   (form.RentalSlip.data.Surcharge.surcharge_rate / 100))
            else:
                if form.RentalSlip.data.Surcharge.surcharge_rate == 0 \
                        and form.RentalSlip.data.CustommerType.coefficient != 0:
                    Bill.into_money = price_by_time * form.RentalSlip.data.CustommerType.coefficient
                else:
                    if form.RentalSlip.data.Surcharge.surcharge_rate != 0 \
                            and form.RentalSlip.data.CustommerType.coefficient != 0:
                        Bill.into_money = price_by_time * form.RentalSlip.data.CustommerType.coefficient + \
                                          (price_by_time + (price_by_time *
                                                            (form.RentalSlip.data.Surcharge.surcharge_rate / 100)))


# ------
class ChangeTheRolesView(ModelView):
    __tablename__ = "changetherules"
    column_display_pk = True
    can_create = True
    can_set_page_size = True
    can_view_details = True
    column_labels = {
        "id": "Mã quy đinh",
        "name_change": "Tên quy định",
        "contents": "Nội dung",
        "User": "Người dùng truy cập"

    }

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


class ChangeRolesView(BaseView):
    @expose("/")
    def index(self):
        ch_name = request.args.get("name_change")
        ch_content = request.args.get("contents")
        us_id = request.args.get("us")

        return self.render("admin/change-rules.html",
                           changetherules=dao.dao_change_rule_infor(name_change=ch_name, contents=ch_content,

                                                                    user_id=us_id))


# ------
class AboutUsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# ------
class LogoutAdminView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


class RoomListView(BaseView):
    @expose("/")
    def index(self):
        r_name = request.args.get("name")
        k_o_r_id = request.args.get("kor")
        r_status = request.args.get("status")
        r_amount = request.args.get("amount")

        return self.render("admin/room-list.html",
                           room=dao.dao_room_info(room_name=r_name, kinds_of_room_id=k_o_r_id,
                                                  room_status=r_status, room_amount=r_amount),
                           room_status=StatusOfRoom)


class ReportView(BaseView):
    @expose("/")
    def __index__(self, ):
        at_month = request.args.get("at_month") or 0
        session['at_month'] = at_month
        return self.render('admin/report-tatistics.html',
                           kinds_of_room_A=len(dao.kinds_of_room_A(at_month=at_month)),
                           kinds_of_room_B=len(dao.kinds_of_room_B(at_month=at_month)),
                           kinds_of_room_C=len(dao.kinds_of_room_C(at_month=at_month)),
                           custommer=dao.payment_customers(),
                           date=date.today(),
                           total_payment=dao.total_revenue())

    def is_accessible(self):
        return current_user.is_authenticated and \
               (current_user.user_roles == "Admin-(Quản trị viên)")


# --------------------------------------------------------------------------------
admin.add_view(RoomListView(name="Danh sách các phòng"))
admin.add_view(KindsOfRoomModelView(KindsOfRoom, db.session, name="Loại phòng"))
admin.add_view(TypeOfBedModelView(TypeOfBed, db.session, name="Loại giường"))
admin.add_view(ServicesModelView(Services, db.session, name="Dịch vụ"))
admin.add_view(RoomModelView(Room, db.session, name="Quản lý phòng"))
admin.add_view(CustommerTypeModelView(CustommerType, db.session, name="Loại khách hàng"))
admin.add_view(RentalSlipModeView(RentalSlip, db.session, name="Phiếu thuê phòng"))
admin.add_view(BillModelView(Bill, db.session, name="Hóa đơn"))
admin.add_view(SurchargeModelView(Surcharge, db.session, name="Bảng phụ thu"))
admin.add_view(UserModelView(User, db.session, name="Người dùng"))
admin.add_view(ReportView(name="Báo báo thống kê"))
admin.add_view(ChangeTheRolesView(ChangeTheRules, db.session, name="Thay đổi qui định"))
admin.add_view(ChangeRolesView(name="Quy định của khách sạn"))
admin.add_view(AboutUsView(name="Giới thiệu"))
admin.add_view(LogoutAdminView(name="Đăng xuất"))
