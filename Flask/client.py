import json
import requests
import pyodbc
import time
server = 'aaditechdb.database.windows.net'
database = 'JNPT_QA'
username = 'aaditechadmin'
password = 'AadiTech@123'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()
# conn = pyodbc.connect("DRIVER={SQL Server}; SERVER=localhost\SQLEXPRESS; Database=ParkingAi; trusted_connection=YES;")


IP = 'http://127.0.0.1'
PORT = '5000'
API = 'get_parking_results'




def main():
    cam = ""
    pid = ""
    p_value = ""
    pvalue = "0"

    url = IP + ":" + PORT + "/" + API

    count = 0
    while True:
        response = requests.post(url).json()
        print(response)
        time.sleep(5)
        if count == 2:
            print(count)
            count = 0
            # logic part
            # For Loop

            for key in response:
                result = response.get(key)
                # print(result)
                print(response)
                for spot_result in result:
                    # print(spot_result)
                    # print(result.get(spot_result))
                    pid = spot_result
                    p_value = result.get(spot_result)

                    if p_value:
                        pvalue = "1"
                    else:
                        pvalue = "0"

                    if key == str(1):
                        cam = "C1"
                    if key == str(2):
                        cam = "C3"

                    # print(key)

                    # print("UPDATE Hourly_Parking_Statistics SET [Date] = getdate(), IsOccupied = " + pvalue + " WHERE ParkingId = '" + str(pid) + "' AND Camera = '" + cam + "'")

                    cursor.execute("UPDATE Hourly_Parking_Statistics SET [Date] = getdate(), IsOccupied = " + pvalue + " WHERE ParkingId = '" + str(pid) + "' AND Camera = '" + cam + "'")
                    conn.commit()


        count += 1




if __name__ == '__main__':
    main()