import sqlite3
import pandas as pd
import numpy as np
import os
from loguru import logger

# 配置 loguru 日志输出
logger.add("logfile.log", rotation="10 MB", level="INFO")

def calculate_individual_scores(db_path):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_path)

    # 查询 score 表和 users 表，获取被评分人的姓名和区队
    query = '''
        SELECT s.被评分学号, u.姓名, u.区队, s.总分
        FROM score s
        JOIN users u ON s.被评分学号 = u.学号
    '''
    score_df = pd.read_sql_query(query, conn)

    # 将被评分学号转换为文本类型
    score_df['被评分学号'] = score_df['被评分学号'].astype(str)

    # 计算每个被评分人的总分和去前后10%后的平均分
    individual_scores = []
    for student_id, group in score_df.groupby('被评分学号'):
        name = group['姓名'].iloc[0]  # 获取被评分人姓名
        team = group['区队'].iloc[0]  # 获取被评分人区队
        total_score = group['总分'].sum()  # 计算总分

        # 对评分分数进行排序
        scores = group['总分'].sort_values().tolist()
        logger.info(f"\n被评分人: {name}, 区队: {team}, 原始分数: {scores}")

        # 去掉前10%和后10%的分数
        n = len(scores)
        lower_bound = int(n * 0.1)  # 前10%的索引
        upper_bound = int(n * 0.9)  # 后10%的索引
        trimmed_scores = scores[lower_bound:upper_bound]
        logger.info(f"去掉前10%和后10%后的分数: {trimmed_scores}")

        # 计算剩余分数的平均分
        trimmed_avg = np.mean(trimmed_scores) if trimmed_scores else 0
        logger.info(f"去掉极端分数后的平均分: {trimmed_avg:.2f}")

        # 将结果添加到 individual_scores 中
        individual_scores.append({
            '被评分学号': student_id,
            '姓名': name,
            '区队': team,
            '总分': total_score,
            '去前后10%平均分': trimmed_avg
        })

    # 将结果转换为 DataFrame
    individual_scores_df = pd.DataFrame(individual_scores)

    # 关闭数据库连接
    conn.close()

    return individual_scores_df

def calculate_average_score_by_team(db_path):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_path)

    # 获取每个被评分人的总分
    individual_scores = calculate_individual_scores(db_path)

    # 查询每个被评分人的区队信息
    query = '''
        SELECT 学号, 区队
        FROM users
    '''
    user_df = pd.read_sql_query(query, conn)

    # 将 user_df 中的学号转换为字符串类型
    user_df['学号'] = user_df['学号'].astype(str)

    # 将 individual_scores 和 user_df 合并，获取每个被评分人的总分和区队
    merged_df = pd.merge(
        individual_scores,
        user_df,
        left_on='被评分学号',
        right_on='学号',
        how='left'
    )

    # 检查 merged_df 的字段名，确保正确访问区队字段
    # 合并后，区队字段可能会被重命名为 区队_x 或 区队_y
    if '区队_x' in merged_df.columns:
        team_column = '区队_x'
    elif '区队_y' in merged_df.columns:
        team_column = '区队_y'
    else:
        team_column = '区队'

    # 使用字典按区队分组总分
    team_scores = {}
    for _, row in merged_df.iterrows():
        team = row[team_column]
        total_score = row['总分']
        if team not in team_scores:
            team_scores[team] = []
        if total_score is not None:
            team_scores[team].append(total_score)

    # 输出每个区队的原始分数
    logger.info("各区队的原始分数:")
    for team, scores in team_scores.items():
        logger.info(f"{team}: {scores}")

    # 计算每个区队的平均分
    average_scores = {}
    for team, scores in team_scores.items():
        logger.info(f"\n计算区队 {team} 的平均分:")
        if len(scores) < 10:
            average_scores[team] = np.mean(scores) if scores else 0
            logger.info(f"  成员不足10人，直接计算平均分: {average_scores[team]:.2f}")
            continue

        # 将分数排序
        scores.sort()
        logger.info(f"  排序后的分数: {scores}")

        # 计算去掉前10%和后10%后的平均值
        n = len(scores)
        lower_bound = int(n * 0.1)  # 前10%的索引
        upper_bound = int(n * 0.9)  # 后10%的索引

        # 取出中间的分数
        trimmed_scores = scores[lower_bound:upper_bound]
        logger.info(f"  去掉前10%和后10%后的分数: {trimmed_scores}")

        # 计算平均值
        average_scores[team] = np.mean(trimmed_scores) if trimmed_scores else 0
        logger.info(f"  去掉极端分数后的平均分: {average_scores[team]:.2f}")

    # 关闭数据库连接
    conn.close()

    return team_scores, average_scores

def export_data_to_excel(db_path, output_folder, team_scores, average_scores, individual_scores):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_path)

    # 查询 user 表
    user_query = "SELECT * FROM users"
    user_df = pd.read_sql_query(user_query, conn)

    # 查询 score 表
    score_query = "SELECT * FROM score"
    score_df = pd.read_sql_query(score_query, conn)

    # 将学号字段转换为文本格式
    user_df['学号'] = user_df['学号'].astype(str)
    score_df['评分人学号'] = score_df['评分人学号'].astype(str)
    score_df['被评分学号'] = score_df['被评分学号'].astype(str)

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)

    # 将数据导出到 Excel 文件
    output_file_path = os.path.join(output_folder, 'output.xlsx')
    with pd.ExcelWriter(output_file_path) as writer:
        user_df.to_excel(writer, sheet_name='user', index=False)
        score_df.to_excel(writer, sheet_name='score', index=False)

        # 创建一个 DataFrame 存储区队的成绩和平均分
        team_scores_df = pd.DataFrame({
            '区队': list(team_scores.keys()),
            '平均分': [average_scores.get(team, 0) for team in team_scores.keys()]
        })

        # 将区队成绩和平均分导出到 Excel
        team_scores_df.to_excel(writer, sheet_name='区队成绩', index=False)

        # 将每个被评分人的总分和去前后10%后的平均分导出到 Excel
        individual_scores.to_excel(writer, sheet_name='被评分人成绩', index=False)

    # 关闭数据库连接
    conn.close()

    logger.info(f"数据已成功导出到 {output_file_path}")

# 使用示例
db_path = '信息网络安全大队_数据库文件.db'  # 请替换为你的数据库路径
output_folder = 'output_folder'  # 请替换为你希望输出的文件夹路径

# 计算区队平均分
team_scores, average_scores_by_team = calculate_average_score_by_team(db_path)

# 计算每个被评分人的总分和去前后10%后的平均分
individual_scores = calculate_individual_scores(db_path)

# 输出结果
logger.info("\n最终各区队的平均分:")
for team, avg_score in average_scores_by_team.items():
    logger.info(f"区队: {team}, 全区队评价成绩的平均值为: {avg_score:.2f}")

# 导出数据到 Excel
export_data_to_excel(db_path, output_folder, team_scores, average_scores_by_team, individual_scores)