import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy as sp
from sklearn.linear_model import LinearRegression


def create_db():
    conn = sqlite3.connect('firingevaluator.db')
    cur = conn.cursor()
    # cur.execute("CREATE TABLE IF NOT EXISTS personalInfo (army_no VARCHAR2(30) primary key,name VARCHAR2(100),rank VARCHAR2(30),unit VARCHAR2(30),joining_date DATE);")
    # cur.execute("CREATE TABLE IF NOT EXISTS firingInfo (army_no VARCHAR(30),firing_date DATE,grouping DOUBLE,error VARCHAR(30));")
    # cur.execute("CREATE TABLE IF NOT EXISTS performanceInfo (army_no VARCHAR(30),perf_date DATE,performance DOUBLE);")
    # cur.execute("CREATE TABLE IF NOT EXISTS evaluationInfo(army_no VARCHAR(30),eval_date DATE,no_of_firings INTEGER,interval INTEGER,season DOUBLE,svc_length DOUBLE,avg_gp DOUBLE);")
    
    # cur.execute("INSERT OR IGNORE INTO personalInfo VALUES ('1111', 'XX XXXXXX XXXX XXXX', 'Maj', 'MIST', '2011-01-01')")
    # cur.execute("INSERT OR IGNORE INTO personalInfo VALUES ('2222', 'YY YYYYYY YYYYYY', 'Maj', 'MIST', '2010-01-01')")
    # cur.execute("INSERT OR IGNORE INTO personalInfo VALUES ('3333', 'ZZZZZ ZZZZZZ ZZZ', 'Maj', 'MIST', '2010-06-01')")
    # cur.execute("INSERT OR IGNORE INTO personalInfo VALUES ('4444', 'AAAAA', 'Maj', 'MIST', '2011-01-01')")
    # cur.execute("INSERT OR IGNORE INTO personalInfo VALUES ('5555', 'BBBBB', 'Maj', 'MIST', '2010-01-01')")
    # cur.execute("INSERT OR IGNORE INTO personalInfo VALUES ('6666', 'CCCCC', 'Maj', 'MIST', '2010-06-01')")
    # cur.execute("INSERT OR IGNORE INTO personalInfo VALUES ('7777', 'DDDDD', 'Maj', 'MIST', '2010-01-01')")
    # cur.execute("INSERT OR IGNORE INTO personalInfo VALUES ('8888', 'EEEEE', 'Maj', 'MIST', '2010-06-01')")
   
#     cur.execute("INSERT OR IGNORE INTO firingInfo VALUES ('3333', '2022-02-06', '9.62', 'No Listed Error')")
#     cur.execute("INSERT OR IGNORE INTO firingInfo VALUES ('3333', '2022-02-06', '12.62', 'Bi-focal Error')")
#     cur.execute("INSERT OR IGNORE INTO firingInfo VALUES ('3333', '2022-02-06', '9.62', 'No Listed Error')")
#     cur.execute("INSERT OR IGNORE INTO firingInfo VALUES ('3333', '2022-03-20', '9.62', 'No Listed Error')")
#     cur.execute("INSERT OR IGNORE INTO firingInfo VALUES ('3333', '2022-03-20', '12.62', 'Bi-focal Error')")
#     cur.execute("INSERT OR IGNORE INTO firingInfo VALUES ('3333', '2022-03-20', '9.62', 'No Listed Error')")
#     cur.execute("INSERT OR IGNORE INTO firingInfo VALUES ('3333', '2022-03-20', '9.62', 'No Listed Error')")

#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333', '2022-01-02', '62.62')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333', '2022-02-01', '62.62')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333', '2022-02-04', '69.26')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333', '2022-02-06', '69.63')")
    
#     cur.execute("INSERT OR IGNORE INTO evaluationInfo VALUES ('3333', '2022-01-02', '2', '33', '0', '11', '9.35')")    
#     cur.execute("INSERT OR IGNORE INTO evaluationInfo VALUES ('3333', '2022-02-01', '4', '30', '0', '11', '9.33')")
#     cur.execute("INSERT OR IGNORE INTO evaluationInfo VALUES ('3333', '2022-02-04', '1', '3', '0', '11', '9.34')")
#     cur.execute("INSERT OR IGNORE INTO evaluationInfo VALUES ('3333', '2022-02-06', '1', '3', '0', '11', '9.34')")

#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2022-01-02','60.69')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-12-25','62.16')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-12-16','61.92')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-12-09','62.99')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-12-01','59.69')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-11-23','69.90')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-11-15','69.40')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-11-06','69.20')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-10-30','63.96')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-10-22','63.93')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-10-14','63.60')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-10-06','69.69')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-09-29','62.61')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-09-20','61.69')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-09-12','61.26')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-09-04','61.35')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-09-26','61.36')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-09-19','64.44')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-09-11','69.15')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-09-03','61.62')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-06-26','59.66')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-06-19','63.66')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-06-10','63.21')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-06-02','61.63')")
#     cur.execute("INSERT OR IGNORE INTO performanceInfo VALUES ('3333','2021-06-24','69.62')")

    # X_Data = cur.execute("SELECT evaluationInfo.no_of_firings, evaluationInfo.interval, evaluationInfo.season, evaluationInfo.svc_length, evaluationInfo.avg_gp FROM evaluationInfo JOIN performanceInfo WHERE evaluationInfo.army_no = performanceInfo.army_no AND evaluationInfo.eval_date = performanceInfo.perf_date AND evaluationInfo.army_no = '1111'")
    # x1 = cur.fetchall()
    # X_Data = x1
    # X = []
    # for row in X_Data:
    #     X.append(list(row))

    # Y_Data = cur.execute("SELECT performanceInfo.performance FROM evaluationInfo JOIN performanceInfo WHERE evaluationInfo.army_no = performanceInfo.army_no AND evaluationInfo.eval_date = performanceInfo.perf_date AND evaluationInfo.army_no = '1111'")
    # y1 = cur.fetchall()
    # Y_Data = y1
    # Y = []
    # for row in Y_Data:
    #     Y.append(row[0])

    # X = np.array(X)
    # Y = np.array(Y)
    
    # print(X)
    # print(Y)

    # reg = LinearRegression().fit(X, Y)

    # print(reg.intercept_)
    # print(reg.coef_[0])

    # result  = reg.predict(np.array([[2, 20, 1, 11, 7.34]]))
    # result = round(result[0], 2)
    # print('Result: ', result)

    # cur.execute("UPDATE personalInfo SET joining_date = ? WHERE army_no = ?", ('2010-06-01','8888'))

    # cur.execute("INSERT OR IGNORE INTO firingInfo VALUES(?,?,?,?)", ('3333','2022-03-22','8.13','No Listed Error'))

    # cur.execute("DELETE FROM firingInfo WHERE army_no = ? AND firing_date = ?", ('2222','2022-03-22'))

    conn.commit()
    conn.close()

create_db()


# SELECT AVG(grouping) FROM firingInfo WHERE army_no = '3333' AND firing_date = '2022-03-20'


