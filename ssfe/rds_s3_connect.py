import pymysql
import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self, host, port, user, passwd, db, charset):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            charset=self.charset,
        )

    def execute(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        self.conn.commit()
        cursor.close()
        return result

    def insert_execute(self, query, args):
        cursor = self.conn.cursor()
        cursor.execute(query, args)
        self.conn.commit()
        cursor.close()
        return "complete"


class S3:
    def __init__(self, access_key_id, secret_access_key, bucket_name):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        self.bucket_name = bucket_name

    def video_list_make(self):
        all_videos = []
        response = self.s3.list_objects(Bucket=self.bucket_name)
        if "Contents" in response:
            objects = response["Contents"]
            for obj in objects:
                if obj["Key"].endswith(".mp4"):
                    all_videos.append(obj["Key"])

        print(all_videos)
        return all_videos

    def stream_download_fuc(self, key):
        file_obj = self.s3.get_object(Bucket=self.bucket_name, Key=key)
        file_size = file_obj["ContentLength"]
        data = file_obj["Body"]
        headers = {"Content-Disposition": "attachment; filename={}".format(key)}
        return data, headers

c = ""

db = Database(
    host=os.environ.get("rds_endpoint"),
    port=int(os.environ.get("rds_port")),
    user=os.environ.get("user_name"),
    passwd=os.environ.get("rds_pw"),
    db=os.environ.get("db_name"),
    charset=os.environ.get("language_setting"),
)

def sever_connect_insert(sql, recode):
    try:
        sys_mess = ""
        sys_mess = db.insert_execute(sql, recode)
        return sys_mess
    except:
        return 404


def sever_connect2(sql):
    try:
        data_list = []
        data_list = db.execute(sql)
        return data_list
    except:
        return 404


s3 = S3(
    access_key_id=os.environ.get("s3_access_key_1"),
    secret_access_key=os.environ.get("s3_access_key_2"),
    bucket_name=os.environ.get("s3_name"),
)
