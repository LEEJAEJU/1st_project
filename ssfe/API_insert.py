from flask import request
from rds_s3_connect import sever_connect_insert, db


def insert_check(num, vest, s_type, time):
    post_data = request.get_json(" ")
    data_check = post_data.get("data")
    qurry_sum = {
        1: "INSERT INTO securevest.Flame (vest_num, Fire, FlameTime) VALUES (%s, %s, %s);",
        2: "INSERT INTO securevest.Gassensor (vest_num, Gas, GasTime) VALUES (%s, %s, %s);",
        3: "INSERT INTO securevest.Led (vest_num, OnOff, LedTime) VALUES (%s, %s, %s);",
        4: "INSERT INTO securevest.visitor (visitant, state, visit_time) VALUES (%s, %s, %s);",
        5: "INSERT INTO securevest.LightSensor (vest_num, Light, LightTime) VALUES (%s, %s, %s);",
    }
    vest_num, ss_type, active_time = insert_date_classify(
        data_check, vest, s_type, time
    )
    recode = (vest_num, ss_type, active_time)
    cour = sever_connect_insert(qurry_sum[num], recode)
    return "data_insert_complete"


def insert_date_classify(data_check, vest, s_type, time):
    vest_num = data_check.get(vest)
    ss_type = data_check.get(s_type)
    active_time = data_check.get(time)
    return vest_num, ss_type, active_time


def insert_check2(num, vest, s_type, reason, time):
    post_data = request.get_json(" ")
    data_check = post_data.get("data")
    qurry_sum = {
        6: "INSERT INTO securevest.Buzzer (vest_num, Buz, BuzReason, BuzTime) VALUES (%s, %s, %s, %s);",
        7: "INSERT INTO securevest.TempHm (vest_num, Temp, Hm, TempHmTime) VALUES (%s, %s, %s, %s);",
    }
    vest_num, ss_type, reason, active_time = insert_date_classify2(
        data_check, vest, s_type, reason, time
    )

    recode = (vest_num, ss_type, reason, active_time)
    cour = sever_connect_insert(qurry_sum[num], recode)
    return "data_insert_complete"


def insert_date_classify2(data_check, vest, s_type, reason, time):
    vest_num = data_check.get(vest)
    ss_type = data_check.get(s_type)
    reason = data_check.get(reason)
    active_time = data_check.get(time)
    return vest_num, ss_type, reason, active_time
