import mysql.connector

def getdbconnection():

    try:
        conn = mysql.connector.connect(host='127.0.0.1',user='root',password='root')
        conn.autocommit = False
        return conn

    except mysql.connector.Error as error:
        print("Failed to create connection: {}".format(error))
        # reverting changes because of exception
        conn.rollback()

def getsymbolid(symbol):
    try:
        conn = getdbconnection()
        cursor = conn.cursor()
        sql = f"select id from pbt.t_symbols where symbol='{symbol}'"
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchone()
        print(res[0])

    except Exception as error:
        print("Failed to get symbol id {}".format(error))
    finally:
        # closing database connection.
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("connection is closed")

def updateInstruments(
    ltp,
    change,
    symbolid
):
    sql = f"update pbt.t_instruments set LTP ={ltp}, CHANGEPER={change} where SYMBOL_ID={symbolid}"
    try:
        conn = getdbconnection()
        cursor = conn.cursor()
        print('Executing query : '+sql)
        cursor.execute(sql)
        conn.commit()
        print(cursor.rowcount, " row was updated")

    except Exception as error:
        print("Failed to insert data  {}".format(error))
    finally:
        # closing database connection.
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("connection is closed")

def insert(tablename, columns, values, valuesLen):
    try:
        conn = getdbconnection()
        cursor = conn.cursor()
        sql = f"INSERT INTO {tablename} {columns} VALUES {valuesLen}"
        print(sql)
        cursor.executemany(sql, values)
        conn.commit()
        print(cursor.rowcount, "was inserted.")

    except Exception as error:
        print("Failed to insert data  {}".format(error))
    finally:
        # closing database connection.
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("connection is closed")

def getAllRows(tableName):
    try:
        conn = getdbconnection()
        cursor = conn.cursor()
        sql = f"select * from {tableName}"
        cursor.execute(sql)
        myresult = cursor.fetchall()
        return myresult
    except Exception as error:
        print("Failed to insert data  {}".format(error))
    finally:
        # closing database connection.
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("connection is closed")
if __name__=="__main__":
    getsymbolid('NIFTY')