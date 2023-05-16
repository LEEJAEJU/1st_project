from rds_s3_connect import sever_connect2, sever_connect_insert, db
from flask import request


def login_make(ID:str, Passwd:str):  # 로그인 데이터 확인
    """_summary_

    Args:
        ID (str): HTTP_Login_Entered_Id \n
        Passwd (str): HTTP_Login_Entered_Passwd

    Returns:
        log_data (list): User_name_and_admin
    """
    login_sql = f'select userid, passwd, admin, username from securevest.worker where userid Like "{ID}";'
    result = sever_connect2(login_sql)
    log_data = []
    for log in result:
        if log[1] == Passwd:
            log_data.append("O")
            if log[2] == "O":  # 관리자인지 확인
                name = log[3] + "(관리자)"
                log_data.append(name)
                log_data.append("O")
            else:
                log_data.append(log[3])  # 관리자가 아닐경우
                log_data.append("X")

    log_data.append("X")

    return log_data


def duplicate_check_fuc(id:str):  # 중복검사용
    """_summary_

    Args:
        id (str): HTTP_join_the_membership_Id

    Returns:
        duplicate (str): Duplicate_or_not
    """
    duplicate_check = "SELECT userid FROM securevest.worker"  # 아이디 중복 검사
    result = sever_connect2(duplicate_check)  # 중복 검사용
    for bd_id in result:
        if bd_id[0] == id:
            return "duplicate"


def new_login_data_insert(name:str, id:str, pw:str, pnum:str):  # 새로운 회원 데이터 저장용
    """_summary_

    Args:
        name (srt): User_name
        id (str): User_Id
        pw (str): User_Passwd
        pnum (str): User_vest_num
    """
    qurry_m = "INSERT INTO securevest.worker (username, userid, passwd, phone) VALUES (%s, %s, %s, %s);"
    recode = (name, id, pw, pnum)
    sever_connect_insert(qurry_m, recode)


def name_admin_move() -> tuple[str, str]:
    """_summary_

    Returns:
        name (str): User_name \n
        admin (str): admin_existence_and_nonexistence
    """
    name = request.args.get("name")
    admin = request.args.get("admin")
    return name, admin
