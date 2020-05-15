import mysql.connector
from mysql.connector import errorcode
import datetime

class MySQLPipeline:

    insert_ = ("INSERT INTO web_scraping.quotes_tb"
                "(quote,author,tags,insert_time_stamp)"
                "VALUES (%s,%s,%s,%s)")
    config = {
            'user' : 'mysql1',
            'password' : 'password',
            'host' : '127.0.0.1',
            'database' : 'web_scraping'
            }

    def open_spider(self,spider):
        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cursor = self.cnx.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def process_item(self, item, spider):
        tags = self.list_to_string(item['tags'])
        try:
            #"*****************INSERTING INTO DB****************"
            self.cursor.execute(self.insert_,(item['title'].encode('utf-8'),
                                                 item['author'].encode('utf-8'),
                                                  tags.encode('utf-8'),
                                                 self.get_time_now()))
            self.cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        return item

    def list_to_string(self,s):
        str1 = ''
        for ele in s:
            str1 += ele +' '
        return str1

    def get_time_now(self):
        now = datetime.datetime.utcnow()
        today_now = now.strftime("%Y-%m-%d %H:%M:%S")
        return today_now