import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def search_youtube_video(driver, query, max_results=1):
    """
    Cari video di YouTube berdasarkan query dan ambil URL-nya.
    """
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3)

    video_links = []
    elems = driver.find_elements(By.XPATH, '//a[@id="video-title"]')
    for e in elems[:max_results]:
        href = e.get_attribute("href")
        if href and "watch" in href:
            video_links.append(href)

    return video_links


def scrape_youtube_comments(driver, video_url, max_comments=50, max_replies=0):
    """
    Scrape komentar (dan optionally replies) dari sebuah video YouTube.
    Args:
        driver: selenium webdriver
        video_url (str): link video YouTube
        max_comments (int): batas jumlah komentar
        max_replies (int): jumlah reply per komentar (0 = skip replies)
    Returns:
        list of dict
    """
    comments = []
    scraped_at = datetime.datetime.utcnow().isoformat()  # waktu scraping (UTC)

    driver.get(video_url)
    time.sleep(4)  # tunggu halaman load

    # Scroll agar komentar muncul
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while len(comments) < max_comments:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        # Ambil komentar utama
        comment_elems = driver.find_elements(By.CSS_SELECTOR, "#content #content-text")
        time_elems = driver.find_elements(By.CSS_SELECTOR, "#header-author time")

        for idx, c in enumerate(comment_elems[len(comments):max_comments]):
            text = c.text.strip()
            if text:
                # ambil waktu publish kalau ada
                published_time = None
                if idx < len(time_elems):
                    try:
                        published_time = time_elems[idx].get_attribute("aria-label")
                    except:
                        published_time = None

                comments.append({
                    "platform": "youtube",
                    "url": video_url,
                    "text": text,
                    "lang": "und",
                    "type": "comment",
                    "scraped_at": scraped_at,
                    "published_time": published_time
                })

        if len(comments) >= max_comments:
            break

    # Opsional: scraping replies
    if max_replies > 0:
        try:
            reply_buttons = driver.find_elements(By.CSS_SELECTOR, "ytd-button-renderer#more-replies button")
            for btn in reply_buttons[:max_comments]:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1.5)
                except:
                    continue

            reply_elems = driver.find_elements(By.CSS_SELECTOR, "ytd-comment-replies-renderer #content #content-text")
            reply_times = driver.find_elements(By.CSS_SELECTOR, "ytd-comment-replies-renderer #header-author time")

            count = 0
            for idx, r in enumerate(reply_elems):
                if count >= max_replies:
                    break
                txt = r.text.strip()
                if txt:
                    published_time = None
                    if idx < len(reply_times):
                        try:
                            published_time = reply_times[idx].get_attribute("aria-label")
                        except:
                            published_time = None

                    comments.append({
                        "platform": "youtube",
                        "url": video_url,
                        "text": txt,
                        "lang": "und",
                        "type": "reply",
                        "scraped_at": scraped_at,
                        "published_time": published_time
                    })
                    count += 1
        except Exception as e:
            print(f"⚠️ Gagal ambil replies: {e}")

    return comments
