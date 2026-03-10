# 將company_data中的各公司有登記的領導人姓名都抓下來
# 記得要重改，用思婷判斷的軟體業進行查詢，才能得到真的要的董監事名單

import json, ssl, urllib.request, mariadb,requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlunparse


def getTaipeiInformation():    
    # sql config
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'Ts258775',
        'database': 'Youbike',
    }
    connect_db = None
    cursor = None
    
    try:
        connect_db = mariadb.connect(**db_config)
        print("connect_db connect")
        cursor = connect_db.cursor()

        # # 為了完整更新整個表須將先前的資料刪除
        # delete_query = """
        #     DELETE FROM {tableName};
        # """
        # cursor.execute(delete_query)
        # connect_db.commit()
        
        
        
        tableName = 'taipei'
        url="https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
        context = ssl._create_unverified_context()
        response = requests.get(url)
        
        try:
            response.raise_for_status() # raises exception when not a 2xx response
            # # 跳過空白頁
            # if response.text == "":
            #     getTaipeiInformation()
        except requests.exceptions.HTTPError as e:
            # Whoops it wasn't a 200
            print("Error: " + str(e))

        # 將各站點車輛數量抓下來
        with urllib.request.urlopen(url, context=context) as jsondata:
            #將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
            data = json.loads(jsondata.read().decode('utf-8-sig')) 
            # if data == "":
            #     getTaipeiInformation()
            for element in data:
                # 將單一站點插入資料庫
                insert_query = """
                    INSERT INTO {} (sno, quantity, available_rent_bikes, available_return_bikes, infoTime) 
                    VALUES (%s, %s, %s, %s, %s);
                """.format(tableName)

                cursor.execute(insert_query, (element["sno"], element["sna"], element["latitude"], element["longitude"], element["Quantity"], element["available_rent_bikes"], element["available_return_bikes"], element["infoTime"]))
                connect_db.commit()
                print("已插入" + element["sna"])
                
            
                
    except mariadb.Error as err:
        print(f"Error: {err}\n")

    
    finally:
        if cursor:
            cursor.close()
        if connect_db:
            connect_db.close()
            print("connect_db closed")

# def getTaipei():
#     1

# def getTaichung():
#     1

# def getKaohsiung():
#     1

if __name__=="__main__":
    print("目前僅抓取台北之資料")
    getTaipeiInformation()
