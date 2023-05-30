import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import time
import os
import requests
from urllib.parse import urlparse
import io
from PIL import Image


class googleImageScraper():
    def __init__(self, image_path, search_key="pigeon", number_of_images=1, headless=True, min_resolution=(0, 0), max_resolution=(1920, 1080), max_missed=10):
        # check parameter types
        image_path = os.path.join(image_path, search_key)
        if (type(number_of_images) != int):
            print("[Error] Number of images must be integer value.")
            return
        if not os.path.exists(image_path):
            print("[INFO] Image path not found. Creating a new folder.")
            os.makedirs(image_path)

        # initialize the webdriver
        ffoptions = Options()
        if headless:
            ffoptions.add_argument('-headless')
        driver = webdriver.Firefox(options=ffoptions)
        try:
            driver.get("https://www.google.com/")
        except Exception as e:
            print('in init, except e: ', e)

        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.image_path = image_path
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947" % (
            search_key)
        self.headless = headless
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.max_missed = max_missed


    def find_image_urls(self):
        """
            This function search and return a list of image urls based on the search key.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls = google_image_scraper.find_image_urls()

        """
        print("[INFO] Gathering image links")
        print("url is:", self.url)
        self.driver.get(self.url)
        image_urls = []
        count = 0
        missed_count = 0
        indx_1 = 0
        indx_2 = 0
        search_string = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'
        print("search_string is: ", search_string)

        # accept cookies
        consent_screen = WebDriverWait(self.driver, 5).until(
            lambda driver: driver.find_element(by=By.XPATH, value="/html/body/c-wiz"))
        consent_screen.find_elements(
            by=By.TAG_NAME, value="button")[1].click()

        # while loop to download images
        while self.number_of_images > count and missed_count < self.max_missed:
            if indx_2 > 0:
                try:
                    imgurl = self.driver.find_element(
                        By.XPATH, search_string % (indx_1, indx_2+1))
                    imgurl.click()
                    indx_2 = indx_2 + 1
                    missed_count = 0
                except Exception:
                    try:
                        imgurl = self.driver.find_element(
                            By.XPATH, search_string % (indx_1+1, 1))
                        imgurl.click()
                        indx_2 = 1
                        indx_1 = indx_1 + 1
                    except:
                        indx_2 = indx_2 + 1
                        missed_count = missed_count + 1
            else:
                try:
                    imgurl = self.driver.find_element(
                        By.XPATH, search_string % (indx_1+1))
                    imgurl.click()
                    missed_count = 0
                    indx_1 = indx_1 + 1
                except Exception:
                    try:
                        imgurl = self.driver.find_element(
                            By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img' % (indx_1, indx_2+1))
                        imgurl.click()
                        missed_count = 0
                        indx_2 = indx_2 + 1
                        search_string = '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                    except Exception:
                        indx_1 = indx_1 + 1
                        missed_count = missed_count + 1

            try:
                # select image from the popup
                WebDriverWait(self.driver, 1).until(
                    lambda driver: driver.find_element(by=By.ID, value="islsp"))
                class_names = ["n3VNCb", "iPVvYb", "r48jcc", "pT0Scc"]
                images = [self.driver.find_elements(By.CLASS_NAME, class_name) for class_name in class_names if len(
                    self.driver.find_elements(By.CLASS_NAME, class_name)) != 0][0]
                for image in images:
                    # only download images that starts with http
                    src_link = image.get_attribute("src")
                    if (("http" in src_link) and (not "encrypted" in src_link)):
                        print(
                            f"[INFO] {self.search_key} \t #{count} \t {src_link}")
                        image_urls.append(src_link)
                        count += 1
                        break
            except Exception:
                print("[INFO] Unable to get link")

            try:
                # scroll page to load next image
                if (count % 3 == 0):
                    self.driver.execute_script(
                        "window.scrollTo(0, "+str(indx_1*60)+");")
                element = self.driver.find_element(By.CLASS_NAME, "mye4qd")
                element.click()
                print("[INFO] Loading next page")
                time.sleep(3)
            except Exception:
                time.sleep(1)

        self.driver.quit()
        print("[INFO] Google search ended")
        return image_urls


    def save_images(self, image_urls, keep_filenames):
        """
            This function takes in an array of image urls and save it into the given image path/directory.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls=["https://example_1.jpg","https://example_2.jpg"]
                google_image_scraper.save_images(image_urls)

        """
        print("[INFO] Saving image, please wait...")
        for indx, image_url in enumerate(image_urls):
            try:
                print("[INFO] Image url:%s" % (image_url))
                search_string = ''.join(
                    e for e in self.search_key if e.isalnum())
                image = requests.get(image_url, timeout=5)
                if image.status_code != 200:
                    return
                with Image.open(io.BytesIO(image.content)) as image_from_web:
                    try:
                        if (keep_filenames):
                            # extact filename without extension from URL
                            o = urlparse(image_url)
                            image_url = o.scheme + "://" + o.netloc + o.path
                            name = os.path.splitext(
                                os.path.basename(image_url))[0]
                            # join filename and extension
                            filename = "%s.%s" % (
                                name, image_from_web.format.lower())
                        else:
                            filename = "%s%s.%s" % (search_string, str(
                                indx), image_from_web.format.lower())

                        image_path = os.path.join(
                            self.image_path, filename)
                        print(
                            f"[INFO] {self.search_key} \t {indx} \t Image saved at: {image_path}")
                        image_from_web.save(image_path)
                    except OSError:
                        rgb_im = image_from_web.convert('RGB')
                        rgb_im.save(image_path)
                    image_resolution = image_from_web.size
                    if image_resolution != None:
                        if image_resolution[0] < self.min_resolution[0] or image_resolution[1] < self.min_resolution[1] or image_resolution[0] > self.max_resolution[0] or image_resolution[1] > self.max_resolution[1]:
                            image_from_web.close()
                            os.remove(image_path)

                    image_from_web.close()
            except Exception as e:
                print("[ERROR] Download failed: ", e)
                pass
        print("--------------------------------------------------")
        print("[INFO] Downloads completed. Please note that some photos were not downloaded as they were not in the correct format (e.g. jpg, jpeg, png)")


if __name__ == '__main__':
    google_image_scraper = googleImageScraper(
        "scrappedImages", "rock%20pigeon", 10, max_missed=3)
    image_urls = google_image_scraper.find_image_urls()
    google_image_scraper.save_images(image_urls, False)
