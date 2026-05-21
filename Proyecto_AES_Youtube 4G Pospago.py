import time
from time import sleep
from datetime import datetime
import os
import uiautomator2 as u2
from common import adb, connection, go_home, open_bbklogs, get_cfg, take_screenshot, write_time_to_Excel_1_column

print(r"""
 ___      ___ ___  ___      ___ ________          ___   _________  _________        _____ ______   _______      ___    ___ ___  ________  ________     
|\  \    /  /|\  \|\  \    /  /|\   __  \        |\  \ |\___   ___\\___   ___\     |\   _ \  _   \|\  ___ \    |\  \  /  /|\  \|\   ____\|\   __  \    
\ \  \  /  / | \  \ \  \  /  / | \  \|\  \       \ \  \\|___ \  \_\|___ \  \_|     \ \  \\\__\ \  \ \   __/|   \ \  \/  / | \  \ \  \___|\ \  \|\  \   
 \ \  \/  / / \ \  \ \  \/  / / \ \  \\\  \       \ \  \    \ \  \     \ \  \       \ \  \\|__| \  \ \  \_|/__  \ \    / / \ \  \ \  \    \ \  \\\  \  
  \ \    / /   \ \  \ \    / /   \ \  \\\  \       \ \  \____\ \  \     \ \  \       \ \  \    \ \  \ \  \_|\ \  /     \/   \ \  \ \  \____\ \  \\\  \ 
   \ \__/ /     \ \__\ \__/ /     \ \_______\       \ \_______\ \__\     \ \__\       \ \__\    \ \__\ \_______\/  /\   \    \ \__\ \_______\ \_______\
    \|__|/       \|__|\|__|/       \|_______|        \|_______|\|__|      \|__|        \|__|     \|__|\|_______/__/ /\ __\    \|__|\|_______|\|_______|
               
                                                                            ▄███████████▄
                                                                            █████░▀██████
                                                                            █████░░░▀████
                                                                            █████░░░▄████
                                                                            █████░▄██████
                                                                            █████████████
                                                                            ─▀▀▀▀▀▀▀▀▀▀▀─
""")
time.sleep(3)

def go_home(d):
    d.press("home")
    sleep(1)

def take_log(d):
    sleep(3)
    try:
        xp = '//android.widget.TextView[@resource-id="com.android.bbklog:id/issue_name" and (@text="Llamada/Señal" or @text="Phone call/Signal")]/parent::*'
        if d.xpath(xp).wait(timeout=3):
            d.xpath(xp).click()
            goto_start_record(d)
            return
    except Exception as e:
        print("take_log: xpath attempt failed:", e)

def goto_start_record(d):
    sleep(3)
    if d(resourceId="com.android.bbklog:id/log_record_start_btn").wait(timeout=10):
        d(resourceId="com.android.bbklog:id/log_record_start_btn").click()
        sleep(10)
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
    d(resourceId="android:id/edit").set_text("YT_4G_Pospago")
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

def youtube(d, repetitions=10, interval=60):
    now = time.time()
    start_time = ((int(now) // interval) + 1) * interval
    for i in range(repetitions):
        target = start_time + i * interval
        wait = target - time.time()
        if wait > 0:
            time.sleep(wait)
        iter_start = time.time()
        current_time = datetime.now().strftime('%I:%M %p') 

        print(f"YouTube test #{i+1} starting at {datetime.now().strftime(current_time)}")

        write_time_to_Excel_1_column(i+1, current_time, col="C", start_row=49, NW="3G")          #Escribe en Excel, pasar en que columna, fila y RAT empieza a escribir. Pospago celda =C49; Prepago con saldo celda = K49;  


        d.app_start("com.google.android.youtube")
        sleep(2)

        d(description="Shorts").click_exists(timeout=5)
        sleep(5)

        d.swipe_ext("up", scale=0.2)
        sleep(5)
        go_home(d)
        d.app_stop("com.google.android.youtube")
    print("YouTube schedule finished.")

def main():
    connection()
    sleep(300)
    d = u2.connect()
    interval = get_cfg("YT_INTERVAL")
    reps     = get_cfg("YT_REPS")
    open_bbklogs(d)
    sleep(5)
    take_log(d)
    open_settings(d)
    youtube(d, repetitions=reps, interval=interval)
    sleep(5)
    close_settings(d)
    close_log(d)
    print("All repetitions completed. Exiting program.")

if __name__ == "__main__":
    main()
