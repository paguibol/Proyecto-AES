import time
from time import sleep
from datetime import datetime
import uiautomator2 as u2
import os
import sys
from common import adb, connection, fill_excel_with_basic_info, go_home, open_bbklogs, take_screenshot, get_cfg, write_time_to_Excel_2_columns, write_time_to_Excel_1_column, write_start_end_time_test_to_Excel

print(r"""
 ___      ___ ___  ___      ___ ________          ___   _________  _________        _____ ______   _______      ___    ___ ___  ________  ________     
|\  \    /  /|\  \|\  \    /  /|\   __  \        |\  \ |\___   ___\\___   ___\     |\   _ \  _   \|\  ___ \    |\  \  /  /|\  \|\   ____\|\   __  \    
\ \  \  /  / | \  \ \  \  /  / | \  \|\  \       \ \  \\|___ \  \_\|___ \  \_|     \ \  \\\__\ \  \ \   __/|   \ \  \/  / | \  \ \  \___|\ \  \|\  \   
 \ \  \/  / / \ \  \ \  \/  / / \ \  \\\  \       \ \  \    \ \  \     \ \  \       \ \  \\|__| \  \ \  \_|/__  \ \    / / \ \  \ \  \    \ \  \\\  \  
  \ \    / /   \ \  \ \    / /   \ \  \\\  \       \ \  \____\ \  \     \ \  \       \ \  \    \ \  \ \  \_|\ \  /     \/   \ \  \ \  \____\ \  \\\  \ 
   \ \__/ /     \ \__\ \__/ /     \ \_______\       \ \_______\ \__\     \ \__\       \ \__\    \ \__\ \_______\/  /\   \    \ \__\ \_______\ \_______\
    \|__|/       \|__|\|__|/       \|_______|        \|_______|\|__|      \|__|        \|__|     \|__|\|_______/__/ /\ __\    \|__|\|_______|\|_______|
                                        
                                                                                                                                                
""")
time.sleep(3)

def destination():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip()
    env = os.environ.get("MMS_PHONE")
    if env:
        return env.strip()
    try:
        if sys.stdin and sys.stdin.isatty():
            return input("Write the number you want to send the MMS to: ").strip()
    except Exception:
        pass
    raise RuntimeError("Destination phone not provided (argv or MMS_PHONE).")

def take_log(d):
    sleep(2)
    try:
        xp = '//android.widget.TextView[@resource-id="com.android.bbklog:id/issue_name" and (@text="Llamada/Señal" or @text="Phone call/Signal")]/parent::*'
        if d.xpath(xp).wait(timeout=3):
            d.xpath(xp).click()
            goto_start_record(d)
            return
    except Exception as e:
        print("take_log: xpath attempt failed:", e)


def goto_start_record(d):
    sleep(2)
    if d(resourceId="com.android.bbklog:id/log_record_start_btn").wait(timeout=10):
        d(resourceId="com.android.bbklog:id/log_record_start_btn").click()
        sleep(5)
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
    d(resourceId="android:id/edit").set_text("MMS_3G_Pospago")
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
    sleep(2)#
    d.app_stop("com.android.settings")




def mms(phone_number, repetitions=5, interval=60):
    d = u2.connect()
    now = time.time()
    start_time = ((int(now) // interval) + 1) * interval




    tiempo_inicio = None     # Variable para almacenar el timestamp de la primera iteración que se escriba en Excel
    tiempo_fin = None     # Variable para almacenar el timestamp de la última iteración que se escriba en Excel




    for i in range(repetitions):
        target_time = start_time + i * interval
        wait = target_time - time.time()
        if wait > 0:
            time.sleep(wait)

        iter_start = time.time()
        current_time = datetime.now().strftime('%I:%M %p') ##### Obtener timestamp actual para guardar en Excel


        print(f"MMS test #{i+1} started at {datetime.now().strftime(current_time)}")
        resultado =write_time_to_Excel_2_columns(i+1, current_time, col_a="C", col_b="D", start_row=36, NW="3G", total_reps=repetitions)    #Escribe en Excel, pasar en que columnas, fila y RAT empieza a escribir,   
        

        if resultado is not None:             #Buble para determinar el tiempo de la primera y última iteración, resultado es una tupla (tipo, timestamp) donde tipo es "PRIMERA" o "ULTIMA" y timestamp es la hora en que se escribió en Excel
            tipo, ts = resultado       # Desempaquetamos la tupla (Ej: "PRIMERA", "06:14 PM")
            if tipo == "PRIMERA":
                tiempo_inicio = ts
            elif tipo == "ULTIMA":
                tiempo_fin = ts

        write_start_end_time_test_to_Excel(tiempo_inicio, tiempo_fin, col_c="C", col_d="D", start_row=21, NW="3G")  # Escribe en Excel el tiempo de la primera y última iteración del test, en las columnas C y D respectivamente, para la tecnología 3G. 
    






        try:
            d.app_start("com.google.android.apps.messaging")
            if not d(packageName="com.google.android.apps.messaging").wait(timeout=10):
                print("Messaging app not found.")
                continue
            sleep(3)

            if d(resourceId="com.google.android.apps.messaging:id/start_chat_fab").wait(timeout=10):
                d(resourceId="com.google.android.apps.messaging:id/start_chat_fab").click()
                sleep(2)
            else:
                print("FAB button not found.")
                continue

            if d(resourceId="ContactSearchField").wait(timeout=10):
                d(resourceId="ContactSearchField").click()
                sleep(1)
                d(resourceId="ContactSearchField").set_text(phone_number)
                sleep(2)
                d.press("enter")
                sleep(2)
            else:
                print("Contact search field not found.")
                continue

            if d(description="Más").wait(timeout=5):
                d(description="Más").click()
                sleep(2)
            else:
                print("More options button not found.")
                continue

            if d(text="Mostrar campo de asunto").wait(timeout=10):
                d(text="Mostrar campo de asunto").click()
                sleep(2)
            else:
                print("Show subject field option not found.")
                continue

            if d(className="android.widget.EditText").wait(timeout=5):
                edt = d(className="android.widget.EditText")
                edt[0].click()
                sleep(0.5)
                edt[0].set_text(f"MMS Test #{i+1}")
                sleep(1)
            else:
                print("Subject field not found.")
                continue

            if d(text="Aceptar").wait(timeout=10):
                d(text="Aceptar").click()
                sleep(2)
            else:
                print("Accept button not found.")
                continue

            if d(resourceId="com.google.android.apps.messaging:id/compose_message_text").wait(timeout=10):
                d(resourceId="com.google.android.apps.messaging:id/compose_message_text").click()
                sleep(1)
                d(resourceId="com.google.android.apps.messaging:id/compose_message_text").set_text(f"Test number #{i+1}")
                sleep(2)

            if d(resourceId="Compose:Draft:Send").wait(timeout=5):
                d(resourceId="Compose:Draft:Send").click()
                sleep(10)
            else:
                print("Send button not found.")

        except Exception as e:
            print(f"MMS iteration {i+1} failed: {e}")

        finally:
            sleep(5)
            d.app_stop("com.google.android.apps.messaging")
            go_home(d)


def main():
    connection()
    interval = get_cfg("MMS_INTERVAL")
    reps     = get_cfg("MMS_REPS")
    d = u2.connect()
    phone_number = destination()
    open_bbklogs(d)
    take_log(d)
    open_settings(d)   
    mms(phone_number, repetitions=reps, interval=interval)



    fill_excel_with_basic_info(NW="3G")  #Llena en el excel el modelo y la fecha 


    close_settings(d)
    close_log(d)
    print("All repetitions completed. Exiting program.")

if __name__ == "__main__":
    main()