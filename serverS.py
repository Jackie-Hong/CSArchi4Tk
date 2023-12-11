# server.py
from flask import Flask, request, jsonify, session
from flask_session import Session
import os

app = Flask(__name__)

# 设置密钥，用于加密 session 数据
app.config['SECRET_KEY'] = 'your_secret_key'
# 配置 session 存储方式，这里使用简单的基于文件的存储
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)


@app.route('/login', methods=['POST'])
def login():
    # user_id = request.json.get('user_id')
    # user_id = session.get('user_id')
    user_id = request.form.get('user_id')

    if user_id:
        # 将用户信息存储在 session 中
        session['user_id'] = user_id
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid request'})


@app.route('/api', methods=['POST'])
def api():
    user_id = session.get('user_id')
    message = request.form.get('message')

    # message = request.json.get('message')

    # if user_id and message:
    if user_id:
        response_data = {'user_id': user_id, 'message': message}
        # response_data = {'user_id': user_id, 'message': "message"}
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Invalid request'})

@app.route('/logout')
def logout():
    # 清除 session 中的用户信息
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'})


if __name__ == '__main__':
    app.run(debug=True)
