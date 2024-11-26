import pandas as pd
from flask import Blueprint, render_template, request

from app.data_process.완전_통합본_생성 import 완전_통합본_생성

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def get_method():
    return render_template('index.html', 업종_및_업종명=pd.DataFrame())

@main.route('/', methods=['POST'])
def post_method():
    업종 = request.form.get('업종')
    print(업종)

    return render_template('index.html', 업종_및_업종명=pd.DataFrame())

@main.route('/tmp', methods=['POST'])
def tmp_method():
    #통합본_생성("별도")
    #통합본_생성("연결")
    #통합본_생성("별도-연결")

    #전체_통합본_생성('별도')
    #전체_통합본_생성('연결')
    #전체_통합본_생성('별도-연결')

    #완전_통합본_생성('전체_별도_')
    #완전_통합본_생성('전체_연결_')
    완전_통합본_생성('전체_별도-연결_')

    return render_template('index.html', 업종_및_업종명=pd.DataFrame())