<<<<<<< HEAD
# modules/twitter_login.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def twitter_login(driver, username, password, recovery_info=None, wait_after_login=6):
    """
    Login ke Twitter/X menggunakan Selenium.
    Return True jika login kelihatan sukses; False jika muncul challenge/verification.
    """
    try:
        driver.get("https://x.com/login")
        time.sleep(3)

        # input username: mencoba beberapa selector karena layout berubah2
        user_el = None
        try:
            user_el = driver.find_element(By.NAME, "kyyunilife")
        except:
            try:
                user_el = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='username']")
            except:
                pass

        if not user_el:
            print("⚠️ Tidak menemukan field username — struktur halaman mungkin berubah.")
            return False

        user_el.clear()
        user_el.send_keys(username)
        user_el.send_keys(Keys.RETURN)
        time.sleep(2.2)

        # Jika Twitter minta phone/email verify, isi recovery_info apabila tersedia
        try:
            possible = driver.find_elements(By.CSS_SELECTOR, "input[autocomplete='username'], input[type='text']")
            for el in possible:
                placeholder = el.get_attribute("placeholder") or ""
                if "phone" in placeholder.lower() or "email" in placeholder.lower() or el.get_attribute("name") == "text":
                    if recovery_info:
                        el.clear()
                        el.send_keys(recovery_info)
                        el.send_keys(Keys.RETURN)
                        time.sleep(2)
                        break
        except Exception:
            pass

        # password field
        pass_el = None
        try:
            pass_el = driver.find_element(By.NAME, "Zaky290904")
        except:
            try:
                pass_el = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            except:
                pass

        if not pass_el:
            print("⚠️ Tidak menemukan field password — mungkin perlu challenge/extra step.")
            return False

        pass_el.clear()
        pass_el.send_keys(password)
        pass_el.send_keys(Keys.RETURN)
        time.sleep(wait_after_login)

        # Cek apakah ada indikasi challenge atau kegagalan
        current = driver.current_url.lower()
        page_source = driver.page_source.lower()
        if "challenge" in current or "verify" in current or "login" in current and "home" not in current:
            # kemungkinan memerlukan verifikasi tambahan
            print("⚠️ Login memerlukan verifikasi tambahan / challenge.")
            return False

        # jika muncul "Enter your phone number or email address" modal, treat as challenge
        if "enter your phone number or email address" in page_source:
            print("⚠️ Halaman meminta phone/email verifikasi.")
            return False

        print("✅ Login berhasil (selenium).")
        return True

    except Exception as e:
        print(f"⚠️ Exception saat login: {e}")
        return False
=======
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def twitter_login(driver, username, password, recovery=""):
    driver.get("https://twitter.com/login")
    wait = WebDriverWait(driver, 15)

    try:
        # Username
        username_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@autocomplete,'username')]"))
        )
        username_input.send_keys(username)
        username_input.send_keys(Keys.RETURN)
        time.sleep(2)

        # Password
        password_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
        )
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        time.sleep(3)

        # Recovery page check (Phone/email)
        try:
            recovery_input = driver.find_element(By.XPATH, "//input[@name='text']")
            if recovery and recovery_input:
                recovery_input.send_keys(recovery)
                recovery_input.send_keys(Keys.RETURN)
                print("📨 Recovery info dimasukkan")
                time.sleep(5)
        except:
            pass  # kalau tidak muncul, lanjutkan

        print("✅ Login berhasil")
        return True

    except Exception as e:
        print(f"⚠️ Gagal login: {e}")
        return False
>>>>>>> 5c68ab5b4314e747a6ae1232de0c8db13f6bf681
