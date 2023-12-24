import mysql.connector
import sqlite3

#! MySql ====================================
db_samprity = mysql.connector.connect(
    host="localhost", user="root", password="root12", database="samprity_tower"
)

item_code = db_samprity.cursor()
item_code.execute(
    """SELECT 
    a.`Date_of_Transaction`,
    a.`item_id`,
    a.`Description`,
    IFNULL(REPLACE(a.`Unit`, '.', ''), 'LS') AS Unit,
    IFNULL(a.`Quantity`, 1) AS Quantity,
    ROUND(
        a.`Amount` / IFNULL(a.`Quantity`, 1),
        2
    ) AS rate,
    a.`Amount`,
    a.`Voucher_No`,
    a.`Remarks` 
    FROM
    `expenditure` a ;
    """
    )

myresult = item_code.fetchall()

#! Sqlite3 ==================================
conn = sqlite3.connect("ConstructionProject.sqlite3")
insert_cur = conn.cursor()
dt = conn.cursor()

sql = """INSERT INTO Accounts_expenditure(
    dateOfTransaction, item_id, description, unit, quantity, rate, amount, voucherNo, remarks) 
VALUES (?,?,?,?,?,?,?,?,?)"""
# val = [('Civil',),('Electrical',),('Sanitary',),('Carpenter',),('Thai and Glass',),('Plumber',)]
val = myresult
insert_cur.executemany(sql, val)
# insert_cur.execute("COMMIT")
dt.execute("Select * from Accounts_expenditure")
dt_recset = dt.fetchall()

conn.commit()
conn.close()
db_samprity.commit()
db_samprity.close()


print(dt_recset)
