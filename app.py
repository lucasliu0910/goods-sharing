from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB 連線設置
mongo_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")  # 使用環境變數或預設
client = MongoClient(mongo_uri)
db = client["appointment_db"]  # 資料庫名稱
collection = db["appointments"]  # 集合名稱

@app.route('/')
def index():
    # 從 MongoDB 獲取所有預約
    appointments = list(collection.find({}, {"_id": 0}))  # 排除 _id 欄位
    return render_template('index.html', appointments=appointments)

@app.route('/submit', methods=['POST'])
def submit():
    # 從表單獲取資料
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    
    # 儲存到 MongoDB
    appointment = {
        "name": name,
        "date": date,
        "time": time
    }
    collection.insert_one(appointment)
    
    # 重定向到首頁以顯示更新後的預約列表
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)