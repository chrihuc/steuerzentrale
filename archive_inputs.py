
import MySQLdb as mdb
import constants

con = mdb.connect(constants.sql_.IP, constants.sql_.USER, constants.sql_.PASS, constants.sql_.DB)
with con:
    cur = con.cursor()
    cur.execute("SELECT t1.COLUMN_NAME \
FROM (SELECT COLUMN_NAME \
FROM INFORMATION_SCHEMA.COLUMNS \
WHERE TABLE_NAME = N'HIS_inputs') t1 \
LEFT JOIN \
    (SELECT COLUMN_NAME \
FROM INFORMATION_SCHEMA.COLUMNS \
WHERE TABLE_NAME = N'HIS_inputs_arch') t2 \
ON t1.COLUMN_NAME = t2.COLUMN_NAME WHERE t2.COLUMN_NAME is NULL; ")
    results = cur.fetchall()
    for row in results:
        print(row[0])
        ist = "ALTER TABLE `%s` ADD `%s` DECIMAL(8,3)" % ('HIS_inputs_arch', row[0])
        cur.execute(ist)   
#    cmd = "START TRANSACTION;\
#set @N := (now());\
#INSERT INTO Steuerzentrale.HIS_inputs_arch select * from Steuerzentrale.HIS_inputs where Date < date_sub(@N,INTERVAL 31 DAY);\
#DELETE FROM Steuerzentrale.HIS_inputs WHERE Date < date_sub(@N,INTERVAL 31 DAY);\
#COMMIT;"
#    cur.execute(cmd)
con.close()


#START TRANSACTION;
#set @N := (now());
#INSERT INTO Steuerzentrale.HIS_inputs_arch select * from Steuerzentrale.HIS_inputs where Date < date_sub(@N,INTERVAL 14 DAY);
#DELETE FROM Steuerzentrale.HIS_inputs WHERE Date < date_sub(@N,INTERVAL 14 DAY);
#COMMIT;
#
#SELECT COLUMN_NAME
#FROM INFORMATION_SCHEMA.COLUMNS
#WHERE TABLE_NAME = N'HIS_inputs'
#
#IF EXISTS(SELECT 1 FROM sys.columns 
#          WHERE Name = N'columnName'
#          AND Object_ID = Object_ID(N'schemaName.tableName'))
#BEGIN
#    -- Column Exists
#END
#
#
#ALTER TABLE HIS_inputs_arch
#ADD
#
#
#SELECT t1.COLUMN_NAME
#FROM (SELECT COLUMN_NAME
#FROM INFORMATION_SCHEMA.COLUMNS
#WHERE TABLE_NAME = N'HIS_inputs') t1
#LEFT JOIN
#    (SELECT COLUMN_NAME
#FROM INFORMATION_SCHEMA.COLUMNS
#WHERE TABLE_NAME = N'HIS_inputs_arch') t2
#ON t1.COLUMN_NAME = t2.COLUMN_NAME WHERE t2.COLUMN_NAME is NULL; 