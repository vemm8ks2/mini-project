import os
from flask import Flask
from app.main.routes import main
from datetime import datetime

app = Flask(__name__)
today = datetime.today()

# 여기에 설정, 블루프린트 등록 등 애플리케이션 초기화 작업을 추가합니다.
app.config["년"] = today.year
app.config["월"] = today.month
app.config["일"] = today.day
app.config["기본_경로"] = f"C:/dataset/{app.config["년"]}/{app.config["월"]}/{app.config["일"]}"

app.register_blueprint(main)

def 최신_파일명_가져오기(파일_목록):
    최신_연도 = -1
    최신_파일명 = None

    for 파일 in 파일_목록:
        연도 = int(파일.split("_")[0])

        if 연도 > 최신_연도:
            최신_연도 = 연도
            최신_파일명 = 파일

    return 최신_파일명

if __name__ == '__main__':
    년, 월, 일 = app.config["년"], app.config["월"], app.config["일"]
    app.config["파일_목록"] = os.listdir(f"{app.config["기본_경로"]}/base")
    app.config["가장_최근_파일명"] = 최신_파일명_가져오기(app.config["파일_목록"])

    app.run(debug=True)
