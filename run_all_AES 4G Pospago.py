from common import DEFAULTS
import contextlib
import subprocess
import sys
import os
from collections import deque
from pathlib import Path
import runpy
import io
from datetime import datetime
import argparse
import time
import re
import shutil
import threading
_env_root = os.environ.get("AES_ROOT")
if _env_root:
    ROOT = Path(_env_root)
    LOGS = ROOT / "logs"
elif getattr(sys, "frozen", False):
    ROOT = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    LOGS = Path(sys.executable).parent / "logs"
from common import DEFAULTS
import contextlib
import subprocess
import sys
import os
from collections import deque
from pathlib import Path
import runpy
import io
from datetime import datetime
import argparse
import time
import re
import shutil
import threading

_env_root = os.environ.get("AES_ROOT")
if _env_root:
    ROOT = Path(_env_root)
    LOGS = ROOT / "logs"
elif getattr(sys, "frozen", False):
    ROOT = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    LOGS = Path(sys.executable).parent / "logs"
else:
    ROOT = Path(__file__).parent.resolve()
    LOGS = ROOT / "logs"

LOGS.mkdir(parents=True, exist_ok=True)

DEFAULT_SCRIPTS = [
    "Proyecto_AES_MMS 4G Pospago.py",
    "Proyecto_AES_Internet 4G Pospago.py",
    "Proyecto_AES_Youtube 4G Pospago.py",
    "Proyecto_AES_Twitter 4G Pospago.py",
    "Proyecto_AES_Messenger 4G Pospago.py",
    "Proyecto_AES_Gmail 4G Pospago.py",
]


def list_scripts():
    return [ROOT / s for s in DEFAULT_SCRIPTS if (ROOT / s).exists()]


def cleanup_device():
    try:
        out = subprocess.run(["adb", "shell", "pm", "list", "packages"],
                             capture_output=True, text=True, check=False)
        pkgs = [line.split(":")[-1].strip() for line in out.stdout.splitlines()]
        patterns = ("uia", "wetest", "uiautomator", "appium", "uia2")
        to_stop = [p for p in pkgs if any(re.search(pat, p, re.I) for pat in patterns)]
        common = ["com.wetest.uia2", "io.appium.uiautomator2.server", "com.github.uiautomator"]
        for c in common:
            if c not in to_stop:
                to_stop.append(c)
        stopped = []
        for p in to_stop:
            if not p or p.startswith("com.android"):
                continue
            subprocess.run(["adb", "shell", "am", "force-stop", p],
                           capture_output=True, text=True)
            stopped.append(p)
        subprocess.run(["adb", "shell", "input", "keyevent", "3"], capture_output=True, text=True)
        time.sleep(1)
        if stopped:
            print(f"[runner] cleanup_device: stopped: {', '.join(sorted(set(stopped)))}")
    except Exception as e:
        print("[runner] cleanup_device error:", e)


def detect_and_respond(line, proc_stdin, email, phone, userx, userf):
    s = (line or "").lower()
    try:
        if any(x in s for x in ("write the email", "email address", "write the e-mail")) and email:
            proc_stdin.write(email + "\n"); proc_stdin.flush(); print(f"[runner] sent email: {email}"); return True
        if any(x in s for x in ("write the number", "phone number", "write the phone")) and phone:
            proc_stdin.write(phone + "\n"); proc_stdin.flush(); print(f"[runner] sent phone: {phone}"); return True
        if any(x in s for x in ("write the contact of twitter", "write the contact of twitter(x)", "write the user", "write twitter user")) and userx:
            proc_stdin.write(userx + "\n"); proc_stdin.flush(); print(f"[runner] sent userx: {userx}"); return True
        if any(x in s for x in ("write the contact of facebook", "write the contact of facebook", "write facebook user", "write the userf", "write userf")) and userf:
            proc_stdin.write(userf + "\n"); proc_stdin.flush(); print(f"[runner] sent userf: {userf}"); return True
        if any(x in s for x in ("press enter", "press any key")):
            proc_stdin.write("\n"); proc_stdin.flush(); print("[runner] pressed Enter"); return True
    except Exception:
        pass
    return False


def run_script(path: Path, email: str, phone: str, userx: str, userf: str, timeout: int):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = LOGS / f"{path.stem}_{ts}.log"
    if not path.exists():
        msg = f"[runner] script not found: {path}"
        print(msg)
        with open(LOGS / f"{path.stem}_{ts}.log", "w", encoding="utf-8") as f:
            f.write(msg + "\n")
        return 1, str(log_path)
    
    if getattr(sys, "frozen", False):
        rc = 0
        try:
            with open(log_path, "w", encoding="utf-8") as f:
                orig_stdout = getattr(sys, "__stdout__", None) or sys.stdout
                orig_stderr = getattr(sys, "__stderr__", None) or sys.stderr
                class Tee:
                    def __init__(self, *streams):
                        self.streams = streams
                    def write(self, data):
                        for s in self.streams:
                            try:
                                s.write(data)
                            except Exception:
                                pass
                    def flush(self):
                        for s in self.streams:
                            try:
                                s.flush()
                            except Exception:
                                pass

                tee_out = Tee(orig_stdout, f)
                tee_err = Tee(orig_stderr, f)

                import builtins
                _orig_input = builtins.input
                def _auto_input(prompt=""):
                    p = (prompt or "").lower()
                    tee_out.write(str(prompt)); tee_out.flush()
                    if any(x in p for x in ("write the number", "phone number", "write the phone")) and phone:
                        tee_out.write(phone + "\n"); tee_out.flush(); return phone
                    if any(x in p for x in ("write the email", "email address", "write the e-mail")) and email:
                        tee_out.write(email + "\n"); tee_out.flush(); return email
                    if any(x in p for x in ("write the contact of twitter", "write twitter user", "write the user", "twitter/x username", "twitter username")) and userx:
                        tee_out.write(userx + "\n"); tee_out.flush(); return userx
                    if any(x in p for x in ("write the contact of facebook", "write facebook user", "write userf", "messenger/facebook username", "messenger username", "facebook username")) and userf:
                        tee_out.write(userf + "\n"); tee_out.flush(); return userf
                    return _orig_input()
                builtins.input = _auto_input
                if email:
                    os.environ["AES_EMAIL"] = email
                    os.environ["EMAIL_DEST"] = email
                if phone:
                    os.environ["AES_PHONE"] = phone
                    os.environ["MMS_PHONE"] = phone
                if userx:
                    os.environ["AES_USERX"] = userx
                if userf:
                    os.environ["AES_USERF"] = userf
                try:
                    with contextlib.redirect_stdout(tee_out), contextlib.redirect_stderr(tee_err):
                        runpy.run_path(str(path), run_name="__main__")
                finally:
                    builtins.input = _orig_input
        except SystemExit as e:
            try:
                rc = int(e.code) if e.code is not None else 0
            except Exception:
                rc = 0
        except Exception as e:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"[runner] exception: {e}\n")
            rc = 1
        return rc, str(log_path)

    python_exec = shutil.which("py") or shutil.which("python") or sys.executable
    cmd = [python_exec, str(path)]
    if "Proyecto_AES_MMS" in path.name and phone:
        cmd.append(phone)
    if "Proyecto_AES_Gmail" in path.name and email:
        cmd.append(email)
    if "Proyecto_AES_Twitter" in path.name and userx:
        cmd.append(userx)
    if "Proyecto_AES_Messenger" in path.name and userf:
        cmd.append(userf)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    if userx:
        env["AES_USERX"] = userx
    if userf:
        env["AES_USERF"] = userf
    if email:
        env["AES_EMAIL"] = email
        env["EMAIL_DEST"] = email
    if phone:
        env["AES_PHONE"] = phone
        env["MMS_PHONE"] = phone

    proc = subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        bufsize=1,
        universal_newlines=True
    )

    rc = None
    with open(log_path, "w", encoding="utf-8") as f:
        killer = None
        try:
            effective_timeout = timeout or 0
            _timeout_cfg = {
                "Proyecto_AES_MMS.py":       ("MMS_REPS",       "20", "MMS_INTERVAL",       "60", 120),
                "Proyecto_AES_Youtube.py":    ("YT_REPS",        "10", "YT_INTERVAL",        "60",  60),
                "Proyecto_AES_Internet.py":   ("INTERNET_REPS",  "10", "INTERNET_INTERVAL",  "60",  60),
                "Proyecto_AES_Messenger.py":  ("MESSENGER_REPS", "20", "MESSENGER_INTERVAL", "60",  60),
                "Proyecto_AES_Twitter.py":    ("TWITTER_REPS",   "20", "TWITTER_INTERVAL",   "60",  60),
                "Proyecto_AES_Gmail.py":      ("GMAIL_REPS",     "20", "GMAIL_INTERVAL",     "60",  60),
            }
            try:
                cfg = _timeout_cfg.get(path.name)
                if cfg:
                    reps_key, reps_def, iv_key, iv_def, margin = cfg
                    reps = int(os.environ.get(reps_key, reps_def))
                    interval = int(os.environ.get(iv_key, iv_def))
                    extra = interval if path.name == "Proyecto_AES_Youtube.py" else 0
                    est = reps * interval + extra + margin + 30
                    if est > effective_timeout:
                        effective_timeout = est
                        print(f"[runner] raising timeout for {path.name} to {effective_timeout}s")
            except Exception:
                pass

            killer = None
            if effective_timeout:
                def kill_proc():
                    try:
                        proc.kill()
                        print(f"[runner] timeout: killed {path.name}")
                    except Exception:
                        pass
                killer = threading.Timer(effective_timeout, kill_proc)
                killer.daemon = True
                killer.start()

            while True:
                line = proc.stdout.readline()
                if line:
                    print(line, end=""); f.write(line); f.flush()
                    try:
                        detect_and_respond(line, proc.stdin, email, phone, userx, userf)
                    except Exception:
                        pass
                elif proc.poll() is not None:
                    rem = proc.stdout.read()
                    if rem:
                        print(rem, end=""); f.write(rem)
                    break
        except KeyboardInterrupt:
            print("Interrupted by user; terminating child...")
            try: proc.terminate()
            except: pass
            proc.wait()
        finally:
            if killer:
                try: killer.cancel()
                except: pass
            try:
                rc = proc.returncode if proc.returncode is not None else proc.wait(timeout=1)
            except Exception:
                rc = proc.returncode if proc.returncode is not None else 1

    return rc, str(log_path)



def main():
    parser = argparse.ArgumentParser(description="Run all Proyecto AES scripts sequentially")
    parser.add_argument("--email", help="email for scripts")
    parser.add_argument("--phone", help="phone for scripts")
    parser.add_argument("--userx", help="Twitter/X username to provide to scripts")
    parser.add_argument("--userf", help="Facebook/Messenger username to provide to scripts")
    parser.add_argument("--mms-reps",       type=int, default=int(os.environ.get("MMS_REPS",       DEFAULTS["MMS_REPS"])),       help=f"MMS repetitions (default {DEFAULTS['MMS_REPS']})")
    parser.add_argument("--mms-interval",   type=int, default=int(os.environ.get("MMS_INTERVAL",   DEFAULTS["MMS_INTERVAL"])),   help=f"MMS interval seconds (default {DEFAULTS['MMS_INTERVAL']})")
    parser.add_argument("--internet-reps",  type=int, default=int(os.environ.get("INTERNET_REPS",  DEFAULTS["INTERNET_REPS"])),  help=f"Internet repetitions (default {DEFAULTS['INTERNET_REPS']})")
    parser.add_argument("--yt-reps",        type=int, default=int(os.environ.get("YT_REPS",        DEFAULTS["YT_REPS"])),        help=f"YouTube repetitions (default {DEFAULTS['YT_REPS']})")
    parser.add_argument("--gmail-reps",     type=int, default=int(os.environ.get("GMAIL_REPS",     DEFAULTS["GMAIL_REPS"])),     help=f"Gmail repetitions (default {DEFAULTS['GMAIL_REPS']})")
    parser.add_argument("--twitter-reps",   type=int, default=int(os.environ.get("TWITTER_REPS",   DEFAULTS["TWITTER_REPS"])),   help=f"Twitter repetitions (default {DEFAULTS['TWITTER_REPS']})")
    parser.add_argument("--messenger-reps", type=int, default=int(os.environ.get("MESSENGER_REPS", DEFAULTS["MESSENGER_REPS"])), help=f"Messenger repetitions (default {DEFAULTS['MESSENGER_REPS']})")
    parser.add_argument("--timeout",        type=int, default=7200,                                        help="per-script timeout seconds (default 7200)")
    parser.add_argument("--continue-on-error", action="store_true", help="continue even if a script fails")
    ns = parser.parse_args()

    os.environ["MMS_REPS"]       = str(ns.mms_reps)
    os.environ["MMS_INTERVAL"]   = str(ns.mms_interval)
    os.environ["INTERNET_REPS"]  = str(ns.internet_reps)
    os.environ["YT_REPS"]        = str(ns.yt_reps)
    os.environ["GMAIL_REPS"]     = str(ns.gmail_reps)
    os.environ["TWITTER_REPS"]   = str(ns.twitter_reps)
    os.environ["MESSENGER_REPS"] = str(ns.messenger_reps)

    email = ns.email or os.environ.get("AES_EMAIL")
    phone = ns.phone or os.environ.get("AES_PHONE")
    userx = ns.userx or os.environ.get("AES_USERX")
    userf = ns.userf or os.environ.get("AES_USERF")

    try:
        if (not email) and sys.stdin and sys.stdin.isatty():
            email = input("Email to use for scripts (leave blank to skip): ").strip() or None
        if (not phone) and sys.stdin and sys.stdin.isatty():
            phone = input("Phone number to use for scripts (leave blank to skip): ").strip() or None
        if (not userx) and sys.stdin and sys.stdin.isatty():
            userx = input("Twitter/X username to use for scripts (leave blank to skip): ").strip() or None
        if (not userf) and sys.stdin and sys.stdin.isatty():
            userf = input("Facebook/Messenger username to use for scripts (leave blank to skip): ").strip() or None
    except Exception:
        pass

    print("====================================")
    print(" AES Test Suite - Start")
    print(f" Start time: {datetime.now()}")
    print("====================================\n")

    scripts = list_scripts()
    if not scripts:
        print("No scripts found. Exiting.")
        return 1

    for s in scripts:
        rc, log = run_script(s, email, phone, userx, userf, ns.timeout)
        if rc != 0:
            print(f"Error in {s.name} (rc={rc}) - log: {log}")
            try:
                log_path_obj = Path(log)
                if log_path_obj.exists():
                    print("--- Log tail (last 200 lines) ---")
                    with open(log_path_obj, "r", encoding="utf-8", errors="ignore") as lf:
                        for line in deque(lf, maxlen=200):
                            print(line, end="")
                    print("--- End log tail ---\n")
                else:
                    print(f"Log file not found: {log}")
            except Exception as e:
                print(f"Could not read log file: {e}")

            cleanup_device()
            if not ns.continue_on_error:
                print("Suite stopped")
                return rc
            else:
                print("Continuing despite error")
        else:
            print(f"{s.name} completed -> {log}\n")
            cleanup_device()
            time.sleep(1)

    print("====================================")
    print(f" End time: {datetime.now()}")
    print("====================================")
    return 0



if __name__ == "__main__":
    rc = main()
    try:
        input("\nPress Enter to close...")
    except Exception:
        pass
    sys.exit(rc)
