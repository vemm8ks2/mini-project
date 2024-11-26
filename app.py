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
app.config["루트_경로"] = f"C:/dataset/{app.config["년"]}/{app.config["월"]}"
app.config["재무제표_종류"] = ["손익계산서", "재무상태표", "현금흐름표"]
app.config["재무제표_목록"] = {}
app.config["종목"] = {}
app.config["종목코드"] = {}

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

    경로_목록 = [f"{app.config["루트_경로"]}/{경로}" for 경로 in app.config["재무제표_종류"]]
    
    for 종류 in app.config["재무제표_종류"]:
        app.config["재무제표_목록"][종류] = {}
        app.config["재무제표_목록"][종류]["기본_경로"] = f"{app.config["루트_경로"]}/{종류}"

        기본_경로 = app.config["재무제표_목록"][종류]["기본_경로"]
        모든_목록 = os.listdir(기본_경로)
        폴더_목록 = [폴더 for 폴더 in 모든_목록 if os.path.isdir(os.path.join(기본_경로, 폴더))]

        for 폴더 in 폴더_목록:
            연도 = 폴더.split("_")[0]
            파일_목록 = os.listdir(f"{기본_경로}/{폴더}")

            app.config["재무제표_목록"][종류][연도] = {}
            app.config["재무제표_목록"][종류][연도]["폴더_경로"] = f"{기본_경로}/{폴더}"
            
            app.config["재무제표_목록"][종류][연도]["별도"] = []
            별도 = app.config["재무제표_목록"][종류][연도]["별도"]

            app.config["재무제표_목록"][종류][연도]["연결"] = []
            연결 = app.config["재무제표_목록"][종류][연도]["연결"]

            for 파일명 in 파일_목록:
                if "연결" in 파일명 and 파일명.endswith(".txt"):
                    연결.append(파일명) # 파일명이 '연결'을 포함하고 txt 파일이면 연결 재무제표이므로 '연결' 리스트에 추가
                elif 파일명.endswith(".txt"):
                    별도.append(파일명) # 파일명이 '연결'을 포함하지 않고 txt 파일이면 별도 재무제표이므로 '별도' 리스트에 추가

    for k1, v1 in app.config["재무제표_목록"].items():
        for k2, v2 in v1.items():
            print(k2, v2, '\n')

    app.run(debug=True)
