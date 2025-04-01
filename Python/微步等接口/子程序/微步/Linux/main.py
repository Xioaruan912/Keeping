from flask import Flask, request, jsonify

from function.main_request import search_req, get_auth
from function.openChrome import openChrome
from loguru import logger
from function.main_request import bypass
import time

from loguru import logger
from function.main_request import bypass
from function.main_request import search_req, get_auth
from function.openChrome import openChrome





app = Flask(__name__)

@app.route('/search', methods=['POST'])
def run_script():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    search_url = data.get('search_url')

    if not username or not password or not search_url:
        return jsonify({"error": "Missing username, password, or search_url"}), 400

    try:
        start_time = time.time()
        driver = openChrome(username, password)
        bypass(driver, "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[1]", "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[2]", "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[1]")
        search_req(driver, search_url)
        x_csrf_token,xx_csrf,cookie = get_auth(driver)
        driver.quit()
        end_time = time.time()
        elapsed_time = end_time - start_time
        logger.info(f"脚本执行时间: {elapsed_time:.2f} 秒")
        return jsonify({
            "message": "1",
            "time": f"{elapsed_time:.2f} s",
            "x-csrf-token": x_csrf_token,
            "xx-csrf": xx_csrf,
            "cookie": cookie
        }), 200
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.config['JSON_SORT_KEYS'] = False  #禁止排序
    app.run(host='0.0.0.0', port=5000)



# username = "x"
# password = "x"
# search_url = "baidu.com"
#
# if __name__ == '__main__':
#     start_time = time.time()
#     driver = openChrome(username, password)
#     bypass(driver, "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[1]",
#            "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[2]",
#            "/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div[1]/div[1]")
#     search_req(driver, search_url)
#     x_csrf_token, xx_csrf, cookie = get_auth(driver)
#     logger.success("xx_csrf:" + xx_csrf)
#     logger.success("x_csrf_token:" + x_csrf_token)
#     logger.success("cookie:" + cookie)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     logger.info(f"脚本执行时间: {elapsed_time:.2f} 秒")
#     # 等待用户输入
#     input("按 Enter 键退出...")
#     driver.quit()