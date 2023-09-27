mysqld --user=root &
sleep 5
mysql < /backup.sql
cd /app
python3 app.py
tail -f /dev/null
