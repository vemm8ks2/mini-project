import os
import pandas as pd
from flask import current_app

from app.data_process.재무제표_제어 import 재무제표_가져오기, 재무제표_저장


def 재무제표_통합(구분, 파일_경로, 저장_경로='nothing'):
    별도_구분자 = ['sep', 'separate', '별도']
    연결_구분자 = ['con', 'consolidated', '연결']
    확장자 = ['xlsx', 'csv', 'txt']

    if 구분.lower() not in 별도_구분자 + 연결_구분자:
        raise ValueError("kind의 파라미터는 'sep', 'con', separate', 'consolidated', '별도', '연결' 중 하나여야 합니다.")

    저장_유형 = 저장_경로.split('.')[-1]

    if 저장_경로 != 'nothing' and 저장_유형 not in 확장자:
        raise ValueError("save_as의 파라미터는 'xlsx', 'csv', 'txt' 중 하나여야 합니다.")

    if os.path.isfile(저장_경로):
        return 재무제표_가져오기(저장_경로)

    재무제표_통합본 = pd.DataFrame()

    for 파일명 in 파일_경로:
        재무제표 = pd.read_csv(파일명, sep='\t', encoding='cp949')
        재무제표_통합본 = pd.concat([재무제표_통합본, 재무제표], axis=0, ignore_index=True)

    if 저장_경로 != 'nothing':
        재무제표_저장(재무제표_통합본, 저장_경로)

    return 재무제표_통합본


def 재무제표_통합_작업(구분, 파일_경로, 저장_경로='nothing', 반환=True):
    if 저장_경로 != 'nothing' and os.path.isfile(저장_경로):
        if 반환:
            재무제표_가져오기(저장_경로)
        else:
            return

    return 재무제표_통합(구분, 파일_경로, 저장_경로)


def 통합본_생성(구분):
    app = current_app  # 현재 활성화된 앱에 접근

    for 재무제표_종류, 연도별_구분별_분류 in app.config["재무제표_목록"].items():
        for 연도, 구분별_분류 in 연도별_구분별_분류.items():
            if 연도 == "기본_경로":
                continue

            별도_재무제표_파일_경로 = [f"{구분별_분류["폴더_경로"]}/{파일명}" for 파일명 in 구분별_분류["별도"]]
            연결_재무제표_파일_경로 = [f"{구분별_분류["폴더_경로"]}/{파일명}" for 파일명 in 구분별_분류["연결"]]

            별도_통합본_저장_경로 = f"{구분별_분류["폴더_경로"]}/별도_통합본.csv"
            연결_통합본_저장_경로 = f"{구분별_분류["폴더_경로"]}/연결_통합본.csv"

            if 구분 == '별도':
                재무제표_통합_작업('별도', 별도_재무제표_파일_경로, 별도_통합본_저장_경로, False)
                continue

            if 구분 == '연결':
                재무제표_통합_작업('연결', 연결_재무제표_파일_경로, 연결_통합본_저장_경로, False)
                continue

            if 구분 == '별도-연결':
                별도_연결_재무제표_저장_경로 = f"{구분별_분류["폴더_경로"]}/별도-연결_통합본.csv"

                if not os.path.isfile(별도_연결_재무제표_저장_경로):
                    별도_재무제표_통합본 = 재무제표_통합_작업('별도', 별도_재무제표_파일_경로)
                    연결_재무제표_통합본 = 재무제표_통합_작업('연결', 연결_재무제표_파일_경로)

                    별도_연결_재무제표_통합본 = pd.concat([별도_재무제표_통합본, 연결_재무제표_통합본], axis=0, ignore_index=True)

                    재무제표_저장(별도_연결_재무제표_통합본, 별도_연결_재무제표_저장_경로)
