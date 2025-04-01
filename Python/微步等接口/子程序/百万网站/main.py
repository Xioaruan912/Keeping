import csv
import psycopg2
import requests
from tqdm import tqdm
import time

# 数据库连接信息
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'zq',
    'user': 'postgres',
    'password': '123456'
}

# 请替换为你的实际 API Token
API_TOKEN = "-Bavd6a6T6YVzvYpmYoSlbPXaT30qpDstF3kJEX8"

# 定义请求头
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# 错误时的等待时间（单位：秒），设置为 5 分钟即 300 秒
error_wait_time = 300
# 正常循环间隔时间为 7 天（单位：秒）
# loop_interval = 7 * 24 * 60 * 60
loop_interval = 7 * 24 * 60 * 60

# 第一步：获取所有排名桶数据集
def get_ranking_bucket_datasets():
    url = "https://api.cloudflare.com/client/v4/radar/datasets?limit=10&datasetType=RANKING_BUCKET"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                return data["result"]["datasets"]
    except requests.RequestException as e:
        print(f"获取排名桶数据集时出现网络错误: {e}")
    return []

# 第二步：找到前一百万排名的数据集 ID
def find_top_one_million_dataset_id(datasets):
    for dataset in datasets:
        if dataset["meta"].get("top") == 1000000:
            return dataset["id"]
    return None

# 第三步：获取数据集的下载 URL
def get_dataset_download_url(dataset_id):
    url = "https://api.cloudflare.com/client/v4/radar/datasets/download"
    headers["Content-Type"] = "application/json"
    data = {
        "datasetId": dataset_id
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                return data["result"]["dataset"]["url"]
    except requests.RequestException as e:
        print(f"获取数据集下载 URL 时出现网络错误: {e}")
    return None

# 第四步：下载数据集并保存为 CSV 格式文件
def download_dataset(url):
    try:
        print("开始下载数据集...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        temp_filename = "temp_dataset.txt"
        with open(temp_filename, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

        if total_size != 0 and progress_bar.n != total_size:
            print("下载未完成，可能网络出现问题。")
            return False

        print("下载完成，开始转换为 CSV 格式...")
        with open(temp_filename, 'r', encoding='utf-8') as infile, \
                open("top_one_million_domains.csv", 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            first_line = True
            for line in infile:
                if first_line:
                    # 处理第一行，可能是标题行
                    writer.writerow([line.strip()])
                    first_line = False
                else:
                    # 处理后续行
                    writer.writerow([line.strip()])

        print("数据集已成功保存为 top_one_million_domains.csv")
        return True
    except requests.RequestException as e:
        print(f"下载过程中出现网络错误: {e}")
        return False
    except Exception as e:
        print(f"下载或保存文件时出现错误: {e}")
        return False

# 创建用于存储域名的表
def create_table(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS domains (
                    id INT,
                    domain_name VARCHAR(255) NOT NULL
                )
            """)
        connection.commit()
        print("表创建成功")
    except (Exception, psycopg2.Error) as error:
        print(f"创建表时出现错误: {error}")

# 从 CSV 文件中导入数据到数据库表，旧数据会被清空
def import_data_from_csv(connection):
    try:
        with connection.cursor() as cursor:
            # 清空旧数据
            cursor.execute("DELETE FROM domains")
            connection.commit()  # 确保删除操作提交
            # 导入新数据
            with open("top_one_million_domains.csv", 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # 跳过标题行
                id_counter = 1
                for row in reader:
                    domain = row[0].strip()
                    cursor.execute("INSERT INTO domains (id, domain_name) VALUES (%s, %s)", (id_counter, domain))
                    id_counter += 1
            connection.commit()
        print("数据导入成功，旧数据已被覆盖")
        return True
    except (Exception, psycopg2.Error) as error:
        print(f"导入数据时出现错误: {error}")
        if "permission denied" in str(error):
            print("可能是权限不足导致删除或插入数据失败，请检查数据库用户权限。")
        return False

# 主函数
def main():
    connection = None
    is_first_loop = True  # 标记是否为首次循环
    try:
        # 建立数据库连接
        connection = psycopg2.connect(**DB_CONFIG)
        # 设置隔离级别为默认的 READ COMMITTED
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        # 创建表
        create_table(connection)

        while True:
            try:
                # 获取所有排名桶数据集
                datasets = get_ranking_bucket_datasets()
                if not datasets:
                    print("未找到排名桶数据集")
                    raise Exception("未找到排名桶数据集")

                # 找到前一百万排名的数据集 ID
                dataset_id = find_top_one_million_dataset_id(datasets)
                if dataset_id is None:
                    print("未找到前一百万排名的数据集")
                    raise Exception("未找到前一百万排名的数据集")

                # 获取数据集的下载 URL
                download_url = get_dataset_download_url(dataset_id)
                if download_url is None:
                    print("未获取到下载 URL")
                    raise Exception("未获取到下载 URL")

                print(f"前一百万排名的数据集下载 URL: {download_url}")

                # 下载数据集并保存为 CSV 格式文件
                if not download_dataset(download_url):
                    print("下载数据集失败")
                    raise Exception("下载数据集失败")

                # 导入数据到数据库
                if not import_data_from_csv(connection):
                    print("导入数据到数据库失败")
                    raise Exception("导入数据到数据库失败")

                if not is_first_loop:
                    print(f"等待 {loop_interval / 3600} 小时后进行下一次更新...")
                    time.sleep(loop_interval)  # 非首次循环，数据导入成功后按照设置的间隔时间等待
                is_first_loop = False  # 首次循环结束，更新标志

            except Exception as e:
                print(f"出现错误: {e}，等待 {error_wait_time / 60} 分钟后重试...")
                time.sleep(error_wait_time)  # 等待错误等待时间后重试

    except (psycopg2.OperationalError) as error:
        print(f"数据库连接失败: {error}")
    except (Exception, psycopg2.Error) as error:
        print(f"数据库操作出现错误: {error}")
    finally:
        if connection:
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    main()