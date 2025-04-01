from flask import Flask, request, jsonify, render_template
import sqlite3
from src.db import init_database

init_database()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# 获取所有区队列表
@app.route('/api/teams', methods=['GET'])
def get_teams():
    conn = sqlite3.connect('信息网络安全大队_数据库文件.db')
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT 区队 FROM users')
    teams = cursor.fetchall()
    conn.close()
    return jsonify([team[0] for team in teams])

# 根据区队获取学生列表
@app.route('/api/students', methods=['GET'])
def get_students():
    team = request.args.get('team')
    conn = sqlite3.connect('信息网络安全大队_数据库文件.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 学号, 姓名 FROM users WHERE 区队 = ?', (team,))
    students = cursor.fetchall()
    conn.close()
    return jsonify([{'学号': row[0], '姓名': row[1]} for row in students])

@app.route('/api/scored-students', methods=['GET'])
def get_scored_students():
    team = request.args.get('team')
    student_id = request.args.get('student_id')  # 添加评分人学号作为查询条件
    conn = sqlite3.connect('信息网络安全大队_数据库文件.db')
    cursor = conn.cursor()

    # 查询已评价的学生学号
    cursor.execute('''
        SELECT DISTINCT 被评分学号
        FROM score
        WHERE 评分人学号 = ? AND 被评分学号 IN (
            SELECT 学号 FROM users WHERE 区队 = ?
        )
    ''', (student_id, team))  # 同时匹配评分人学号和区队
    scored_students = cursor.fetchall()
    conn.close()
    return jsonify([{'被评分学号': row[0]} for row in scored_students])

# 检验学号
@app.route('/api/check-student', methods=['GET'])
def check_student():
    student_id = request.args.get('student_id')
    conn = sqlite3.connect('信息网络安全大队_数据库文件.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 姓名, 区队 FROM users WHERE 学号 = ?', (student_id,))
    student = cursor.fetchone()
    conn.close()
    if student:
        return jsonify({'姓名': student[0], '区队': student[1]})
    else:
        return jsonify({'error': '学号不存在'}), 404

# 提交评分
@app.route('/api/submit-score', methods=['POST'])
def submit_score():
    data = request.get_json()
    student_id = data.get('student_id')  # 评分人学号
    student_name = data.get('student_name')  # 评分人姓名
    team = data.get('team')  # 区队
    target_student_id = data.get('target_student_id')  # 被评分人学号
    target_student_name = data.get('target_student_name')  # 被评分人姓名
    ideology_score = data.get('ideology_score')
    patriotism_score = data.get('patriotism_score')
    morality_score = data.get('morality_score')
    collectivism_score = data.get('collectivism_score')
    legality_score = data.get('legality_score')

    # 计算总分
    total_score = (
        int(ideology_score) +
        int(patriotism_score) +
        int(morality_score) +
        int(collectivism_score) +
        int(legality_score)
    )

    # 计算平均分
    average_score = total_score / 5

    # 验证分数范围
    if not (0 <= int(ideology_score) <= 30):
        return jsonify({'error': '理想信念分数必须在 0-30 之间'}), 400
    if not (0 <= int(patriotism_score) <= 25):
        return jsonify({'error': '爱国情怀分数必须在 0-25 之间'}), 400
    if not (0 <= int(morality_score) <= 20):
        return jsonify({'error': '道德品质分数必须在 0-20 之间'}), 400
    if not (0 <= int(collectivism_score) <= 15):
        return jsonify({'error': '集体观念分数必须在 0-15 之间'}), 400
    if not (0 <= int(legality_score) <= 10):
        return jsonify({'error': '法治观念分数必须在 0-10 之间'}), 400

    conn = sqlite3.connect('信息网络安全大队_数据库文件.db')
    cursor = conn.cursor()

    # 使用 INSERT OR REPLACE 实现去重更新
    cursor.execute('''
        INSERT OR REPLACE INTO score (
            评分人学号, 评分人姓名, 区队, 被评分学号, 被评分名字,
            理想信念分数, 爱国情怀分数, 道德品质分数, 集体观念分数, 法治观念分数,
            总分, 平均分
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        student_id, student_name, team, target_student_id, target_student_name,
        ideology_score, patriotism_score, morality_score, collectivism_score, legality_score,
        total_score, average_score
    ))

    conn.commit()
    conn.close()
    return jsonify({'message': '评分提交成功'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)