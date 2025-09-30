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
