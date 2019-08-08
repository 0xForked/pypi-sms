#!/usr/bin/env python

import os
import pymysql

from pathlib import Path 
from dotenv import load_dotenv

from converterMessage import Message

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=str(env_path))

connection = pymysql.connect(
    str(os.getenv("DB_HOST")),
    str(os.getenv("DB_USERNAME")),
    str(os.getenv("DB_PASSWORD")),
    str(os.getenv("DB_DATABASE"))
)

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `sms_queues` WHERE `status` IN (%s, %s)"
        cursor.execute(sql, ('pending', 'failed'))
        result = cursor.fetchone()
        
        if result != None:
            with connection.cursor() as cursor:
                sql = "UPDATE sms_queues SET status='sending' WHERE id=%s"
                cursor.execute(sql, (result[0]))
            connection.commit()
            
            message = Message(result)
            status, id = message.send()
            
            if status == 1:
                with connection.cursor() as cursor:
                    sql = "UPDATE sms_queues SET status='sent' WHERE id=%s"
                    cursor.execute(sql, (id))
                connection.commit()
            else:
                with connection.cursor() as cursor:
                    sql = "UPDATE sms_queues SET status='failed' WHERE id=%s"
                    cursor.execute(sql, (id))
                connection.commit()
            
finally:
    connection.close()

