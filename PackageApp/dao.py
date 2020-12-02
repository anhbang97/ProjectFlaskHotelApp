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

