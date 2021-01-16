from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbmyproject

@app.route('/')
def home():  # 함수명 수정 - 이름만 보고 접속되는 페이지를 확인할 수 있게!
    return render_template('index.html')

@app.route('/bbang', methods=['POST'])
def save_bbang():

    bbang = {
        'sido': request.form['sido_give'],
        'sigugun': request.form['sigugun_give'],
        'address': request.form['address_give'],
        'taste': request.form['taste_give'],
        'detail': request.form['detail_give'],
        'like': 0,
        'delete': 0
    }
    db.bbangs.insert_one(bbang)
    return jsonify({'result': 'success', 'msg': '감사합니다. 당신의 정보가 따뜻한 붕어빵을 선물했습니다.'})

@app.route('/bbang', methods=['GET'])
def view_bbang():
    bbang_list = list(db.bbangs.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'bbang_list': bbang_list})

@app.route('/bbang/like', methods=['POST'])
def like_bbang():
    address_receive = request.form['address_give']
    spot = db.bbangs.find_one({'address': address_receive})
    new_like = spot['like'] +1
    db.bbangs.update_one({'address': address_receive}, {'$set': {'like': new_like}})

    return jsonify({'result': 'success'})

@app.route('/bbang/delete', methods=['POST'])
def delete_bbang():
    address_receive = request.form['address_give']
    spot_delete = db.bbangs.find_one({'address': address_receive})
    new_delete = spot_delete['delete'] +1
    db.bbangs.update_one({'address': address_receive}, {'$set': {'delete': new_delete}})

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)