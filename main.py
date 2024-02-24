import datetime
import uuid
import os
from prettytable import PrettyTable

PEAK_BEGIN = "18:00"
PEAK_END = "22:00"
NOW = "08:00"
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER = "0123456789"
MENU = """
        **************************************************************
        *                          MENU                              *
        **************************************************************
        *    1.   Bán Vé Mới                                         *
        *    2.   Hủy Vé Đã Bán                                      *
        *    3.   Thống kê số lượng vé đã bán                        *
        *    4.   Thống kê thông tin vé đã bán theo tên phim         *
        *    5.   Tính tổng doanh thu vé đã bán                      *
        *    6.   Hiển thị danh sách vé đang chờ xem                 *
        *    7.   Hiển thị doanh thu theo khung thời gian            *
        *    8.   Hiển thị doanh thu theo phim                       *
        *    9.   Hiển thị top 5 phim doanh thu cao nhất             *
        *    10.  Tìm kiếm phim theo khoảng thời gian                *
        *    11.  Danh sách vé đã bị hủy                             *
        *    999. Đổi Thời Gian Thực (TEST)                          *
        *    0.   Thoát                                              *
        **************************************************************
"""

def getPrice(loaiPhim, gioChieu):
    if timeCompare(gioChieu, PEAK_BEGIN) != False and timeCompare(PEAK_END, gioChieu) != False: #giochieu >= 18h   22h >= giochieu
        if loaiPhim == "VN":
            return 60000
        return 72000
    if loaiPhim == "VN":
        return 50000
    return 60000
def inGhe(danhSachGhe):
    n = int(len(danhSachGhe)**0.5)
    m = 2*n + 2 + 3*(n+1)
    flag = False
    for ghe in danhSachGhe:
        if ghe.trangThai == 0:
            flag = True
            break
    if not flag:
        s = """
        -------------------------------
        |   Vé đã hết mất rồi, huhu   |
        -------------------------------
        """
        print(s)
        return 0
    else:
        print(" "*((m-14)//2)+"---MÀN HÌNH---"+" "*((m-14)//2))
        print('-'*m)
        for i in range(len(danhSachGhe)):
            if i % n == 0:
                print("|   ", end="")
            if danhSachGhe[i].trangThai == 1:
                print("  ", end="   ")
            else:
                print(danhSachGhe[i].maGhe, end="   ")
            if i % n == (n-1):
                print("|")
        print('-'*m)
        return 1
def getRoomByFilmNameAndTimeAndRoomName(film_name, time_start, room_name):
    roomList = []
    for thoiGianPhongChieu in danhSachThoiGianPhongChieu:
        if thoiGianPhongChieu.phim.tenPhim == film_name and thoiGianPhongChieu.phongChieu.tenPhong == room_name and thoiGianPhongChieu.thoiGian.thoigian == time_start:
            roomList.append(thoiGianPhongChieu)
    return roomList
def getListRoomByFilmName(film_name):
    roomList = []
    for thoiGianPhongChieu in danhSachThoiGianPhongChieu:
        if thoiGianPhongChieu.phim.tenPhim == film_name:
            if timeCompare(timeDif(thoiGianPhongChieu.thoiGian.thoigian, 5), NOW): #Hiện tại < Chiếu - 5p
                roomList.append(thoiGianPhongChieu)
    return roomList

def isInteger(i):
    try:
        intI = int(i)
        return True
    except:
        return False
def timeCheck(time):
    # pattern = r"[0-2][0-9]:[0-5]{2}$"
    try:
        datetime.datetime.strptime(time, "%H:%M")
        return True
    except:
        return False
def timeAdd(time, minutes):
    timeDenta = datetime.timedelta(minutes=minutes)
    return (datetime.datetime.strptime(time, "%H:%M") + timeDenta).strftime("%H:%M")

def timeDif(time, minutes):
    timeDenta = datetime.timedelta(minutes=minutes)
    return (datetime.datetime.strptime(time, "%H:%M") - timeDenta).strftime("%H:%M")

def timeCompare(time1, time2):
    if datetime.datetime.strptime(time1, "%H:%M") == datetime.datetime.strptime(time2, "%H:%M"):
        return None
    return datetime.datetime.strptime(time1, "%H:%M") > datetime.datetime.strptime(time2, "%H:%M")
    #True: time1 > time2
    #False: time1 < time2
    #None: time1 = time2

class ThoiGian:
    def __init__(self, thoigian):
        self.thoigian = thoigian
class PhongChieu_ThoiGian:
    def __init__(self, phongChieu, thoiGian, phim):
        self.thoiGian = thoiGian
        self.phongChieu = phongChieu
        self.phim = phim
        self.gheNgoi = []
        for i in range(int(phongChieu.soGhe ** 0.5)):
            for j in range(int(phongChieu.soGhe ** 0.5)):
                self.gheNgoi.append(GheNgoi(ALPHABET[i] + NUMBER[j], 0))
class PhongChieu:
    def __init__(self, tenPhong, soGhe):
        self.tenPhong = tenPhong
        self.soGhe = soGhe
class Phim:
    def __init__(self, tenPhim, thoiLuong, loaiPhim):
        self.tenPhim = tenPhim
        self.thoiLuong = thoiLuong
        self.loaiPhim = loaiPhim
class GheNgoi:
    def __init__(self, maGhe, trangThai):
        self.maGhe = maGhe
        self.trangThai = trangThai
class Ticket:
    def __init__(self, mave, phongChieu, tenPhim, thoiGianChieu, viTriGhe, loaiPhim, giaVe):
        self.mave = mave
        self.phongChieu = phongChieu
        self.tenPhim = tenPhim
        self.thoiGianChieu = thoiGianChieu
        self.viTriGhe = viTriGhe
        self.loaiPhim = loaiPhim
        self.giaVe = giaVe
    def display(self):
        print(vars(self))
class ManageTicket:
    def printListTicket(self, tickets, status):
        x = PrettyTable(["Mã Vé", "Tên Phim", "Thời Gian Chiếu", "Phòng Chiếu", "Vị Trí Ghế", "Loại Phim", "Giá Vé", "Trạng Thái Vé"])
        for i in range(len(tickets)):
            ticket = tickets[i]
            if status[i] == 1:
                s = "Đã Bán"
            else:
                s = "Đã Hoàn Trả"
            x.add_row([ticket.mave, ticket.tenPhim, ticket.thoiGianChieu, ticket.phongChieu , ticket.viTriGhe, ticket.loaiPhim, ticket.giaVe, s])
        print(x)
    def __init__(self):
        self.tickets = []
        self.trangThaiTicket = []  #1: Mua, 0.8: Hủy Có Hoàn Tiền NN, 0.6: Huỷ có hoàn tiền VN, 0: Hủy Không Hoàn Tiền
    def getAllTickets(self):
        for ticket in self.tickets:
            ticket.display()
        print(self.trangThaiTicket)
    def banVeMoi(self, ticket):
        if isinstance(ticket, Ticket):
            self.tickets.append(ticket)
            self.trangThaiTicket.append(1)
    def huyVeDaBan(self):
        if len(self.tickets) == 0:
            print("Không có vé nào")
        else:
            flag = False
            mave = input("Nhập mã vé muốn hủy: ")
            for i in range(len(self.tickets)):
                if self.tickets[i].mave == mave and self.trangThaiTicket[i] == 1:
                    print("Thông tin vé:")
                    self.tickets[i].display()
                    print()
                    if input("Bạn có chắc chắn muốn hủy? (y/n) ").lower() == "y":
                        if timeCompare(timeDif(self.tickets[i].thoiGianChieu, 240), NOW): #thời gian chiếu - 4 tiếng > hiện tại
                            if self.tickets[i].loaiPhim == "VN":
                                self.trangThaiTicket[i] = 0.4
                            else:
                                self.trangThaiTicket[i] = 0.2
                            listRoom = getRoomByFilmNameAndTimeAndRoomName(self.tickets[i].tenPhim,
                                                                           self.tickets[i].thoiGianChieu,
                                                                           self.tickets[i].phongChieu)[0]
                            [ghe for ghe in listRoom.gheNgoi if ghe.maGhe == self.tickets[i].viTriGhe][
                                0].trangThai = 0
                            print("Hủy vé thành công")
                            break
                        else:
                            print("VÉ CHỈ ĐƯỢC HỦY TRƯỚC KHI CHIẾU 4 TIẾNG")
                    flag = True
            if not flag:
                print("Mã Vé Không Tồn Tại!!!")
    def thongKeLuongVeMoiLoai(self):
        soVeVN = 0
        soVeNN = 0
        for i in range(len(self.tickets)):
            if self.tickets[i].loaiPhim == "VN":
                soVeVN += 1
            if self.tickets[i].loaiPhim == "NN":
                soVeNN += 1
        print("HÔM NAY ĐÃ BÁN ĐƯỢC:")
        x = PrettyTable(["Loại Phim", "Số Vé Đã Bán Trong Ngày"])
        x.add_row(["Phim Việt Nam", soVeVN])
        x.add_row(["Phim Nước Ngoài", soVeNN])
        print(x)
    def thongKeTheoTenPhim(self):
        tenPhim = input("Nhập Tên Phim: ").lower()
        sort = input("Kiểu sắp xếp?(Mặc định là tăng dần theo thời gian(A)). Vui lòng nhập A/D: ").upper()
        found = [phim for phim in danhSachPhim if phim.tenPhim.lower() == tenPhim]
        if len(found) == 0:
            print("Nhập Sai Tên Phim Mất Rồi!!!")
        else:
            soVe = 0
            for i in range(len(self.tickets)):
                if self.tickets[i].tenPhim.lower() == tenPhim and self.trangThaiTicket[i] == 1:
                    soVe += 1
            print(f"Hôm nay phim {found[0].tenPhim} đã bán được {soVe} vé.")
            print("Danh Sách Vé:")
            l = []
            for i in range(len(self.tickets)):
                if self.tickets[i].tenPhim.lower() == tenPhim and self.trangThaiTicket[i] == 1:
                    l.append(self.tickets[i])
            l.sort(key=lambda t: t.thoiGianChieu)
            if sort == 'D':
                l.reverse()
            for i in l:
                i.display()
    def tongDoanhThu(self):
        totalMoney = 0
        for i in range(len(self.tickets)):
            totalMoney += (self.tickets[i].giaVe * self.trangThaiTicket[i])
        print(f"Doanh Số Đến {NOW} là: {totalMoney}")
        print("Danh Sách Vé")
        self.printListTicket(self.tickets, self.trangThaiTicket)
    def danhSachVeDangCho(self):
        l = []
        s = []
        t = []
        for i in range(len(self.tickets)):
            if timeCompare(self.tickets[i].thoiGianChieu, NOW):
                l.append([self.trangThaiTicket[i], self.tickets[i]])
        l.sort(key=lambda t:t[1].thoiGianChieu)
        for i in l:
            s.append(i[0])
            t.append(i[1])
        self.printListTicket(t, s)
    def doanhThuTheoKhungThoiGianChieu(self):
        dict = {}
        for i in danhSachThoiGian:
            dict[i.thoigian] = 0
        for i in range(len(self.tickets)):
            dict[self.tickets[i].thoiGianChieu] += (self.tickets[i].giaVe * self.trangThaiTicket[i])
        t = PrettyTable(["Thời Gian Chiếu", "Doanh Thu"])
        for thoiGian in dict:
            if(dict[thoiGian] > 0):
                t.add_row([thoiGian, dict[thoiGian]])
        print(t)
    def doanhThuTheoPhim(self):
        dict = {}
        for i in danhSachPhim:
            dict[i.tenPhim] = 0
        for i in range(len(self.tickets)):
            dict[self.tickets[i].tenPhim] += (self.tickets[i].giaVe * self.trangThaiTicket[i])
        t = PrettyTable(["Tên Phim", "Doanh Thu"])
        for phim in dict:
            if (dict[phim] > 0):
                t.add_row([phim, dict[phim]])
        print(t)
    def topPhim(self, soPhim, choice):
        dic = {}
        for i in danhSachPhim:
            dic[i.tenPhim] = 0
        for i in range(len(self.tickets)):
            dic[self.tickets[i].tenPhim] += (self.tickets[i].giaVe * self.trangThaiTicket[i])
        t = PrettyTable(["Tên Phim", "Doanh Thu"])
        tupleSorted = sorted(dic.items(), key=lambda x: x[1])
        sortedDict = dict((x, y) for x, y in tupleSorted)
        if choice == 0:
            sortedDict = dict(reversed(list(sortedDict.items())))
        i = 0

        for phim in sortedDict:
            if i == soPhim:
                break
            t.add_row([phim, sortedDict[phim]])
            i += 1
        print(t)
    def searchByTime(self):
        flag = 1
        l = []
        start = input("Phim bắt đầu từ (mặc định là 08:00 (Định dạng hh:mm)): ")
        end = input("đến (mặc định là 23:59 (Định dạng hh:mm)): ")
        if start == "":
            start = NOW
        if end == "":
            end = "23:59"
        if not timeCheck(start) or not timeCheck(end) or timeCompare(start, end):
            flag = 0
        if flag == 0:
            print("Thời gian không hợp lệ")
        else:
            for i in danhSachThoiGianPhongChieu:
                if not timeCompare(start, i.thoiGian.thoigian) and not timeCompare(i.thoiGian.thoigian, end):
                    if len([x for x in i.gheNgoi if x.trangThai == 0]) != 0:
                        l.append(i)
            if len(l) == 0:
                print("Không Có Phim Nào Trong Khoảng Thời Gian Này")
            else:
                l.sort(key=lambda x: x.thoiGian.thoigian)
                x = PrettyTable(["Tên Phim", "Xuất Chiếu", "Phòng Chiếu", "Số Ghế Còn Trống/Tổng Số Ghế"])
                for i in l:
                    x.add_row([i.phim.tenPhim, i.thoiGian.thoigian, i.phongChieu.tenPhong, f"{len([z for z in i.gheNgoi if z.trangThai == 0])}/{len([z for z in i.gheNgoi])}"])
                print(x)
    def danhSachVeDaHuy(self):
        l = []
        for i in range(len(self.tickets)):
            if self.trangThaiTicket[i] != 1:
                l.append(self.tickets[i])
        if len(l) == 0:
            s = """
                    ********************************************
                    *   Tuyệt, hôm nay chưa có vé nào bị hủy   *
                    ********************************************
            """
            print(s)
        else:
            self.printListTicket(l, [0]*len(l))
# print(isinstance(obj, Ticket))
danhSachPhim = [Phim("Mai", 131, "VN"),
                Phim("Nhà Bà Nữ", 145, "VN"),
                Phim("Bố Già", 153, "VN"),
                Phim("Lật Mặt 6", 120, "VN"),
                Phim("Lật Mặt 7", 127, "VN"),
                Phim("Transformer", 144, "NN"),
                Phim("Kungfu Panda 4", 115, "NN"),
                Phim("Marvel: Sieu Anh Hung Thai Dang", 110,"NN")]
danhSachThoiGian = [ThoiGian("08:00"),
                    ThoiGian("10:00"),
                    ThoiGian("11:30"),
                    ThoiGian("13:00"),
                    ThoiGian("15:30"),
                    ThoiGian("17:50"),
                    ThoiGian("19:00"),
                    ThoiGian("20:30")]
danhSachPhongChieu = [PhongChieu("Phòng 1", 36),
                      PhongChieu("Phòng 2", 49),
                      PhongChieu("Phòng 3", 49),
                      PhongChieu("Phòng 4", 64)]
danhSachThoiGianPhongChieu = [PhongChieu_ThoiGian(danhSachPhongChieu[0], danhSachThoiGian[0], danhSachPhim[0]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[0], danhSachThoiGian[2], danhSachPhim[0]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[0], danhSachThoiGian[4], danhSachPhim[7]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[0], danhSachThoiGian[5], danhSachPhim[3]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[0], danhSachThoiGian[7], danhSachPhim[5]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[1], danhSachThoiGian[0], danhSachPhim[3]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[1], danhSachThoiGian[2], danhSachPhim[0]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[1], danhSachThoiGian[4], danhSachPhim[0]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[1], danhSachThoiGian[6], danhSachPhim[6]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[2], danhSachThoiGian[0], danhSachPhim[7]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[2], danhSachThoiGian[1], danhSachPhim[0]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[2], danhSachThoiGian[3], danhSachPhim[4]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[2], danhSachThoiGian[4], danhSachPhim[2]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[2], danhSachThoiGian[6], danhSachPhim[4]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[3], danhSachThoiGian[0], danhSachPhim[6]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[3], danhSachThoiGian[2], danhSachPhim[1]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[3], danhSachThoiGian[5], danhSachPhim[5]),
                              PhongChieu_ThoiGian(danhSachPhongChieu[3], danhSachThoiGian[7], danhSachPhim[7])]
"""
    Phòng 1     08:00: Mai ->       10:11
    Phòng 1     11:30: Mai ->       13:41
    Phòng 1     15:30: Marvel       17:20
    Phòng 1     17:50: Lật Mặt 6    19:50
    Phòng 1     20:20: Transformer  22:44
    Phòng 2     08:00: Lật Mặt 6 -> 10:00
    Phòng 2     11:30: Mai ->       13:41
    Phòng 2     15:30: Mai          17:41
    Phòng 2     19:00: Kungfu       20:55
    Phòng 3     08:00: Marvel       09:50
    Phòng 3     10:00: Mai ->       12:11
    Phòng 3     13:00: Lật Mặt 7 -> 15:07
    Phòng 3     15:30: Bố Già       18:03
    Phòng 3     19:00: Lật Mặt 7    21:07
    Phòng 4     11:30: Kungfu       13:25
    Phòng 4     08:00: Nhà Bà Nữ -> 10:25
    Phòng 4     17:50: Transformer  20:14
    Phòng 4     20:30: Marvel       22:20
"""
manageTicket = ManageTicket()
select = 1
while select != 0:
    print("\033[96m {}\033[00m".format(MENU))
    select = input("Nhập lựa chọn của bạn: ")
    if select == "0":
        break
    elif select == "1":
        os.system("cls")
        t = PrettyTable(["STT", "Tên Phim", "Loại Phim"])
        for i in range(len(danhSachPhim)):
            t.add_row([i + 1, danhSachPhim[i].tenPhim, danhSachPhim[i].loaiPhim])
        print(t)
        p = input("Nhập STT phim: ")
        os.system("cls")
        if not isInteger(p):
            print("Lựa Chọn Không Phải Là Số Nguyên!!!")
        else:
            if int(p) in range(1, len(danhSachPhim) + 1):
                rooms = getListRoomByFilmName(danhSachPhim[int(p) - 1].tenPhim)
                print("SUẤT CHIẾU CỦA PHIM", danhSachPhim[int(p) - 1].tenPhim)
                if len(rooms) == 0:
                    print("Oops!! Không Còn Suất Chiếu Nào Trong Ngày")
                else:
                    r = PrettyTable(["STT", "Thời Gian Bắt Đầu", "Phòng Chiếu", "Số Ghế Trống/Tổng Số Ghế"])
                    for i in range(len(rooms)):
                        r.add_row([i + 1, rooms[i].thoiGian.thoigian, rooms[i].phongChieu.tenPhong, f"{len([tdf for tdf in rooms[i].gheNgoi if tdf.trangThai == 0])}/{len([tdf for tdf in rooms[i].gheNgoi])}"])
                    print(r)
                    sc = input("Nhập Suất Chiếu Bạn Muốn: ")
                    if isInteger(sc) and int(sc) in range(1, len(rooms) + 1):
                        print("\n")
                        if inGhe(rooms[int(sc) - 1].gheNgoi) == 1: #Chưa có check
                            choNgoi = input("Nhập Chỗ Ngồi: ").upper()
                            checkGhe = False
                            #Hàm
                            for gh in rooms[int(sc) - 1].gheNgoi:
                                if choNgoi == gh.maGhe and gh.trangThai == 0:
                                    gh.trangThai = 1
                                    checkGhe = True
                                    break
                            ###
                            if(checkGhe):
                                ticket = Ticket(str(uuid.uuid4())[0:6],
                                                rooms[int(sc) - 1].phongChieu.tenPhong,
                                                danhSachPhim[int(p) - 1].tenPhim,
                                                rooms[int(sc) - 1].thoiGian.thoigian,
                                                choNgoi,
                                                danhSachPhim[int(p) - 1].loaiPhim,
                                                getPrice(danhSachPhim[int(p) - 1].loaiPhim, rooms[int(sc) - 1].thoiGian.thoigian)
                                                )
                                manageTicket.banVeMoi(ticket)
                            ###
                            else:
                                print("Ghế không tồn tại")
                            manageTicket.getAllTickets()
                    elif not isInteger(sc):
                        print("Suất chiếu là một số nguyên")
                    else:
                        print("Suất chiếu không tồn tại")
            else:
                print("Lựa Chọn Không Tồn Tại!!!")
    elif select == "2":
        os.system("cls")
        manageTicket.huyVeDaBan()
        manageTicket.getAllTickets()
    elif select == "3":
        os.system("cls")
        manageTicket.thongKeLuongVeMoiLoai()
    elif select == "4":
        os.system("cls")
        manageTicket.thongKeTheoTenPhim()
    elif select == "5":
        os.system("cls")
        manageTicket.tongDoanhThu()
    elif select == "6":
        os.system("cls")
        manageTicket.danhSachVeDangCho()
    elif select == "7":
        os.system("cls")
        manageTicket.doanhThuTheoKhungThoiGianChieu()
    elif select == "8":
        os.system("cls")
        manageTicket.doanhThuTheoPhim()
    elif select == "9":
        os.system("cls")
        manageTicket.topPhim(5, 0) #0: Giam dan, 1:Tang dan

    elif select == "10":
        os.system("cls")
        manageTicket.searchByTime()
    elif select == "11":
        os.system("cls")
        manageTicket.danhSachVeDaHuy()
    elif select == "999":
        os.system("cls")
        t = input("Nhập thời gian mong muốn để test (định dạng HH:MM) ")
        if timeCheck(t):
            NOW = t
    else:
        print("Lựa Chọn Không Tồn Tại, Vui Lòng Nhập Lại!")
