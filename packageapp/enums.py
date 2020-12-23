import enum # Kiểu liệt kê


class InteriorDesignStyle(enum.Enum): # Các phong cách thiết kế của khách sạn
    ModernAndSimple = "Hiện đại và đơn giản"
    ModernAndLuxurious = "Hiện đại và sang trọng"
    ClassicAndLuxurious = "Cổ điển và sang trọng"
    NewClassical = "Tân cổ điển"
    Classic = "Cổ điển"


class ImportFromCountry(enum.Enum):# Khách sạn chỉ nhập khẩu từ 4 nước Anh/Pháp/Ý/Đức
    England = "Anh Quốc"
    France = "Pháp"
    Italian = "Ý"
    Germany = "Đức"


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




