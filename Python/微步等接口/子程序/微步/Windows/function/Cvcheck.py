import time

import cv2
from selenium.webdriver import ActionChains


#模拟人为查找
def get_track(distance):
    track = []
    current = 0
    while current < distance:
        move = min(10, distance - current)  # 每次移动的最大步长为 10
        track.append(move)
        current += move
    return track



# 处理cv 和对比坑位
from threading import Thread

def process_image(qk, hk):
    hk_img_01 = cv2.imread(f"{hk}", 0)
    qk_img_01 = cv2.imread(f"{qk}", 0)
    late = cv2.matchTemplate(qk_img_01, hk_img_01, cv2.TM_CCOEFF_NORMED)
    loc = cv2.minMaxLoc(late)
    return loc

def drag_slider(driver, hk_box, x):
    action = ActionChains(driver)
    tracks = get_track(x)
    action.click_and_hold(hk_box).perform()
    for i in tracks:
        action.move_by_offset(i, 0).perform()
    action.release().perform()

def img_attack(qk, hk, driver, hk_box):
    # 使用多线程并行处理
    image_thread = Thread(target=process_image, args=(qk, hk))
    image_thread.start()
    image_thread.join()

    loc = process_image(qk, hk)
    x = int(loc[2][0] * 49 / 50)

    drag_slider(driver, hk_box, x)
    time.sleep(1)