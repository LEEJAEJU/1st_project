from flask import Flask, render_template, request, redirect, url_for, Response
import pymysql
from werkzeug.utils import secure_filename
import boto3


def sever_connect_insert(sql, recode):
    try:
        global db
        db = pymysql.connect(
            host="free-test.cmmknlcj0s9v.ap-northeast-2.rds.amazonaws.com",
            port=3306,
            user="admin",
            passwd="01041107029",
            db="securevest",
            charset="utf8",
        )
        cursor = db.cursor()
        cursor.execute(sql, recode)
        return cursor
    except:
        return 404


def sever_connect2(sql):
    try:
        global db
        db = pymysql.connect(
            host="free-test.cmmknlcj0s9v.ap-northeast-2.rds.amazonaws.com",
            port=3306,
            user="admin",
            passwd="01041107029",
            db="securevest",
            charset="utf8",
        )
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor
    except:
        return 404


app = Flask(__name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id="AKIA3YT2IIE7I5ZWSM7H",
    aws_secret_access_key="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",
)
bucket_name = "project-s3-data"


@app.route("/")  # 로그인으로 이동
def start():
    return redirect(url_for("login_page"))


@app.route("/login", methods=["GET", "POST"])  # 로그인
def login_page():
    if request.method == "POST":
        if request.form["sel"] == "new":
            return redirect(url_for("new_worker_registration"))  # 회원가입
        else:
            ID = request.form["ID"]
            Passwd = request.form["Passwd"]
            login_sql = f'select userid, passwd, admin, username from securevest.worker where userid Like "{ID}";'
            result = sever_connect2(login_sql)
            for log in result:
                if log[1] == Passwd:
                    if log[2] == "O":  # 관리자인지 확인
                        name = log[3] + "(관리자)"
                        return redirect(url_for("meun_select", name=name, admin="O"))
                    else:
                        name = log[3]  # 관리자가 아닐경우
                        return redirect(url_for("meun_select", name=name, admin="X"))
                else:
                    return render_template("index.html")

    return render_template("index.html")


@app.route("/login/new", methods=["GET", "POST"])  # 회원가입
def new_worker_registration():
    if request.method == "POST":
        if request.form["sel"] == "back":
            return redirect(url_for("login_page"))
        else:
            name = request.form["name"]
            id = request.form["id"]
            pw = request.form["password"]
            pnum = request.form["num"]
            if name == "" or id == "" or pw == "" or pnum == "":
                return render_template("new.html", message="입력되지 않은 값이 존재합니다.")
            duplicate_check = "SELECT userid FROM securevest.worker"  # 아이디 중복 검사
            result = sever_connect2(duplicate_check)  # 중복 검사용
            for bd_id in result:
                if bd_id[0] == id:
                    return render_template("new.html", message="아이디 중복 입니다.")
            qurry_m = "INSERT INTO securevest.worker (username, userid, passwd, phone) VALUES (%s, %s, %s, %s);"
            recode = (name, id, pw, pnum)
            print(qurry_m, recode)
            cursor = sever_connect_insert(qurry_m, recode)
            db.commit()
            return redirect(url_for("login_page"))

    return render_template("new.html")


@app.route("/meun_select", methods=["GET", "POST"])  # 메뉴선택
def meun_select():
    name = request.args.get("name")
    admin = request.args.get("admin")
    global reset_check
    if request.method == "POST":
        print(request.form["sel"])
        if request.form["sel"] == "data":
            reset_check = 0
            return redirect(url_for("DB_data_view", name=name, admin=admin))  # 데이터보기
        elif request.form["sel"] == "video_view":
            return redirect(
                url_for("video_list_view", name=name, admin=admin)
            )  # 동영상 보기
        else:
            return redirect(url_for("login_page"))  # 처음 페이지로 돌아감

    return render_template("select.html", name=name)


def data_check(want_data):  # 어떤 데이터를 검색할지 확인할 때 사용
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


radio_check = ""  # 값 확인용 전역
real_search_list = []  # 데이터 처리용 리스트
reset_check = 0  # 데이터 초기화 체크용


@app.route("/meun_select/data_view", methods=["GET", "POST"])  # 데이터 조회
def DB_data_view():
    name = request.args.get("name")
    admin = request.args.get("admin")
    global real_search_list
    global radio_check
    global reset_check
    if reset_check == 0:
        real_search_list.clear()
    data_list = [[], [], [], [], [], [], []]
    view_table = ["0", "0", "0", "0", "0", "0", "0", "0"]
    if request.method == "POST":
        Search_type = request.form["set"]  # 검색종류
        try:
            sel_check = request.form["one_value"]
        except:
            sel_check = "0"
        try:
            Search_Point = request.form["option"]
            assert radio_check == Search_type, "list_reseting"
        except:
            if Search_type == "day":
                radio_check = Search_type
                real_search_list = day_list_make(admin)
                reset_check = 1

            else:
                radio_check = Search_type
                real_search_list = num_list_make(admin)
                reset_check = 1

            return render_template(
                "data_see.html",
                name=name,
                valuecheck=view_table,
                options=real_search_list,
                selected_value=Search_type,
                selected_value2=sel_check,
            )
        want_data = request.form["one_value"]
        view_table[int(want_data)] = "1"  # 해당하는 표 작동용
        if want_data != "0":  # 특정 데이터만 조회할 때
            data_list[int(want_data) - 1] = data_check(want_data)
        else:  # 모든 데이터 조회할 떄
            data_list = data_check(want_data)
        for b in range(0, 7):
            if data_list[b] == 404:  # bd에 연결 되지 않았을 경우 에러코드
                return render_template("data_see.html", name=name, valuecheck_404="404")

        data_list = data_classfiy(data_list, Search_type, Search_Point, admin)  # 데이터 분류

        return render_template(
            "data_see.html",
            name=name,
            valuecheck=view_table,
            options=real_search_list,
            list=data_list,
            selected_value=Search_type,
            selected_value2=sel_check,
        )

    return render_template(
        "data_see.html",
        name=name,
        valuecheck=view_table,
        options=real_search_list,
        selected_value="day",
        selected_value2="0",
    )


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


search_video_day = []  # 데이터 처리용 리스트


@app.route("/meun_select/video_view_and_download", methods=["GET", "POST"])  # 동영상 선택용
def video_list_view():
    name = request.args.get("name")
    admin = request.args.get("admin")
    global search_video_day

    all_videos = []
    div_videos = []
    if admin == "O":
        response = s3.list_objects(Bucket=bucket_name)
        objects = response["Contents"]
        for obj in objects:
            if obj["Key"].endswith(".mp4"):
                all_videos.append(obj["Key"])

    if request.method == "POST":
        sel = request.form["sel"]
        if request.form["sel"] == "back":
            return redirect(url_for("meun_select", name=name, admin=admin))
        try:
            Search_Point = request.form["option"]
        except:
            for b in all_videos:
                search_video_day.append(b[0:10])

            search_video_day = set(search_video_day)
            search_video_day = list(search_video_day)

            search_video_day.insert(0, "전체")

            return render_template(
                "video_list_view.html", name=name, admin=admin, options=search_video_day
            )
        if Search_Point == "전체":
            div_videos = all_videos
        else:
            for a in range(0, len(all_videos)):
                if Search_Point in all_videos[a]:
                    div_videos.append(all_videos[a])

        return render_template(
            "video_list_view.html",
            name=name,
            admin=admin,
            options=search_video_day,
            videos=div_videos,
        )

    return render_template("video_list_view.html", name=name, admin=admin)


@app.route("/video_view/<value>", methods=["GET", "POST"])  # 동영상 시청용
def video_view(value):
    name = request.args.get("name")
    admin = request.args.get("admin")
    if request.method == "POST":
        print(request.form["sel"])
        if request.form["sel"] == "back":
            return redirect(url_for("video_list_view", name=name, admin=admin))
        else:
            return redirect(url_for("video_download", key=value))
    return render_template("video_streaming.html", key=value)


@app.route("/stream/<key>")  # 동영상 시청용
def stream(key):
    file_obj = s3.get_object(Bucket=bucket_name, Key=key)
    file_size = file_obj["ContentLength"]
    data = file_obj["Body"]
    headers = {"Content-Disposition": "attachment; filename={}".format(key)}
    return Response(
        data, headers=headers, content_type="video/mp4", direct_passthrough=True
    )


@app.route("/video_download/<key>")  # 비디오 다운로드 용
def video_download(key):
    file_obj = s3.get_object(Bucket=bucket_name, Key=key)
    file_size = file_obj["ContentLength"]
    data = file_obj["Body"]
    headers = {"Content-Disposition": "attachment; filename={}".format(key)}
    return Response(
        data, headers=headers, content_type="video/mp4", direct_passthrough=True
    )


@app.route("/insert/Flame", methods=["POST"])
def flame_data_insert_and_save():
    fire_post = ""
    if request.method == "POST":
        fire_post = request.get_json(" ")
        data_check = fire_post.get("data")
        vest_num = data_check.get("vest")
        fire = data_check.get("Fire")
        FlameTime = data_check.get("FlameTime")
        qurry_m = "INSERT INTO securevest.Flame (vest_num, Fire, FlameTime) VALUES (%s, %s, %s);"
        recode = (vest_num, fire, FlameTime)
        cursor = sever_connect_insert(qurry_m, recode)
        db.commit()

    else:
        test_post = "not data"

    return "aa"


@app.route("/insert/Buzzer", methods=["POST"])
def buzzer_data_insert_and_save():
    buzzer_post = ""
    if request.method == "POST":
        buzzer_post = request.get_json(" ")
        data_check = buzzer_post.get("data")
        vest_num = data_check.get("vest")
        buz = data_check.get("Buz")
        BuzTime = data_check.get("BuzTime")
        reason = data_check.get("Reason")
        recode = (vest_num, buz, reason, BuzTime)
        qurry_m = "INSERT INTO securevest.Buzzer (vest_num, Buz, BuzReason, BuzTime) VALUES (%s, %s, %s, %s);"
        cursor = sever_connect_insert(qurry_m, recode)
        db.commit()

    else:
        test_post = "not data"

    return "aa"


@app.route("/insert/Gas", methods=["POST"])
def CO_gas_data_insert_and_save():
    gas_post = ""
    if request.method == "POST":
        gas_post = request.get_json(" ")
        data_check = gas_post.get("data")
        vest_num = data_check.get("vest")
        gas = data_check.get("Gas")
        GasTime = data_check.get("GasTime")
        recode = (vest_num, gas, GasTime)
        qurry_m = "INSERT INTO securevest.Gassensor (vest_num, Gas, GasTime) VALUES (%s, %s, %s);"
        cursor = sever_connect_insert(qurry_m, recode)
        db.commit()

    else:
        test_post = "not data"

    return "aa"


@app.route("/insert/Led", methods=["POST"])
def led_on_off_data_insert_and_save():
    led_post = ""
    if request.method == "POST":
        led_post = request.get_json(" ")
        data_check = led_post.get("data")
        vest_num = data_check.get("vest")
        active = data_check.get("Active")
        LedTime = data_check.get("LedTime")
        recode = (vest_num, active, LedTime)
        qurry_m = (
            "INSERT INTO securevest.Led (vest_num, OnOff, LedTime) VALUES (%s, %s, %s);"
        )
        cursor = sever_connect_insert(qurry_m, recode)
        db.commit()

    else:
        test_post = "not data"

    return "aa"


@app.route("/insert/Light", methods=["POST"])
def light_on_off_data_insert_and_save():
    light_post = ""
    if request.method == "POST":
        light_post = request.get_json(" ")
        data_check = light_post.get("data")
        vest_num = data_check.get("vest")
        active = data_check.get("Active")
        LightTime = data_check.get("LightTime")
        recode = (vest_num, active, LightTime)
        qurry_m = "INSERT INTO securevest.LightSensor (vest_num, Light, LightTime) VALUES (%s, %s, %s);"
        cursor = sever_connect_insert(qurry_m, recode)
        db.commit()

    else:
        test_post = "not data"

    return "aa"


@app.route("/insert/TempHm", methods=["POST"])
def TempHm_data_insert_and_save():
    temphm_post = ""
    if request.method == "POST":
        temphm_post = request.get_json(" ")
        data_check = temphm_post.get("data")
        vest_num = data_check.get("vest")
        Temp = data_check.get("Temp")
        Hm = data_check.get("Hm")
        TempHmTime = data_check.get("TempHmTime")
        recode = (vest_num, Temp, Hm, TempHmTime)
        qurry_m = "INSERT INTO securevest.TempHm (vest_num, Temp, Hm, TempHmTime) VALUES (%s, %s, %s, %s);"
        cursor = sever_connect_insert(qurry_m, recode)
        db.commit()

    else:
        test_post = "not data"

    return "aa"


@app.route("/insert/Visitor", methods=["POST"])
def Visitor_data_insert_and_save():
    visit_post = ""
    if request.method == "POST":
        visit_post = request.get_json(" ")
        data_check = visit_post.get("data")
        name = data_check.get("visitant")
        visit_time = data_check.get("visit_time")
        state = data_check.get("state")
        recode = (name, state, visit_time)
        qurry_m = "INSERT INTO securevest.visitor (visitant, state, visit_time) VALUES (%s, %s, %s);"
        cursor = sever_connect_insert(qurry_m, recode)
        db.commit()

    else:
        test_post = "not data"

    return "aa"


if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0", port=8080)
