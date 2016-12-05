PASSWORD=root
USERNAME=root
DBNAME=final_project
 
mysql -u $USERNAME $DBNAME -p < sql/tbl_drop.sql
mysql -u $USERNAME $DBNAME -p < sql/tbl_create.sql