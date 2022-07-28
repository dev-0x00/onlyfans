

import queue
import time

import chromedriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec

from selenium.common.exceptions import TimeoutException

class Onlyfans():

    def __init__(self) -> None:
        self.driver = chromedriver.get_chromedriver(use_proxy=True) 
    
    def Login(self, username, password):
        self.driver.get("https://onlyfans.com/")
        WebDriverWait(self.driver, 120).until(Ec.presence_of_element_located((
            By.ID, "input-20"
        ))).send_keys(username)
        WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
            By.ID, "input-23"
        ))).send_keys(password)
        WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
            By.CLASS_NAME, "g-btn.m-rounded.m-block.m-lg.mb-0"
        ))).click()
        print("[*] Loading login: ")
        WebDriverWait(self.driver, 120).until(Ec.presence_of_element_located((
            By.XPATH, "/html/body/div/div[2]/main/div[1]/div/div/div/div[1]/a"
        )))

    def LoadUsers(self) :
        self.driver.get("https://onlyfans.com/my/subscribers/expired")
        print("[*] Logged in, Fetching expired subs:  ")
        screen_height = self.driver.execute_script("return window.screen.height;")
        x = 1
        while True:

            try:
                print(f"[*] Loading page {x}")
                self.driver.execute_script("window.scrollTo(0, {screen_height}*{x});".format(screen_height=screen_height, x=x))  
                x += 1
                time.sleep(1)
                scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
                
                if x == 250:
                    break

            except:
                if x == 250:
                    break
                elif x < 250:
                    x += 1
                else:
                    break

        users = WebDriverWait(self.driver, 20).until(Ec.presence_of_all_elements_located((
                        By.CLASS_NAME, "b-users__item.m-fans"
                    )))

        for user in users:
            username = user.find_elements(
                By.TAG_NAME, "a"
            )[0].get_attribute("href")
            with open("fans.txt", "a") as fi:
                fi.write(username + "\n")


    def Subscriber(self, queue):
        self.driver.execute_script("window.open('');")
        # Switch to the new window and open new URL
        self.driver.switch_to.window(self.driver.window_handles[1])
        while not queue.empty():
            self.driver.get(queue.get())
            try:
                status = WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
                            By.CLASS_NAME, "b-btn-text"
                        ))).get_attribute("innerHTML")

                if status == "subscribed":
                    username = self.driver.current_url.split("/")[-1:]
                    print(f"[*] User {username} already subscribed: ")
                    pass

                else:
                    subscribe = WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
                        By.CLASS_NAME, "m-rounded.m-flex.m-space-between.m-lg.g-btn"
                    )))
                    self.driver.execute_script("arguments[0].click();", subscribe)
                    username = self.driver.current_url.split("/")[-1:]
                    print(f"[*] Subscribed to {username}")

                    WebDriverWait(self.driver, 20).until(Ec.presence_of_all_elements_located((
                        By.CLASS_NAME, "g-page__header__btn.m-with-round-hover"
                    )))

            except TimeoutException:
                pass

        queue.join()

def main():
    holder = queue.Queue()
    fans = Onlyfans()
    username = input("[*] Enter Username: "
    )
    password = input("[*] Enter password: ")
    fans.Login(username, password)
    fans.LoadUsers()
    with open("fans.txt", "r") as fi:
        for user in fi.readlines():
            holder.put(user)
    fans.Subscriber(holder)
    
    
if __name__ == "__main__":
    main()