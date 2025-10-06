import time
import csv
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from langdetect import detect
from config import SCROLL_PAUSE, MAX_SCROLLS, BATCH_SAVE_EVERY, RESULTS_FILE

def _safe_detect_lang(text):
    if not text or text.strip() == "":
        return "und"
    try:
        return detect(text)
    except Exception:
        return "und"

def _save_batch(items, filename=RESULTS_FILE, mode="w"):
    if not items:
        return
    fieldnames = list(items[0].keys())
    with open(filename, mode, newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if mode == "w":
            writer.writeheader()
        writer.writerows(items)

def scroll_once(driver, pause=SCROLL_PAUSE):
    try:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    except Exception:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception:
            pass
    time.sleep(pause)

def scrape_twitter_search(driver, query, max_tweets=200, allowed_langs=None):
    """
    Crawl search results (live).
    Return: [{text, lang, timestamp, url, source}]
    """
    results = []
    seen_texts = set()

    search_url = f"https://x.com/search?q={query}&src=typed_query&f=live"
    driver.get(search_url)
    time.sleep(3.0)

    scrolls = 0
    last_len = 0

    while len(results) < max_tweets and scrolls < MAX_SCROLLS:
        try:
            if "something went wrong" in driver.page_source.lower():
                print("⚠️ Twitter returned 'Something went wrong' — stopping.")
                break
        except Exception:
            pass

        cards = driver.find_elements(By.XPATH, '//article[@role="article"]')
        for card in cards:
            try:
                txt_el = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                text = txt_el.text.strip()
                if not text or text in seen_texts:
                    continue

                # ambil waktu & url
                try:
                    time_el = card.find_element(By.XPATH, './/time')
                    timestamp = time_el.get_attribute("datetime") or datetime.utcnow().isoformat()
                    parent = time_el.find_element(By.XPATH, "..")
                    url = parent.get_attribute("href") or ""
                except Exception:
                    timestamp = datetime.utcnow().isoformat()
                    url = ""

                lang = _safe_detect_lang(text)
                if allowed_langs and lang not in allowed_langs:
                    seen_texts.add(text)
                    continue

                item = {
                    "text": text,
                    "lang": lang,
                    "timestamp": timestamp,   # 🔹 ganti dari 'date'
                    "url": url,
                    "source": "twitter"
                }
                results.append(item)
                seen_texts.add(text)

                if len(results) % BATCH_SAVE_EVERY == 0:
                    print(f"🔖 Auto-saving batch: {len(results)} items so far.")
                    _save_batch(results, filename=RESULTS_FILE, mode="w")

            except (NoSuchElementException, StaleElementReferenceException):
                continue
            except Exception:
                continue

            if len(results) >= max_tweets:
                break

        if len(results) == last_len:
            scrolls += 1
        else:
            last_len = len(results)

        try:
            scroll_once(driver)
        except WebDriverException:
            print("⚠️ WebDriver error during scroll — stopping.")
            break

    if results:
        _save_batch(results, filename=RESULTS_FILE, mode="w")
    print(f"✅ Finished scraping search: collected {len(results)} tweets.")
    return results


def scrape_replies_for_tweet(driver, tweet_url, max_replies=5, allowed_langs=None):
    """
    Crawl replies for a given tweet.
    Return: [{text, lang, timestamp, url, source}]
    """
    replies = []
    if not tweet_url:
        return replies

    try:
        driver.get(tweet_url)
    except Exception:
        return replies

    time.sleep(2.5)

    collected = 0
    seen = set()
    scroll_limit = 30

    while collected < max_replies and scroll_limit > 0:
        if "something went wrong" in driver.page_source.lower():
            print("⚠️ Twitter 'Something went wrong' inside tweet page — stop replies fetch.")
            break

        cards = driver.find_elements(By.XPATH, '//article[@role="article"]')
        for card in cards:
            if collected >= max_replies:
                break
            try:
                try:
                    time_el = card.find_element(By.XPATH, './/time')
                    card_url = time_el.find_element(By.XPATH, "..").get_attribute("href")
                    timestamp = time_el.get_attribute("datetime") or datetime.utcnow().isoformat()
                except Exception:
                    card_url = ""
                    timestamp = datetime.utcnow().isoformat()

                if card_url == tweet_url:
                    continue

                try:
                    txt_el = card.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                    text = txt_el.text.strip()
                except Exception:
                    text = ""

                if not text or text in seen:
                    continue

                lang = _safe_detect_lang(text)
                if allowed_langs and lang not in allowed_langs:
                    seen.add(text)
                    continue

                replies.append({
                    "text": text,
                    "lang": lang,
                    "timestamp": timestamp,  # 🔹 ganti dari 'date'
                    "url": card_url,
                    "source": "twitter_reply"
                })

                seen.add(text)
                collected += 1

            except Exception:
                continue

        scroll_once(driver)
        scroll_limit -= 1

    print(f"  - Collected {len(replies)} replies for {tweet_url}")
    return replies
