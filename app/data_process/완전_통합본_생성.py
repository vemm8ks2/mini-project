from flask import current_app
import os
import pandas as pd

from app.data_process.재무제표_제어 import 재무제표_가져오기, 재무제표_저장, 재무제표_삭제


def 완전_통합본_생성(분류):
    app = current_app  # 현재 활성화된 앱에 접근

    삭제_파일_경로 = []

    완전_통합본_저장_경로 = f"{app.config["루트_경로"]}/{분류}완전_통합본.csv"
    재무제표_완전_통합본 = pd.DataFrame()

    for 재무제표_종류, 연도별_구분별_분류 in app.config["재무제표_목록"].items():
        기본_경로 = 연도별_구분별_분류["기본_경로"]
        통합본_경로 = f"{기본_경로}/{분류}통합본.csv"
        삭제_파일_경로.append(통합본_경로)

        if not os.path.isfile(통합본_경로):
            raise FileNotFoundError(f'아직 통합본이 생성되지 않았습니다 : {통합본_경로}')

        전체_통합본 = 재무제표_가져오기(통합본_경로)
        재무제표_완전_통합본 = pd.concat([재무제표_완전_통합본, 전체_통합본], axis=0, ignore_index=True)

    재무제표_저장(재무제표_완전_통합본, 완전_통합본_저장_경로)

    for 경로 in 삭제_파일_경로:
        재무제표_삭제(경로)

    print(f'{분류} 재무제표 완전 통합본 저장 완료')