PASSWORD=root
USERNAME=root
DBNAME=final_project
 
"C:\Program Files\MySQL\MySQL Server 5.6\bin\mysql.exe" -u $USERNAME $DBNAME -p < sql/tbl_drop.sql
"C:\Program Files\MySQL\MySQL Server 5.6\bin\mysql.exe" -u $USERNAME $DBNAME -p < sql/tbl_create.sql
