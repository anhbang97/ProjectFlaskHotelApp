from sqlalchemy import extract


from PackageApp.models import *


def dao_room_info(room_name=None, kinds_of_room_id=None, type_of_bed_id=None, services_id=None, img_kor=None,
                  img_tob=None, room_status=None, room_amount=None, notes=None):
    roo = Room.query.all()
    kor = str(kinds_of_room_id)
    tob = str(type_of_bed_id)
    ser = str(services_id)

    if room_name:
        roo = filter(lambda tt: tt.room_name == room_name, roo)
    if kinds_of_room_id:
        roo = list(filter(lambda tt: tt.KindsOfRoom.kor_name == kor, roo))
    if type_of_bed_id:
        roo = list(filter(lambda tt: tt.TypeOfBed.tob_name == tob, roo))
    if services_id:
        roo = list(filter(lambda tt: tt.Services.ser_name == ser, roo))
    if room_status:
        roo = filter(lambda tt: tt.room_status.value == room_status, roo)

    return roo


def dao_change_rule_infor(name_change=None, contents=None, user_id=None):
    chri = ChangeTheRules.query.all()
    us = str(user_id)

    if name_change:
        chri = filter(lambda tt: tt.name_change == name_change,chri)
    if contents:
        chri = filter(lambda tt: tt.contents == contents, chri)
    if user_id:
        chri = list(filter(lambda tt: tt.User.user_name == us, chri))
    return chri


def kinds_of_room_A(at_month=0):
    revenue_statistics = RentalSlip.query.filter(extract('month', RentalSlip.hire_start_date) == at_month).all()
    revenue_statistics_A = list(filter(lambda tk: tk.roo.kor == KindsOfRoom.kor_name, revenue_statistics))
    return revenue_statistics_A


def kinds_of_room_B(at_month=0):
    revenue_statistics = RentalSlip.query.filter(extract('month', RentalSlip.hire_start_date) == at_month).all()
    revenue_statistics_B = list(filter(lambda tk: tk.roo.kor == KindsOfRoom.kor_name, revenue_statistics))
    return revenue_statistics_B


def kinds_of_room_C(at_month=0):
    revenue_statistics = RentalSlip.query.filter(extract('month', RentalSlip.hire_start_date) == at_month).all()
    revenue_statistics_C = list(filter(lambda tk: tk.roo.kor == KindsOfRoom.kor_name, revenue_statistics))
    return revenue_statistics_C


def payment_customers():
    revenue_kor = Bill.query.all()
    revenue_kor = list(filter(lambda tk: tk.into_money != 0, revenue_kor))
    return revenue_kor


def total_revenue():
    revenue_kor = Bill.query.all()
    revenue_kor = list(filter(lambda tk: tk.into_money != 0, revenue_kor))
    total_revenue = 0
    for p in revenue_kor:
        total_revenue += p.into_money

    return total_revenue