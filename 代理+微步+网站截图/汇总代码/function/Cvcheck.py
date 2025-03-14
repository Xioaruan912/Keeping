import time
from threading import Thread

import cv2
from selenium.webdriver import ActionChains


##########################################  模拟人为查找 #############################################
def get_track(distance):
    """
    生成模拟人为拖动的轨迹。
    :param distance: 需要拖动的总距离
    :return: 拖动的轨迹列表
    """
    track = []
    current = 0
    while current < distance:
        move = min(10, distance - current)  # 每次移动的最大步长为 10
        track.append(move)
        current += move
    return track

############################################ 处理图像并对比坑位 ############################################
def process_image(qk, hk):
    """
    处理图像并对比坑位，返回匹配结果。
    :param qk: 缺口图片路径
    :param hk: 滑块图片路径
    :return: 匹配结果的最小值和最大值
    """
    # 读取图像并转换为灰度图
    hk_img_01 = cv2.imread(f"{hk}", 0)
    qk_img_01 = cv2.imread(f"{qk}", 0)
    # 使用模板匹配算法计算相似度
    late = cv2.matchTemplate(qk_img_01, hk_img_01, cv2.TM_CCOEFF_NORMED)
    # 获取匹配结果的最小值和最大值
    loc = cv2.minMaxLoc(late)
    return loc

########################################### 拖拽实现 #############################################
def drag_slider(driver, hk_box, x):
    """
    模拟人为拖动滑块。
    :param driver: Selenium WebDriver 对象
    :param hk_box: 滑块元素
    :param x: 需要拖动的距离
    """
    action = ActionChains(driver)
    tracks = get_track(x)  # 生成拖动的轨迹
    action.click_and_hold(hk_box).perform()  # 点击并按住滑块
    for i in tracks:
        action.move_by_offset(i, 0).perform()  # 按照轨迹移动滑块
    action.release().perform()  # 释放滑块

########################################### 流程实现 #############################################
def img_attack(qk, hk, driver, hk_box):
    """
    图像攻击流程实现。
    :param qk: 缺口图片路径
    :param hk: 滑块图片路径
    :param driver: Selenium WebDriver 对象
    :param hk_box: 滑块元素
    """
    # 使用多线程并行处理图像
    image_thread = Thread(target=process_image, args=(qk, hk))
    image_thread.start()
    image_thread.join()

    # 获取匹配结果
    loc = process_image(qk, hk)
    x = int(loc[2][0] * 49 / 50)  # 计算需要拖动的距离

    # 模拟人为拖动滑块
    drag_slider(driver, hk_box, x)
    time.sleep(1)  # 等待 1 秒