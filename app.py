from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient('mongodb+srv://test:sparta@cluster0.z68kdip.mongodb.net/?retryWrites=true&w=majority')
db = client.test0727


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    count = list(db.bucket.find({}, {'_id': False}))
    num = len(count) + 1

    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done':0
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록완료!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)}, {'$set': {'done':1}})
    return jsonify({'msg': '달성했다!'})


@app.route("/bucket/cancel", methods=['POST'])
def bucket_cancel():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)}, {'$set': {'done':0}})
    return jsonify({'msg': '취소했다!'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets': bucket_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
