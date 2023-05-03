from rds_s3_connect import sever_connect2
from flask import request

radio_check = ""  # 값 확인용 전역
real_search_list = []  # 데이터 처리용 리스트
reset_check = 0  # 데이터 초기화 체크용


def data_load(data_value):  # 필요한 데이터 불러오기
    BD_data_one = []
    data_list_one = []
    all_data_list = []
    table_select = {
        1: "SELECT * FROM securevest.Buzzer",
        2: "SELECT * FROM securevest.Flame",
        3: "SELECT * FROM securevest.Gassensor",
        4: "SELECT * FROM securevest.Led",
        5: "SELECT * FROM securevest.LightSensor",
        6: "SELECT * FROM securevest.TempHm",
        7: "SELECT * FROM securevest.visitor",
    }
    if data_value == 0:
        for a in range(1, 8):
            BD_data_all = []
            data_list_all = []
            BD_data_all = sever_connect2(table_select[a])
            if BD_data_all == 404:
                return 404
            else:
                for a in BD_data_all:
                    data_list_all.append(a)
            all_data_list.append(data_list_all)
        return all_data_list

    elif data_value == 1:
        BD_data_one = sever_connect2(table_select[data_value])
    elif data_value == 2:
        BD_data_one = sever_connect2(table_select[data_value])
    elif data_value == 3:
        BD_data_one = sever_connect2(table_select[data_value])
    elif data_value == 4:
        BD_data_one = sever_connect2(table_select[data_value])
    elif data_value == 5:
        BD_data_one = sever_connect2(table_select[data_value])
    elif data_value == 6:
        BD_data_one = sever_connect2(table_select[data_value])
    elif data_value == 7:
        BD_data_one = sever_connect2(table_select[data_value])

    if BD_data_one == 404:
        return 404
    else:
        for a in BD_data_one:
            data_list_one.append(a)
        return data_list_one


def data_check(want_data):  # 어떠한 센서 데이터를 검색할지 확인할 때 사용
    data_list = []
    if want_data == "0":
        data_list = data_load(0)
        return data_list
    elif want_data == "1":
        data_list = data_load(1)
        return data_list
    elif want_data == "2":
        data_list = data_load(2)
        return data_list
    elif want_data == "3":
        data_list = data_load(3)
        return data_list
    elif want_data == "4":
        data_list = data_load(4)
        return data_list
    elif want_data == "5":
        data_list = data_load(5)
        return data_list
    elif want_data == "6":
        data_list = data_load(6)
        return data_list
    else:
        data_list = data_load(7)
        return data_list


def day_list_make(admin):
    day_list = []
    table_select = {
        1: "SELECT BuzTime FROM securevest.Buzzer",
        2: "SELECT FlameTime FROM securevest.Flame",
        3: "SELECT GasTime FROM securevest.Gassensor",
        4: "SELECT LedTime FROM securevest.Led",
        5: "SELECT LightTime FROM securevest.LightSensor",
        6: "SELECT TempHmTime FROM securevest.TempHm",
        7: "SELECT visit_time FROM securevest.visitor",
    }
    for a in range(1, 8):
        time_list = sever_connect2(table_select[a])
        for b in time_list:
            day_list.append(b[0][0:10])
    day_list = set(day_list)
    day_list = sorted(day_list)
    if admin == "O":
        day_list.insert(0, "전체")

    return day_list


def num_list_make(admin):
    vest_list = []
    table_select = {
        1: "SELECT vest_num FROM securevest.Buzzer",
        2: "SELECT vest_num FROM securevest.Flame",
        3: "SELECT vest_num FROM securevest.Gassensor",
        4: "SELECT vest_num FROM securevest.Led",
        5: "SELECT vest_num FROM securevest.LightSensor",
        6: "SELECT vest_num FROM securevest.TempHm",
    }
    for a in range(1, 7):
        num_list = sever_connect2(table_select[a])
        for b in num_list:
            vest_list.append(b[0])
    vest_list = set(vest_list)
    vest_list = sorted(vest_list, key=int)
    if admin == "O":
        vest_list.insert(0, "전체")
    return vest_list


def data_classfiy(data_list, Search_type, Search_Point, admin):  # 데이터 분류
    Search_list = []
    if Search_Point == "전체":
        Search_list = data_list
    elif Search_type == "day":
        Search_list = day_search(data_list, Search_Point)
    else:
        Search_list = num_search(data_list, Search_Point)

    if admin != "O":
        Search_list[6] = []
    return Search_list


def num_search(data_list, Search_Point):  # 조끼번호 분류
    Search_list = []
    for a in range(0, len(data_list)):
        Search_list.append([])
        for b in range(0, len(data_list[a])):
            if Search_Point in data_list[a][b][1]:
                if len(Search_Point) == len(data_list[a][b][1]):
                    Search_list[a].append(data_list[a][b])
    return Search_list


def day_search(data_list, Search_Point):  # 날짜 분류
    Search_list = []
    for a in range(0, len(data_list)):
        Search_list.append([])
        for b in range(0, len(data_list[a])):
            if len(data_list[a][b]) <= 4:
                if Search_Point in data_list[a][b][3]:
                    Search_list[a].append(data_list[a][b])
            else:
                if Search_Point in data_list[a][b][4]:
                    Search_list[a].append(data_list[a][b])
    return Search_list


def Search_type_check():
    Search_type = request.form["set"]  # 검색종류
    try:
        sel_check = request.form["one_value"]
    except:
        sel_check = "0"

    return Search_type, sel_check


def Search_type_fuc(Search_type, admin, real_search_list, radio_check, reset_check):
    if Search_type == "day":
        radio_check = Search_type
        real_search_list = day_list_make(admin)
        reset_check = 1

    else:
        radio_check = Search_type
        real_search_list = num_list_make(admin)
        reset_check = 1

    return radio_check, real_search_list, reset_check


def post_set_data_classify_fuc(admin):
    global real_search_list
    global radio_check
    global reset_check
    reset_check = 0
    if reset_check == 0:
        real_search_list.clear()
    Search_type = "day"
    sel_check = "0"
    except_end = 0
    data_list = [[], [], [], [], [], [], []]
    view_table = ["0", "0", "0", "0", "0", "0", "0", "0"]
    if request.method == "POST":
        Search_type, sel_check = Search_type_check()
        try:
            Search_Point = request.form["option"]
            assert radio_check == Search_type, "list_reseting"
            radio_check, real_search_list, reset_check = Search_type_fuc(
                Search_type, admin, real_search_list, radio_check, reset_check
            )
            except_end = 0
        except:
            radio_check, real_search_list, reset_check = Search_type_fuc(
                Search_type, admin, real_search_list, radio_check, reset_check
            )
            except_end = 1
        if except_end == 0:
            data_list, except_end = sensor_data_list(view_table, except_end, data_list)
            data_list = data_classfiy(
                data_list, Search_type, Search_Point, admin
            )  # 데이터 분류

    return view_table, real_search_list, data_list, Search_type, sel_check, except_end


def sensor_data_list(view_table, except_end, data_list):
    want_data = request.form["one_value"]
    view_table[int(want_data)] = "1"  # 해당하는 표 작동용
    if want_data != "0":  # 특정 데이터만 조회할 때
        data_list[int(want_data) - 1] = data_check(want_data)
    else:  # 모든 데이터 조회할 떄
        data_list = data_check(want_data)
    for b in range(0, 7):
        if data_list[b] == 404:  # bd에 연결 되지 않았을 경우 에러코드
            except_end = 2
    return data_list, except_end
