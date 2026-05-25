import os
import sys
import time
from time import sleep
from datetime import datetime
import uiautomator2 as u2
from common import adb, connection, go_home, open_bbklogs, get_cfg, take_screenshot, write_time_to_Excel_2_columns, write_start_end_time_test_to_Excel, fill_excel_with_basic_info, get_number_SIM  

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
    try:
        xp = '//android.widget.TextView[@resource-id="com.android.bbklog:id/issue_name" and (@text="Llamada/Señal" or @text="Phone call/Signal")]/parent::*'
        if d.xpath(xp).wait(timeout=3):
            d.xpath(xp).click()
            print("take_log: clicked via xpath parent for 'Llamada/Señal'")
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
    d(resourceId="android:id/edit").set_text("X_4G_Pospago")
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


def Twitter(d, destination_contact, repetitions=20, interval=60):
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
        resultado = write_time_to_Excel_2_columns(i+1, current_time, col_a="G", col_b="H", start_row=49, NW="4G", total_reps=repetitions)    #Escribe en Excel, pasar en que columnas, fila y RAT empieza a escribir,    

        if resultado is not None:             #Buble para determinar el tiempo de la primera y última iteración, resultado es una tupla (tipo, timestamp) donde tipo es "PRIMERA" o "ULTIMA" y timestamp es la hora en que se escribió en Excel
            tipo, ts = resultado       # Desempaquetamos la tupla (Ej: "PRIMERA", "06:14 PM")
            if tipo == "PRIMERA":
                tiempo_inicio = ts
            elif tipo == "ULTIMA":
                tiempo_fin = ts

        write_start_end_time_test_to_Excel(tiempo_inicio, tiempo_fin, col_c="C", col_d="D", start_row=24, NW="4G")  # Escribe en Excel el tiempo de la primera y última iteración del test, en las columnas C y D respectivamente, para la tecnología 3G. 
    
        try:
            app_opened = False
            app_icon = d.xpath('//android.widget.TextView[@content-desc="X" or @text="X"]')
            if app_icon.wait(timeout=5):
                app_icon.click()
                sleep(5)
                app_opened = True
            else:
                print("App icon not found; starting package com.twitter.android")
                try:
                    d.app_start("com.twitter.android")
                    sleep(6)
                    app_opened = True
                except Exception as e:
                    print("Failed to start app by package:", e)


            dm_selectors = [
                d(resourceId="com.twitter.android:id/dms"),
                d(resourceId="com.twitter.android:id/messages"),
                d(resourceId="com.twitter.android:id/x_chat"),
                d(description="Chat"),
                d(description="Messages"),
                d(description="Mensajes"),
                d(text="Chat"),
                d(text="Mensajes"),
                d(text="Messages"),
            ]

            if not app_opened:
                print("App did not open; skipping this iteration")
                go_home(d)
                try:
                    d.app_stop("com.twitter.android")
                except Exception:
                    pass
                continue

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

            info = dm_btn.info or {}
            bounds = info.get("bounds")
            if bounds:
                x = (bounds["left"] + bounds["right"]) // 2
                y = (bounds["top"] + bounds["bottom"]) // 2
                d.click(x, y)
            else:
                dm_btn.click()
            sleep(8)

            new_msg_selectors = [
                d(description="Mensaje nuevo"),
                d(resourceId="com.twitter.android:id/compose_button"),
                d.xpath('//android.view.View[@clickable="true" and @content-desc="Mensaje nuevo"]'),
            ]
            new_btn = None
            for sel in new_msg_selectors:
                if sel.wait(timeout=5):
                    new_btn = sel
                    break
            if new_btn:
                n_info = new_btn.info or {}
                n_bounds = n_info.get("bounds")
                if n_bounds:
                    nx = (n_bounds["left"] + n_bounds["right"]) // 2
                    ny = (n_bounds["top"] + n_bounds["bottom"]) // 2
                    d.click(nx, ny)
                else:
                    new_btn.click()
                sleep(2)
                to_field = d.xpath('//android.widget.EditText[@clickable="true" and @focusable="true"]')
                if to_field.wait(timeout=5):
                    t_info = to_field.info or {}
                    t_bounds = t_info.get("bounds")
                    if t_bounds:
                        tx = (t_bounds["left"] + t_bounds["right"]) // 2
                        ty = (t_bounds["top"] + t_bounds["bottom"]) // 2
                        d.click(tx, ty)
                    else:
                        to_field.click()
                    sleep(1)
                    to_field.set_text(destination_contact)
                    sleep(2)

                    handle = destination_contact
                    if not handle.startswith("@"):
                        handle = "@" + handle
                    match_xpath = f'//android.widget.TextView[@text="{handle}"]/ancestor::android.view.View[@clickable="true"]'
                    candidate = d.xpath(match_xpath)
                    if candidate.wait(timeout=5):
                        c_info = candidate.info or {}
                        c_bounds = c_info.get("bounds")
                        if c_bounds:
                            cx = (c_bounds["left"] + c_bounds["right"]) // 2
                            cy = (c_bounds["top"] + c_bounds["bottom"]) // 2
                            d.click(cx, cy)
                        else:
                            candidate.click()
                        sleep(2)

                        msg_xpath = '//android.widget.EditText[@clickable="true" and @focusable="true"]'
                        msg_field = d.xpath(msg_xpath)
                        if msg_field.wait(timeout=5):
                            m_info = msg_field.info or {}
                            m_bounds = m_info.get("bounds")
                            if m_bounds:
                                mx = (m_bounds["left"] + m_bounds["right"]) // 2
                                my = (m_bounds["top"] + m_bounds["bottom"]) // 2
                                d.click(mx, my)
                            else:
                                msg_field.click()
                            sleep(1)
                            msg_field.set_text(f"Test #{i+1}")
                            sleep(2)
                        else:
                            print("Message EditText not found")
                    else:
                        print("No matching user row found for", handle)
                else:
                    print("Recipient EditText not found after tapping new message")
            else:
                print("New message button not found")

            sleep(4)
            send_candidates = [
                d.xpath('//android.view.View[@content-desc="Enviar" or @content-desc="Send"]'),
                d.xpath('//android.view.View[@clickable="true" and @focusable="true" and (@content-desc="Enviar" or @content-desc="Send")]'),
                d.xpath('(//android.view.View[@clickable="true" and @focusable="true"])[last()]'),
            ]
            sent = False
            for sc in send_candidates:
                if sc.wait(timeout=3):
                    info = sc.info or {}
                    bounds = info.get('bounds')
                    if bounds:
                        x = (bounds['left'] + bounds['right']) // 2
                        y = (bounds['top'] + bounds['bottom']) // 2
                        d.click(x, y)
                    else:
                        sc.click()
                    sleep(1)
                    sent = True
                    break
            if not sent:
                print("No se encontró el botón Enviar.")

            sleep(2)
            go_home(d)
            d.app_stop("com.twitter.android")

        except Exception as e:
            print("Exception in Twitter loop:", e)
            try:
                go_home(d)
                d.app_stop("com.twitter.android")
            except Exception:
                pass
            continue

        elapsed = time.time() - iter_start
    print("Twitter schedule finished.")
            
def main():
    connection()
    sleep(250)  #250
    d = u2.connect()
    destination_contact = get_userx()
    interval = get_cfg("TWITTER_INTERVAL")
    reps     = get_cfg("TWITTER_REPS")
    open_bbklogs(d)
    sleep(5)
    take_log(d)
    open_settings(d)
    Twitter(d, destination_contact, repetitions=reps, interval=interval)
    number_10_digits = get_number_SIM(d)
    fill_excel_with_basic_info(NW="4G", SIM_number=number_10_digits, Linea ="Pospago")  #Llena en el excel el modelo y la fecha, en Línea colocar: "Pospago", "Prepago sin saldo" o "Prepago con saldo" dependiendo del tipo de línea que se esté probando
    close_settings(d)
    close_log(d)
    print("All repetitions completed. Exiting program.")

if __name__ == "__main__":
    main()