from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    Response,
    make_response,
)
from login_join_fuc import (
    login_make,
    duplicate_check_fuc,
    new_login_data_insert,
    name_admin_move,
)
from sensor_data_fuc import post_set_data_classify_fuc
from vide_fuc import (
    all_video_list,
    video_time_list,
    video_list_classfiy,
    video_stream_download_fuc,
)

from API_insert import insert_check, insert_check2

app = Flask(__name__)


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
            log_data = login_make(ID, Passwd)
            if log_data[0] == "O":
                return redirect(
                    url_for("meun_select", name=log_data[1], admin=log_data[2])
                )

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
            if duplicate_check_fuc(id) == "duplicate":
                return render_template("new.html", message="아이디 중복 입니다.")
            new_login_data_insert(name, id, pw, pnum)
            return redirect(url_for("login_page"))

    return render_template("new.html")


@app.route("/meun_select", methods=["GET", "POST"])  # 메뉴선택
def meun_select():
    name, admin = name_admin_move()
    if request.method == "POST":
        if request.form["sel"] == "data":
            return redirect(url_for("DB_data_view", name=name, admin=admin))  # 데이터보기
        elif request.form["sel"] == "video_view":
            return redirect(
                url_for("video_list_view", name=name, admin=admin)
            )  # 동영상 보기
        else:
            return redirect(url_for("login_page"))  # 처음 페이지로 돌아감

    return render_template("select.html", name=name)


@app.route("/meun_select/data_view", methods=["GET", "POST"])  # 데이터 조회
def DB_data_view():
    name, admin = name_admin_move()
    (
        view_table,
        real_search_list,
        data_list,
        Search_type,
        sel_check,
        except_end,
    ) = post_set_data_classify_fuc(admin)
    if except_end == 2:
        return render_template("data_see.html", name=name, valuecheck_404="404")
    else:
        return render_template(
            "data_see.html",
            name=name,
            valuecheck=view_table,
            options=real_search_list,
            list=data_list,
            selected_value=Search_type,
            selected_value2=sel_check,
        )


@app.route("/meun_select/video_view_and_download", methods=["GET", "POST"])  # 동영상 선택용
def video_list_view():
    name, admin = name_admin_move()
    all_videos = all_video_list(admin)

    if request.method == "POST":
        # sel = request.form["sel"]
        if request.form["sel"] == "back":
            return redirect(url_for("meun_select", name=name, admin=admin))
        search_video_day, Search_Point, except_end = video_time_list(all_videos)
        if except_end == 1:
            return render_template(
                "video_list_view.html", name=name, admin=admin, options=search_video_day
            )
        else:
            div_videos = video_list_classfiy(all_videos, Search_Point)

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
    name, admin = name_admin_move()
    if request.method == "POST":
        if request.form["sel"] == "back":
            return redirect(url_for("video_list_view", name=name, admin=admin))
        else:
            return redirect(url_for("video_download", key=value))
    return render_template("video_streaming.html", key=value)


@app.route("/stream/<key>")  # 동영상 시청용
def stream(key):
    data, headers = video_stream_download_fuc(key)
    return Response(
        data, headers=headers, content_type="video/mp4", direct_passthrough=True
    )


@app.route("/video_download/<key>")  # 비디오 다운로드 용
def video_download(key):
    data, headers = video_stream_download_fuc(key)
    return Response(
        data, headers=headers, content_type="video/mp4", direct_passthrough=True
    )


@app.route("/insert/Flame", methods=["POST"])
def flame_data_insert_and_save():
    if request.method == "POST":
        num = 1
        system_message = insert_check(num, "vest", "Fire", "FlameTime")

    else:
        system_message = "insert_error"

    response = make_response("값을 전달받았습니다.", 200)
    return response


@app.route("/insert/Gas", methods=["POST"])
def CO_gas_data_insert_and_save():
    if request.method == "POST":
        num = 2
        system_message = insert_check(num, "vest", "Gas", "GasTime")

    else:
        system_message = "insert_error"

    response = make_response("값을 전달받았습니다.", 200)  # 상대한테 값 보내기
    return response


@app.route("/insert/Led", methods=["POST"])
def led_on_off_data_insert_and_save():
    if request.method == "POST":
        num = 3
        system_message = insert_check(num, "vest", "OnOff", "LedTime")

    else:
        system_message = "insert_error"

    response = make_response("값을 전달받았습니다.", 200)  # 상대한테 값 보내기
    return response


@app.route("/insert/Visitor", methods=["POST"])
def Visitor_data_insert_and_save():
    if request.method == "POST":
        num = 4
        system_message = insert_check(num, "visitant", "state", "visit_time")

    else:
        system_message = "insert_error"

    response = make_response("값을 전달받았습니다.", 200)
    return response


@app.route("/insert/Light", methods=["POST"])
def light_on_off_data_insert_and_save():
    if request.method == "POST":
        num = 5
        system_message = insert_check(num, "vest", "Light", "LightTime")

    else:
        system_message = "insert_error"

    response = make_response("값을 전달받았습니다.", 200)
    return response


@app.route("/insert/Buzzer", methods=["POST"])
def buzzer_data_insert_and_save():
    if request.method == "POST":
        num = 6
        system_message = insert_check2(num, "vest", "Buz", "BuzReason", "BuzTime")

    else:
        system_message = "insert_error"

    response = make_response("값을 전달받았습니다.", 200)
    return response


@app.route("/insert/TempHm", methods=["POST"])
def TempHm_data_insert_and_save():
    if request.method == "POST":
        num = 7
        system_message = insert_check2(num, "vest", "Temp", "Hm", "TempHmTime")

    else:
        system_message = "insert_error"

    response = make_response("값을 전달받았습니다.", 200)
    return response

@app.route("/insert/test", methods=["POST"])
def test():
    post_data = request.get_json(" ")
    print(post_data)
    response = make_response("값을 전달받았습니다.", 200)
    return response


if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0", port=8080)