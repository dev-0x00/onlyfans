import chromedriver

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec

from selenium.common.exceptions import TimeoutException

class Onlyfans():

    def __init__(self) -> None:
        self.driver = chromedriver.get_chromedriver(use_proxy=True) 
    
    def Login(self, username, password):
        self.driver.get("https://onlyfans.com/")
        WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
            By.ID, "input-20"
        ))).send_keys(username)
        WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
            By.ID, "input-23"
        ))).send_keys(password)
        WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
            By.CLASS_NAME, "g-btn.m-rounded.m-block.m-lg.mb-0"
        ))).click()
        time.sleep(15)
        try:
            self.Subscribe()

        except:
            time.sleep(10)
            self.Subscribe()

    def Subscribe(self):
     
        self.driver.get("https://onlyfans.com/my/subscribers/expired")
        print("[*] Logged in, Fetching expired subs:  ")

        """expusers = WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
            By.XPATH, "
            /html/body/div/div[2]/main/div[1]/div/div[3]/div/div/div[3]/a
            "
        ))).get_attribute("innerHTML")
        print(expusers)"""
        users = 6213

        for i in range(1, int(users)):
            print(f"[*] Fetched user {i}")
            try:
                user = WebDriverWait(self.driver, 10).until(Ec.presence_of_element_located((
                By.XPATH, f"""
                /html/body/div/div[2]/main/div[1]/div/div[5]/div[1]/div[1]/div[{i}]/div/div[1]/div[1]/a
                """
                )))
                self.driver.execute_script("arguments[0].click();", user)

            except TimeoutException:
                try:
                    x = 1
                    screen_height = self.driver.execute_script("return window.screen.height;")
                    while True:
                        self.driver.execute_script("window.scrollTo(0, {screen_height}*{x});".format(screen_height=screen_height, x=x))  
                        x += 1
                        time.sleep(2)
                        scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
                        
                        if x == 5:
                            break

                    user = WebDriverWait(self.driver, 10).until(Ec.presence_of_element_located((
                    By.XPATH, f"""
                    /html/body/div/div[2]/main/div[1]/div/div[5]/div[1]/div[1]/div[{i}]/div/div[1]/div[1]/a
                    """
                    )))
                    self.driver.execute_script("arguments[0].click();", user)
                
                except Exception as Except:
                    print(f"[-] {Except}")
                    pass
    

            WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
                By.XPATH, f"""
                /html/body/div/div[2]/main/div[1]/div[1]/div[2]/div/div[3]/div/div/div[2]/div
                """
            ))).click()
            time.sleep(5)

            backBtn = WebDriverWait(self.driver, 20).until(Ec.presence_of_element_located((
                By.XPATH, f"""
                /html/body/div/div[2]/main/div[1]/div[1]/div[1]/div[2]/button
                """
            )))
            self.driver.execute_script("arguments[0].click();", backBtn)

        


def main():
    fans = Onlyfans()
    fans.Login("Loridaaof@gmail.com", "Asperin1133")


if __name__ == "__main__":
    main()