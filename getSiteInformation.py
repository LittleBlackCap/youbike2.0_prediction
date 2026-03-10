# 將company_data中的各公司有登記的領導人姓名都抓下來
# 記得要重改，用思婷判斷的軟體業進行查詢，才能得到真的要的董監事名單

import json, ssl, urllib.request, mariadb, requests
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlunparse


def getSiteInformation():
    # sql config
    db_config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "Ts258775",
        "database": "Youbike",
        # 'charset': 'utf8mb4' # 超重要，沒有就完蛋，會直接卡住
    }
    tableName = "site"
    connect_db = None
    cursor = None

    try:
        connect_db = mariadb.connect(**db_config)
        print("connect_db connect")
        cursor = connect_db.cursor()

        # 為了完整更新整個表須將先前的資料刪除
        delete_query = """
            DELETE FROM {};
        """.format(tableName)
        cursor.execute(delete_query)
        connect_db.commit()

        
        cities = ["Taipei", "Taichung", "Kaohsiung"]
        urls = {
            "Taipei": "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json", 
            "Taichung": "	https://newdatacenter.taichung.gov.tw/api/v1/no-auth/resource.download?rid=ed5ef436-fb62-40ba-9ad7-a165504cd953",
            "Kaohsiung": "https://api.kcg.gov.tw/api/service/Get/b4dd9c40-9027-4125-8666-06bef1756092"
        }

        for i in range(len(cities)):
            city = cities[i]
            print("目前抓取" + city + "的站牌資料")

            context = ssl._create_unverified_context()
            url = urls[city]
            response = requests.get(url)

            try:
                response.raise_for_status()  # raises exception when not a 2xx response
                # # 跳過空白頁
                # if response.text == "":
                #     getTaipeiInformation()
            except requests.exceptions.HTTPError as e:
                # Whoops it wasn't a 200
                print("Error: " + str(e))

            if (city == cities[1]): # Taichung
                getTaichung(connect_db, cursor, tableName, response)
                continue

            # 將各站點車輛數量抓下來
            with urllib.request.urlopen(url, context=context) as jsondata:
                # 將JSON進行UTF-8的BOM解碼，並把解碼後的資料載入JSON陣列中
                data = json.loads(jsondata.read().decode("utf-8-sig"))
                # if data == "":
                #     getTaipeiInformation()
                if (city == cities[2]): # Kaohsiung
                    data = data["data"]["data"]["retVal"]

                api_count = len(data)
                for element in data:
                    # 將單一站點插入資料庫
                    insert_query = """
                        INSERT INTO {} (sno, sna, latitude, longitude, city) 
                        VALUES (%s, %s, %s, %s, %s);
                    """.format(tableName)

                    if (city == cities[0]): # Taipei
                        cursor.execute(
                            insert_query,
                            (
                                element["sno"],
                                element["sna"],
                                element["latitude"],
                                element["longitude"],
                                city,
                            ),
                        )
                    elif (city == cities[2]): # Kaohsiung
                        cursor.execute(
                            insert_query,
                            (
                                element["sno"],
                                element["sna"],
                                element["lat"],
                                element["lng"],
                                city,
                            ),
                        )

                    connect_db.commit()
                    # print("已插入" + element["sna"])
                
                query=f"SELECT COUNT(*) FROM {tableName} WHERE city=%s"
                cursor.execute(query, (city, ))
                insert_count = cursor.fetchone()[0]

                if insert_count == api_count:
                    print("資料筆數一致，共" + str(insert_count) + "筆")
                else:
                    print("資料筆數不一致，api" + str(api_count) +"筆、資料庫" + str(insert_count) + "筆")

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

def getTaichung(connect_db, cursor, tableName, response):
    print("修改中")
    pass

# def getKaohsiung():
#     1

if __name__ == "__main__":
    getSiteInformation()
