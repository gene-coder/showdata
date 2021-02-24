import pymysql
import cx_Oracle

def run_mysql(database, mysql2):
    if database['get_datatype']=='MYSQL':
        db = pymysql.connect(host=database['get_dataip'], port=int(database['get_dataport']),user=database['get_datausr'],db=database['get_database'], passwd=database['get_datapwd'], charset='utf8')
        cursor = db.cursor()
        cursor.execute(mysql2)
        db.commit()
        data = cursor.fetchall()
        db.close()
        return data
    elif database['get_datatype']=='ORACLE':
        # print(database)
        mysql2=mysql2.strip(';')
        oracle_sid='{}:{}/{}'.format(database['get_dataip'],database['get_dataport'],database['get_database'])
        # print(oracle_sid)
        conn=cx_Oracle.connect(database['get_datausr'],database['get_datapwd'],oracle_sid,encoding='UTF-8')
        cursor=conn.cursor()
        cursor.execute(mysql2)
        data = cursor.fetchall()
        conn.close()
        return data
    else:
        pass


if __name__ == "__main__":
    database = {"get_dataid": "常用", "get_datatype": "MYSQL", "get_dataip": "192.168.80.62",
                "get_dataport": "3306", "get_datausr": "python", "get_datapwd": "comeon", "get_datadesc": "ces "}
    aa = 'use python;'
    print(run_mysql(database,aa))
