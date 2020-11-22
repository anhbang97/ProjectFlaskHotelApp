import enum # Kiểu liệt kê


class StatusOfRoom(enum.Enum):
    isVacant = "Phòng đang trống"
    isOccupied = "Phòng đang có khách"


class AvailableKindsOfRoom(enum.Enum):  # Các chuẩn kiểu phòng chỉ có trong khách sạn
    STD = "STANDARD"
    SUP = "SUPERIOR"
    DLX = "DELUXE"
    SUT = "SUITE"


class AvailableTypeOfBed(enum.Enum): # Các chuẩn kiểu giường chỉ có trong khách sạn
    SGL = "SINGLE BED ROOM"
    TWN = "TWINS BED ROOM"
    DBL = "DOUBLE BED ROOM"
    TRPL = "TRIPLE BED ROOM"

