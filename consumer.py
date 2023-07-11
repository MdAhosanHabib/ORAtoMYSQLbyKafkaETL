import json
from kafka import KafkaConsumer
import mysql.connector
import time

consumer = KafkaConsumer('server1.AHOSAN.TEST', bootstrap_servers='192.168.222.128:9092')

mysql_table = 'todo'
mysql_connection = mysql.connector.connect(
    host="192.168.222.128",
    user="TodoList",
    password="Todo_List123",
    database="TodoList"
)

mysql_cursor = mysql_connection.cursor()

while True:
    for message in consumer:
        change_event = json.loads(message.value)
        print (change_event)

        #get and serial data from kafka
        payload = change_event.get('payload', {})
        data = payload.get('after', {})

        name = data.get('NAME', '')
        address = data.get('ADDRESS', '')
        phone = data.get('PHONE', '')

        #insert the data into MySQL
        insert_query = "INSERT INTO {} (name, address, phone) VALUES (%s, %s, %s)".format(mysql_table)
        values = (name, address, phone)
        mysql_cursor.execute(insert_query, values)
        mysql_connection.commit()

    time.sleep(1)
