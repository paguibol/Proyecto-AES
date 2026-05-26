import os
import sys
import time
from time import sleep
from datetime import datetime
import uiautomator2 as u2
from common import adb, connection, go_home, open_bbklogs, get_cfg, paste_to_excel_screenshot, take_screenshot, write_time_to_Excel_1_column, write_start_end_time_test_to_Excel, fill_excel_with_basic_info, get_number_SIM, paste_to_excel_screenshot 

print(r"""
 ___      ___ ___  ___      ___ ________          ___   _________  _________        _____ ______   _______      ___    ___ ___  ________  ________     
|\  \    /  /|\  \|\  \    /  /|\   __  \        |\  \ |\___   ___\\___   ___\     |\   _ \  _   \|\  ___ \    |\  \  /  /|\  \|\   ____\|\   __  \    
\ \  \  /  / | \  \ \  \  /  / | \  \|\  \       \ \  \\|___ \  \_\|___ \  \_|     \ \  \\\__\ \  \ \   __/|   \ \  \/  / | \  \ \  \___|\ \  \|\  \   
 \ \  \/  / / \ \  \ \  \/  / / \ \  \\\  \       \ \  \    \ \  \     \ \  \       \ \  \\|__| \  \ \  \_|/__  \ \    / / \ \  \ \  \    \ \  \\\  \  
  \ \    / /   \ \  \ \    / /   \ \  \\\  \       \ \  \____\ \  \     \ \  \       \ \  \    \ \  \ \  \_|\ \  /     \/   \ \  \ \  \____\ \  \\\  \ 
   \ \__/ /     \ \__\ \__/ /     \ \_______\       \ \_______\ \__\     \ \__\       \ \__\    \ \__\ \_______\/  /\   \    \ \__\ \_______\ \_______\
    \|__|/       \|__|\|__|/       \|_______|        \|_______|\|__|      \|__|        \|__|     \|__|\|_______/__/ /\ __\    \|__|\|_______|\|_______|
       
                                                   
                                                   
                            ░░░░░░░░         ░░    
    ░░░       ░▒▒▒▒▒▒░░▒░░░  ░██░░▓█░      ░█▓░    
    ▒▒▒░░    ░▒▒▒▒▒▒▒▒▒▒░░░   ░▒█░░▒█▒   ░▓█░░     
    ░▒▒▒▒▒▒░░░▒▒▒▒▒▒▒▒▒░░      ░░█▒░░█▓░▒█▒░       
   ░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░         ░█▓░░▓█▓░         
    ░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░           ▒█░░▒█▒         
    ░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░             ▒██▒░░█▓░       
      ░▒▒▒▒▒▒▒▒▒▒▒▒▒░░           ░█▓░░█▓░ ▓█░      
      ░░░▒▒▒▒▒▒▒▒▒░░           ░▓█░░  ░▓█░░▒█░░    
   ░░▒▒▒▒▒▒▒▒▒▒░░░           ░░█▒       ░█▒░░█▓░░  
      ░░░░░░░░░              ░░░         ░░░░░░░░  
                                                   
                                                                                                                                                                                                                                                                                                                                                        
""")
time.sleep(3)

def get_userx():
    if len(sys.argv) > 1 and sys.argv[1].strip():
        return sys.argv[1].strip()
    u = os.environ.get("AES_USERX")
    if u:
        return u.strip()
    try:
        if sys.stdin and sys.stdin.isatty():
            return input("Write Twitter/X username: ").strip()
    except Exception:
        pass
    
def take_log(d):
    sleep(3)
    xp = '//android.widget.TextView[@resource-id="com.android.bbklog:id/issue_name" and (@text="Llamada/Señal" or @text="Phone call/Signal")]/parent::*'
    if d.xpath(xp).wait(timeout=3):
        d.xpath(xp).click()
        goto_start_record(d)
        return


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
    d(resourceId="android:id/edit").set_text("X_3G_Sin saldo")
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


def get_bounds_center(bounds):
    if not bounds:
        return None
    center_x = (bounds["left"] + bounds["right"]) // 2
    center_y = (bounds["top"] + bounds["bottom"]) // 2
    return center_x, center_y


def get_first_dm_search_result(d):
    excluded_descriptions = {"Buscar", "Search", "Chat", "Mensajes", "Messages", "Atrás", "Back"}
    search_field = d.xpath('//android.widget.EditText[@clickable="true" and @focusable="true"]')
    search_bottom = 0

    if search_field.wait(timeout=3):
        search_info = search_field.info or {}
        search_bounds = search_info.get("bounds")
        if search_bounds:
            search_bottom = search_bounds["bottom"]

    candidates = d.xpath('//android.view.View[@clickable="true" and @focusable="true" and @content-desc]').all()
    for candidate in candidates:
        candidate_info = candidate.info or {}
        candidate_bounds = candidate_info.get("bounds")
        candidate_desc = candidate_info.get("contentDescription") or candidate_info.get("content-desc")

        if not candidate_bounds or not candidate_desc:
            continue
        if candidate_desc in excluded_descriptions:
            continue
        if candidate_bounds["top"] <= search_bottom:
            continue
        return candidate

    return None


def Twitter(d, repetitions=20, interval=60):
    now = time.time()
    start_time = ((int(now) // interval) + 1) * interval

    tiempo_inicio = None
    tiempo_fin = None

    for i in range(repetitions):
        target = start_time + i * interval
        wait = target - time.time()
        if wait > 0:
            time.sleep(wait)

        iter_start = time.time()
        current_time = datetime.now().strftime('%I:%M %p') ##### Obtener timestamp actual para guardar en Excel

        print(f"Twitter test #{i+1} starting at {datetime.now().strftime(current_time)}")
        resultado = write_time_to_Excel_1_column(i+1, current_time, col="T", start_row=96, NW="3G", total_reps=repetitions)    #Escribe en Excel, pasar en que columnas, fila y RAT empieza a escribir,    
        
        if resultado is not None:             #Buble para determinar el tiempo de la primera y última iteración, resultado es una tupla (tipo, timestamp) donde tipo es "PRIMERA" o "ULTIMA" y timestamp es la hora en que se escribió en Excel
            tipo, ts = resultado       # Desempaquetamos la tupla (Ej: "PRIMERA", "06:14 PM")
            if tipo == "PRIMERA":
                tiempo_inicio = ts
            elif tipo == "ULTIMA":
                tiempo_fin = ts

        write_start_end_time_test_to_Excel(tiempo_inicio, tiempo_fin, col_c="G", col_d="H", start_row=24, NW="3G")  # Escribe en Excel el tiempo de la primera y última iteración del test, en las columnas C y D respectivamente, para la tecnología 3G. 
    
        d.app_start("com.twitter.android")

        dm_selectors = [
            d.xpath('//android.widget.LinearLayout[@content-desc="Chat" and @clickable="true"]'),
            d(className="android.widget.LinearLayout", description="Chat"),
            d.xpath('//android.view.View[@resource-id="com.twitter.android:id/x_chat"]/parent::android.widget.LinearLayout[@clickable="true"]'),
            d(resourceId="com.twitter.android:id/x_chat"),
        ]

        dm_btn = None
        for sel in dm_selectors:
            if sel.wait(timeout=3):
                dm_btn = sel
                break

        if not dm_btn:
            print("DM button not found; skipping this iteration.")
            go_home(d)
            d.app_stop("com.twitter.android")
            continue

        dm_btn.click()
        sleep(8)

        search_user_selectors = [
            d.xpath('//android.view.View[@clickable="true" and @focusable="true"][.//android.view.View[@content-desc="Buscar"]]'),
            d.xpath('//android.view.View[@clickable="true" and @focusable="true"][.//android.widget.TextView[@text="Buscar"]]'),
            d.xpath('//android.view.View[@clickable="true" and @focusable="true"][.//android.view.View[@content-desc="Search"]]'),
            d.xpath('//android.view.View[@clickable="true" and @focusable="true"][.//android.widget.TextView[@text="Search"]]'),
        ]

        search_user_btn = None
        for sel in search_user_selectors:
            if sel.wait(timeout=5):
                search_user_btn = sel
                break

        if not search_user_btn:
            print("Buscar/Search button not found")
            go_home(d)
            d.app_stop("com.twitter.android")
            continue

        search_user_btn.click()
        sleep(2)

        candidate = get_first_dm_search_result(d)

        if not candidate:
            print("No search result found after tapping Buscar/Search")
            go_home(d)
            d.app_stop("com.twitter.android")
            continue

        candidate_info = candidate.info or {}
        candidate_bounds = candidate_info.get("bounds")
        candidate_center = get_bounds_center(candidate_bounds)
        if candidate_center:
            center_x, center_y = candidate_center
            d.click(center_x, center_y)
        else:
            candidate.click()
        sleep(2)

        msg_xpath = '//android.widget.EditText[@clickable="true" and @focusable="true"]'
        msg_field = d.xpath(msg_xpath)
        if msg_field.wait(timeout=5):
            msg_field.click()
            sleep(1)
            msg_field.set_text(f"Test #{i+1}")
            sleep(2)
        else:
            print("Message EditText not found")

        sleep(4)
        send_candidates = [
            d.xpath('//android.view.View[@content-desc="Enviar" or @content-desc="Send"]'),
            d.xpath('//android.view.View[@clickable="true" and @focusable="true" and (@content-desc="Enviar" or @content-desc="Send")]'),
            d.xpath('(//android.view.View[@clickable="true" and @focusable="true"])[last()]'),
        ]
        sent = False
        for sc in send_candidates:
            if sc.wait(timeout=3):
                sc.click()
                sleep(1)
                sent = True
                break
        if not sent:
            print("No se encontró el botón Enviar.")

        sleep(10)
        if i == 1:
            sleep(2)
            tech, network, path = take_screenshot(d)
            sleep(2)
            paste_to_excel_screenshot(NW=network, test_name=tech, ruta_imagen=path)
            sleep(5)
        else:
            d.app_stop("com.twitter.android")
            go_home(d)
    print("Twitter schedule finished.")
            
def main():
    connection()
    sleep(250)
    d = u2.connect()
    interval = get_cfg("TWITTER_INTERVAL")
    reps     = get_cfg("TWITTER_REPS")
    open_bbklogs(d)
    sleep(5)
    take_log(d)
    open_settings(d)
    Twitter(d, repetitions=reps, interval=interval)
    number_10_digits = get_number_SIM(d)
    fill_excel_with_basic_info(NW="3G", SIM_number=number_10_digits, Linea ="Prepago sin saldo")  #Llena en el excel el modelo y la fecha, en Línea colocar: "Pospago", "Prepago sin saldo" o "Prepago con saldo" dependiendo del tipo de línea que se esté probando

    close_settings(d)
    close_log(d)
    print("All repetitions completed. Exiting program.")

if __name__ == "__main__":
    main()