import csv
import psycopg2
import requests
from loguru import logger
from tqdm import tqdm
import time







def get_ranking_bucket_datasets(headers):
    url = "https://api.cloudflare.com/client/v4/radar/datasets?limit=10&datasetType=RANKING_BUCKET"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                return data["result"]["datasets"]
    except requests.RequestException as e:
        logger.info(f"获取排名桶数据集时出现网络错误: {e}")
    return []

# 第二步：找到前一百万排名的数据集 ID
def find_top_one_million_dataset_id(datasets):
    for dataset in datasets:
        if dataset["meta"].get("top") == 1000000:
            return dataset["id"]
    return None

# 第三步：获取数据集的下载 URL
def get_dataset_download_url(dataset_id,headers):
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
        logger.info(f"获取数据集下载 URL 时出现网络错误: {e}")
    return None

# 第四步：下载数据集并保存为 CSV 格式文件
def download_dataset(url):
    try:
        logger.info("开始下载数据集...")
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
            logger.info("下载未完成，可能网络出现问题。")
            return False

        logger.info("下载完成，开始转换为 CSV 格式...")
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

        logger.info("数据集已成功保存为 top_one_million_domains.csv")
        return True
    except requests.RequestException as e:
        logger.info(f"下载过程中出现网络错误: {e}")
        return False
    except Exception as e:
        logger.info(f"下载或保存文件时出现错误: {e}")
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
        logger.info("表创建成功")
    except (Exception, psycopg2.Error) as error:
        logger.info(f"创建表时出现错误: {error}")

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
        logger.info("数据导入成功，旧数据已被覆盖")
        return True
    except (Exception, psycopg2.Error) as error:
        logger.info(f"导入数据时出现错误: {error}")
        if "permission denied" in str(error):
            logger.info("可能是权限不足导致删除或插入数据失败，请检查数据库用户权限。")
        return False


def Get_100(API_TOKEN,DB_CONFIG):
    """
    获取前一百万排名的数据集并导入数据库

    Args:
        API_TOKEN: API认证令牌

    Returns:
        bool: 操作是否成功
    """
    connection = None
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    try:
        # 建立数据库连接
        connection = psycopg2.connect(**DB_CONFIG)
        # 设置隔离级别为默认的 READ COMMITTED
        connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
        # 创建表
        create_table(connection)
        # 获取所有排名桶数据集
        datasets = get_ranking_bucket_datasets(headers=headers)
        if not datasets:
            logger.info("未找到排名桶数据集")
            return False

        # 找到前一百万排名的数据集 ID
        dataset_id = find_top_one_million_dataset_id(datasets)
        if dataset_id is None:
            logger.info("未找到前一百万排名的数据集")
            return False

        # 获取数据集的下载 URL
        download_url = get_dataset_download_url(dataset_id, headers=headers)
        if download_url is None:
            logger.info("未获取到下载 URL")
            return False

        logger.info(f"前一百万排名的数据集下载 URL: {download_url}")

        # 下载数据集并保存为 CSV 格式文件
        if not download_dataset(download_url):
            logger.info("下载数据集失败")
            return False

        # 导入数据到数据库
        if not import_data_from_csv(connection):
            logger.info("导入数据到数据库失败")
            return False

        logger.info("数据获取和导入成功完成")
        return True

    except (psycopg2.OperationalError) as error:
        logger.info(f"数据库连接失败: {error}")
        return False
    except (Exception, psycopg2.Error) as error:
        logger.info(f"数据库操作出现错误: {error}")
        return False
    finally:
        if connection:
            connection.close()
            logger.info("数据库连接已关闭")