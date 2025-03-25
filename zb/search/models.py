from django.db import models

# Create your models here.



import pymysql
from pymongo import cursor

# pymysql FFiElr MySQL R6528)↑F
from django.db import models

class bidding(models.Model):
    bid_title = models.CharField(max_length=255)
    bid_time = models.CharField(max_length=255)
    bid_text = models.CharField(max_length=19999)
    bid_web = models.CharField(max_length=255)
    bid_name=models.CharField(max_length=255)
    def __str__(self):
        return self.bid_title


'''
db = pymysql. connect(host='localhost' , user='root',passwd='147369510a!',db='testdb',port=3306)
cursor = db. cursor()
cursor .execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : %s " % data)
db. close()

db = pymysql. connect(host='localhost' , user='root',passwd='147369510a!',db='testdb',port=3306)
cursor.cursor = db. cursor()

#("DROP TABLE IF EXISTS EMPLOYEE")
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

sql1='CREATE TABLE BID(
bid_id int,
bid_time datetime(6),
bid_title varchar(255),
bid_text varchar(255),
bid_file blob,
bid_web varchar(255))'

cursor.execute(sql1)
db.close()


'''
'''
from django.db import models

class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class News(models.Model):
    headline = models.CharField(max_length=200)
    content = models.TextField()
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline
    
    
    

'''

'''      
迁移数据库：运行以下命令来应用模型的迁移并创建数据库表：

python manage.py makemigrations
python manage.py migrate
'''
