import os
import time
from time import sleep
from datetime import datetime
import uiautomator2 as u2
from common import adb, connection, go_home, open_bbklogs, get_cfg, take_screenshot,write_time_to_Excel_1_column, write_start_end_time_test_to_Excel, fill_excel_with_basic_info

print(r"""
 __     __  ___  __     __   ___      _____   ___   _____   _       ____      _____   _____   ____    _____ 
 \ \   / / |_ _| \ \   / /  / _ \    |  ___| |_ _| | ____| | |     |  _ \    |_   _| | ____| / ___|  |_   _|
  \ \ / /   | |   \ \ / /  | | | |   | |_     | |  |  _|   | |     | | | |     | |   |  _|   \___ \    | |  
   \ V /    | |    \ V /   | |_| |   |  _|    | |  | |___  | |___  | |_| |     | |   | |___   ___) |   | |  
    \_/    |___|    \_/     \___/    |_|     |___| |_____| |_____| |____/      |_|   |_____| |____/    |_|          
                                    
                                                    ⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⡀⠀⠀⠀⠀
                                            ⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
                                            ⠀⢀⣾⣯⠻⣿⣿⣿⣿⡿⠟⠛⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣷⡀⠀
                                            ⠀⣾⣿⣿⣧⠈⠻⡿⠋⠀⠀⣀⣠⣄⣀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣷⠀
                                            ⢠⣿⣿⣿⣿⣧⠀⠀⠀⢠⣾⣿⣿⣿⣿⣷⡄⠀⠈⣿⣿⣿⣿⣿⣿⡄
                                            ⢸⣿⣿⣿⣿⣿⡇⠀⠀⢾⣿⣿⣿⣿⣿⣿⡷⠀⠀⢸⣿⣿⣿⣿⣿⡇
                                            ⠘⣿⣿⣿⣿⣿⣿⡀⠀⠘⢿⣿⣿⣿⣿⡿⠃⠀⢀⣿⣿⣿⣿⣿⣿⠃
                                            ⠀⢿⣿⣿⣿⣿⣿⣷℀⠀⠀⠉⠙⠋⠉⠀⠀⣠⣾⣿⣿⣿⣿⣿⡿⠀
                                            ⠀⠈⢿⣿⣿⣿⣿⣿⣿⣦⣤⣀⡀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡿⠁⠀
                                            ⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⠃⣠⣾⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
                                            ⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⡏⣰⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
                                            ⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠼⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀
""")
time.sleep(3)

def go_home(d):
    d.press("home")
    sleep(1)

def take_log(d):
    sleep(1)
    try:
        xp = '//android.widget.TextView[@resource-id="com.android.bbklog:id/issue_name" and (@text="Llamada/Señal" or @text="Phone call/Signal")]/parent::*'
        if d.xpath(xp).wait(timeout=3):
            d.xpath(xp).click()
            goto_start_record(d)
            return
    except Exception as e:
        print("take_log: xpath attempt failed:", e)


def goto_start_record(d):
    sleep(1)
    if d(resourceId="com.android.bbklog:id/log_record_start_btn").wait(timeout=10):
        d(resourceId="com.android.bbklog:id/log_record_start_btn").click()
        sleep(4)
        go_home(d)
    else:
        print("take_log: Start recording button not found.")

def close_log(d):
    try:
        open_bbklogs(d)
    except Exception:
        d.app_start("com.android.bbklog")
    sleep(2)
    if d(resourceId="com.android.bbklog:id/log_record_cancel").wait(timeout=10):
       d(resourceId="com.android.bbklog:id/log_record_cancel").click()
    else:
        print("Stop recording button not found.")
    sleep(2)
    if d(resourceId="android:id/button1").wait(timeout=10):
        d(resourceId="android:id/button1").click()
    else:
        print("Cancel button not found.")
    sleep(15)
    d(resourceId="com.android.bbklog:id/tv_more").wait(timeout=10)
    d(resourceId="com.android.bbklog:id/tv_more").click()
    sleep(2)
    more_item = d.xpath('(//android.widget.LinearLayout[@resource-id="android:id/content"])[2]')
    if more_item.wait(timeout=10):
        more_item.click()
    sleep(2)
    d(resourceId="com.android.bbklog:id/title").wait(timeout=10)
    d(resourceId="com.android.bbklog:id/title").click()
    sleep(2)
    d(resourceId="android:id/edit").wait(timeout=10)
    d(resourceId="android:id/edit").set_text("Internet_4G_Pospago")
    sleep(2)
    d(resourceId="android:id/button1").wait(timeout=10)
    d(resourceId="android:id/button1").click()
    sleep(3)
    d.app_stop("com.google.android.dialer")

def open_settings(d):
    d.app_start("com.android.settings")
    sleep(2)
    d(resourceId="android:id/title", text="Más conexiones").click_exists(timeout=5)
    sleep(2)
    d(description="Modo avión").click()
    print("Air plane mode disabled")
    sleep(2)
    d.app_stop("com.android.settings")

def close_settings(d):
    d.app_start("com.android.settings")
    sleep(2)
    d(resourceId="android:id/title", text="Más conexiones").click_exists(timeout=5)
    sleep(4)
    d(description="Modo avión").click()
    sleep(2)
    d.app_stop("com.android.settings")


def chrome_news(d, repetitions=5, interval=60):
    now = time.time()
    start_time = ((int(now) // interval) + 1) * interval

    tiempo_inicio = None     # Variable para almacenar el timestamp de la primera iteración que se escriba en Excel
    tiempo_fin = None     # Variable para almacenar el timestamp de la última iteración que se escriba en Excel


    for i in range(repetitions):
        target = start_time + i * interval
        wait = target - time.time()
        if wait > 0:
            time.sleep(wait)

        iter_start = time.time()
        current_time = datetime.now().strftime('%I:%M %p') ##### Obtener timestamp actual para guardar en Excel


        print(f"Internet test #{i+1} starting at {datetime.now().strftime(current_time)}")
        resultado = write_time_to_Excel_1_column(i+1, current_time, col="G", start_row=36, NW="4G", total_reps=repetitions)                #Escribe en Excel, pasar en que columna, fila y RAT empieza a escribir. Pospago celda =G36; Prepago con saldo celda = O36; prepago sin saldo celda= T56 


        if resultado is not None:             #Buble para determinar el tiempo de la primera y última iteración, resultado es una tupla (tipo, timestamp) donde tipo es "PRIMERA" o "ULTIMA" y timestamp es la hora en que se escribió en Excel
            tipo, ts = resultado       # Desempaquetamos la tupla (Ej: "PRIMERA", "06:14 PM")
            if tipo == "PRIMERA":
                tiempo_inicio = ts
            elif tipo == "ULTIMA":
                tiempo_fin = ts

        
        write_start_end_time_test_to_Excel(tiempo_inicio, tiempo_fin, col_c="C", col_d="D", start_row=22, NW="4G")  # Escribe en Excel el tiempo de la primera y última iteración del test, en las columnas C y D respectivamente, para la tecnología 3G. 
    
        


        d.app_start("com.android.chrome")
        sleep(2)
        if d(resourceId="com.android.chrome:id/url_bar").exists:
            d(resourceId="com.android.chrome:id/url_bar").click()
            sleep(1)
            d(resourceId="com.android.chrome:id/url_bar").set_text("news")
            d.press("enter")
        else:
            d.app_stop("com.android.chrome")
            continue

        sleep(7)
        go_home(d)
        d.app_stop("com.android.chrome")
        elapsed = time.time() - iter_start
    print("chrome_news schedule finished.")

def main():
    connection()
    sleep(250)
    d = u2.connect()
    interval = get_cfg("INTERNET_INTERVAL")
    reps     = get_cfg("INTERNET_REPS")
    open_bbklogs(d)
    sleep(5)
    take_log(d)
    open_settings(d)
    chrome_news(d, repetitions=reps, interval=interval)
    
    fill_excel_with_basic_info(NW="4G")  #Llena en el excel el modelo y la fecha 

    close_settings(d)
    close_log(d)
    print("All repetitions completed. Exiting program.")

if __name__ == "__main__":
    main()