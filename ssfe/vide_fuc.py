from flask import request
from rds_s3_connect import s3

search_video_day = []  # 데이터 처리용 리스트


def all_video_list(admin):
    test_videos = []
    if admin == "O":
        test_videos = s3.video_list_make()
    return test_videos


def video_time_list(all_videos):
    global search_video_day
    try:
        Search_Point = request.form["option"]
        except_end = 0
    except:  # 처음 동영상 시간 값 추출
        search_video_day.clear()
        for b in all_videos:
            search_video_day.append(b[0:10])

            search_video_day = set(search_video_day)
            search_video_day = list(search_video_day)

        search_video_day.insert(0, "전체")
        except_end = 1
        Search_Point = None
    return search_video_day, Search_Point, except_end


def video_list_classfiy(all_videos, Search_Point):
    div_videos = []
    if Search_Point == "전체":
        div_videos = all_videos
    else:
        for a in range(0, len(all_videos)):
            if Search_Point in all_videos[a]:
                div_videos.append(all_videos[a])

    return div_videos


def video_stream_download_fuc(key):
    data, headers = s3.stream_download_fuc(key)
    return data, headers
