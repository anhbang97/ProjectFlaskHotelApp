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


def dao_custommer_type_infor(custommer_type_name=None, parameter_id=None):
    cus_type = CustommerType.query.all()
    par = str(parameter_id)

    if custommer_type_name:
        cus_type = filter(lambda tt: tt.custommer_type_name == custommer_type_name, cus_type)
    if parameter_id:
        cus_type = list(filter(lambda tt: tt.Parameter.number_custommer_max == par, cus_type))

    return cus_type


def dao_rental_slip_infor(hire_start_date=None, room_id=None, parameter_amount=None):
    rental_sl = RentalSlip.query.all()
    roo = str(room_id)
    para = str(parameter_amount)

    if hire_start_date:
        rental_sl = filter(lambda tt: tt.hire_start_date == hire_start_date, rental_sl)
    if room_id:
        rental_sl = list(filter(lambda tt: tt.Room.room_name == roo, rental_sl))
    if parameter_amount:
        rental_sl = list(filter(lambda tt: tt.Parameter.number_custommer_max == para, rental_sl))
    return rental_sl


def dao_details__rental_slip_infor(custommer_name=None,custommer_type_id=None,identity_card=None,
                                   address=None,rental_slip_id=None):
    details_rental = DetailsRentalSlip.query.all()
    cus_t_i = str(custommer_type_id)
    rent = str(rental_slip_id)

    if custommer_name:
        details_rental = filter(lambda tt: tt.custommer_name == custommer_name, details_rental)
    if custommer_type_id:
        details_rental = list(filter(lambda tt: tt.CustommerType.custommer_type_name == cus_t_i, details_rental))
    if identity_card:
        details_rental = filter(lambda tt: tt.identity_card.value == identity_card, details_rental)
    if address:
        details_rental = filter(lambda tt: tt.address.value == address, details_rental)
    if rental_slip_id:
        details_rental = list(filter(lambda tt: tt.RentalSlip.parameter_amount == rent, details_rental))
    return details_rental