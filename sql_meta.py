# -*- coding: utf-8 -*-

import requests,re        
from lxml import html
from lxml import etree
# import threading
# from requests.exceptions import HTTPError
import time 
from datetime import datetime, timedelta
# import os


import plover as pw

db = pw.SqliteDatabase('lkzyfxfkf.db')

class Owner(pw.Model):
    site=pw.CharField(max_length=100)
    siteurl=pw.CharField(max_length=300, unique=True)
    created_at = pw.DateTimeField(default=datetime.now())
    updated_at = pw.DateTimeField()
    html=pw.TextField(default="")
    # '010101'=pw.IntegerField(default=0)
    # username = pw.CharField(max_length=255, unique=True)
    # points = pw.IntegerField(default=0)
    # age = pw.IntegerField(default=0)


    class Meta:
        database = db


class manufacture():
    
    def __init__(self,url):
        self.url = url
        try:
            self.hostName=re.compile(r".*\/\/([a-zA-Z\.]+)").findall(self.url)[0]
        except:
            self.hostName=re.sub(r'[\/:?;,\s]','', url)[0:50]
        self.db = pw.SqliteDatabase('lkzyfxfkf.db')
        self.db.connect()

        
    def __enter__(self):
        self.mkcolumn()
        
        
    def __exit__(self, exc_type, exc_value, traceback):
        pass
        self.db.close()
    
    def frtag(self,obxpt,whtrm=None):
        try:
            f = (lambda a: a[0] if (len(a)==1 ) else a)
            oxp=f(obxpt).get(whtrm).encode('utf-8').decode('utf-8')
        except Exception as e:
            # print e
            oxp=''
        return oxp        

    def gettime(self):
        dtnowday=time.strftime('%d/%m/%y', time.gmtime()).split('/') # 02/23/2017   ['07', '15', '2017']
        return ''.join(dtnowday)
        
    def columnexist(self,f):
        try:
            pass
            r = db.execute_sql("SELECT count(*) FROM owner o where o.'"+f+"'>-1").fetchall()
            return True
        except:
            print("--has been make column:'"+str(f)+"'")
            return False

    def gethtml(self):
        try:
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
                    ,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    }
            params = {}
            r = requests.get(self.url, stream=True, params=params,headers=headers)
            '''
                r.headers.get('content-length') 
                r.headers.get('last-modified')
            '''
            parsed_body = html.fromstring(r.text)
            htmltext=etree.tostring(parsed_body, encoding='utf-8')     
            return(r.headers.get('content-length'),htmltext)
        except:
            return(0,'')
        
        
    def existRec(self):
        try:
            r = db.execute_sql("SELECT count(*) FROM owner o where o.site='"+str(self.url)+"'").fetchall()
            return r[0][0]>0
        except:
            return False

    def addRec(self):
        fieldColumn=self.gettime()
        exist=self.existRec()
        htmlobj=self.gethtml()
        htmllen=htmlobj[0]
        htmltext=htmlobj[1]
        htmltext=htmltext.replace('\n', '').replace('\r', '').replace('\r\n', '').replace('"', "'")
        strSql='''INSERT INTO owner
                        (
                        'site'
                        ,'siteurl'
                        ,'updated_at'
                        ,'created_at'
                        ,'html'
                        ,"'''+str(fieldColumn)+'''"
                        )
                    VALUES
                        (
                        "'''+str(self.hostName)+'''"
                        ,"'''+str(self.url)+'''"
                        ,"'''+str(datetime.now())+'''"
                        ,""
                        ,"'''+str(htmltext)+'''"
                        ,'''+str(htmllen)+'''
                        )
                '''
        # print(strSql)
        try:
            db.execute_sql(strSql)
        except Exception as e:
            pass
        return 1
        


    def mkcolumn(self):
        fieldColumn=self.gettime()
        # exist =lambda _ : True if len([x for x in Owner._meta.fields.keys() if x==fieldColumn])>0 else False
        exist = self.columnexist(fieldColumn)
        if not exist: db.execute_sql("ALTER TABLE owner ADD COLUMN '"+fieldColumn+"' INTEGER(5) DEFAULT 0")
        
    def anyfunc(self):
        return True
        
    def cn(self,strng):
        return strng.decode('UTF-8').encode('cp1251')
        


if __name__ == '__main__':
    pass
    db.connect()
    db.create_tables([Owner], safe=True)  
    
    slist=[
    'https://blender.stackexchange.com/questions/2747/how-can-a-method-from-a-startup-script-be-invoked'
        ]
    
    for link in slist:
        rf=manufacture('https://blender.stackexchange.com/questions/2747/how-can-a-method-from-a-startup-script-be-invoked')
        rf.mkcolumn()
        rf.addRec()



'''
CREATE TABLE [goods] (
	[Code] bigint NOT NULL PRIMARY KEY, 
	[Barcode] nvarchar(255), 
	[Name] nvarchar(100), 
	[ECRName] nvarchar(200), 
	[Price] bigint, 
	[Rest] bigint, 
	[DiscountSchema_] int, 
	[flags] smallint, 
	[Store] smallint, 
	[MaxDC] smallint, 
	[TaxSchema_] int, 
	[Group_] bigint, 
	[Artikul] nvarchar(255), 
	[PriceLabel] int, 
	[Country] nvarchar(255), 
	[Unit] nvarchar(255)
)
GO
CREATE INDEX [iArtikul]
	ON [goods] ([Artikul])
GO
CREATE INDEX [iGoodBarcode]
	ON [goods] ([Barcode])
GO
CREATE INDEX [iGoodGroup]
	ON [goods] ([Group_])
GO
CREATE UNIQUE INDEX [iGoodsCode]
	ON [goods] ([Code])


id
site
siteurl
name
html
xxyyzz
xxyyzz


если нету на текущую дату 
    у этого хоста 
    создатьдляхоста()
иначе 
    пропустить

если нет колонки на эту дату
    создатьколонку()

создатьдляхоста()
    по хосту получить данные о количестве
    количествозаписсать(хост,количество)

количествозаписать(аа,ьь)
    если нету в таблице, где хост=аа,количество=бб
        тогда
    вставить в таблицу, где хост=аа,количество=бб

'''        
























































'''
CREATE TABLE [AccDiscounts] (
	[Code] int NOT NULL, 
	[Name] nvarchar(100), 
	[Value] bigint, 
	[ECRText] nvarchar(100), 
	[Enable] smallint, 
	[StartSumm] bigint, 
	[EndSumm] bigint, 
	[Schema_] int NOT NULL,
	CONSTRAINT [iAccDiscountCode] PRIMARY KEY ([Code], [Schema_])
)
GO

CREATE TABLE [autocds] (
	[Code] int NOT NULL, 
	[Name] nvarchar(100), 
	[Type] smallint, 
	[Value] bigint, 
	[ECRText] nvarchar(100), 
	[Enable] smallint, 
	[StartDateTime] datetime, 
	[EndDateTime] datetime, 
	[StartDay] smallint, 
	[EndDay] smallint, 
	[StartQuantity] bigint, 
	[EndQuantity] bigint, 
	[StartSumm] bigint, 
	[EndSumm] bigint, 
	[Schema_] int NOT NULL, 
	[ExtPrice_] int,
	CONSTRAINT [iAutoCDCode] PRIMARY KEY ([Code], [Schema_])
)
GO

CREATE TABLE [blacklist] (
	[Code] bigint NOT NULL, 
	[Scheme] int, 
	[Flags] int NOT NULL,
	CONSTRAINT [iBlackListCode] PRIMARY KEY ([Code], [Flags])
)
GO

CREATE TABLE [bonuses] (
	[Code] int NOT NULL PRIMARY KEY, 
	[Name] nvarchar(100), 
	[Text] nvarchar(100), 
	[Flags] int, 
	[Value] bigint, 
	[Limit] bigint
)
GO

CREATE TABLE [cards] (
	[Code] nvarchar(100) NOT NULL PRIMARY KEY, 
	[Name] nvarchar(100), 
	[Text] nvarchar(100), 
	[Flags] int, 
	[Credit] bigint, 
	[Acc] bigint, 
	[AutoSchema_] int, 
	[AccSchema_] int, 
	[Bonus] bigint, 
	[BonusSchema_] int
)
GO

CREATE TABLE [ext_prices] (
	[Code] int NOT NULL, 
	[Name] nvarchar(100), 
	[Price] bigint, 
	[Good_] bigint NOT NULL,
	CONSTRAINT [iExtPriceCode] PRIMARY KEY ([Code], [Good_])
)
GO

CREATE TABLE [fixcds] (
	[Code] int NOT NULL PRIMARY KEY, 
	[Prefix] nvarchar(100), 
	[Name] nvarchar(100), 
	[Type] smallint, 
	[Value] bigint, 
	[ECRText] nvarchar(100), 
	[Flags] int, 
	[ToPrefix] nvarchar(100), 
	[ExtPrice_] int
)
GO

CREATE TABLE [good_set_list] (
	[Code] int NOT NULL IDENTITY(1,1) PRIMARY KEY, 
	[Good] bigint, 
	[GoodSet] int
)
GO

CREATE TABLE [good_sets] (
	[Code] int NOT NULL PRIMARY KEY, 
	[Name] nvarchar(100), 
	[Discount] int
)
GO

CREATE TABLE [goods] (
	[Code] bigint NOT NULL PRIMARY KEY, 
	[Barcode] nvarchar(255), 
	[Name] nvarchar(100), 
	[ECRName] nvarchar(200), 
	[Price] bigint, 
	[Rest] bigint, 
	[DiscountSchema_] int, 
	[flags] smallint, 
	[Store] smallint, 
	[MaxDC] smallint, 
	[TaxSchema_] int, 
	[Group_] bigint, 
	[Artikul] nvarchar(255), 
	[PriceLabel] int, 
	[Country] nvarchar(255), 
	[Unit] nvarchar(255)
)
GO
CREATE INDEX [iArtikul]
	ON [goods] ([Artikul])
GO
CREATE INDEX [iGoodBarcode]
	ON [goods] ([Barcode])
GO
CREATE INDEX [iGoodGroup]
	ON [goods] ([Group_])
GO
CREATE UNIQUE INDEX [iGoodsCode]
	ON [goods] ([Code])
GO

CREATE TABLE [items] (
	[Barcode] nvarchar(255) NOT NULL PRIMARY KEY, 
	[Name] nvarchar(100), 
	[ECRName] nvarchar(100), 
	[Price] bigint, 
	[Koef] bigint, 
	[Code_] bigint
)
GO
CREATE INDEX [iItemsCode_]
	ON [items] ([Code_])
GO

CREATE TABLE [schemas] (
	[Code] int NOT NULL PRIMARY KEY, 
	[Name] nvarchar(100), 
	[OnlyCard] int
)
GO

CREATE TABLE [sellers] (
	[Code] int NOT NULL PRIMARY KEY, 
	[Name] nvarchar(100), 
	[Text] nvarchar(100)
)
GO

CREATE TABLE [users] (
	[Code] int NOT NULL PRIMARY KEY, 
	[Name] nvarchar(100), 
	[Password] nvarchar(25), 
	[Bitmap] nvarchar(255), 
	[Group_] int, 
	[Card] nvarchar(100)
)

'''