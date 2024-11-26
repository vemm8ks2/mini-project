import os
import pandas as pd


def 재무제표_가져오기(경로):
    ext = 경로.split('.')[-1]

    if ext == 'txt':
        return pd.read_csv(경로, sep='\t', encoding='cp949')
    elif ext == 'csv':
        return pd.read_csv(경로)
    elif ext == 'xlsx':
        return pd.read_excel(경로, engine='openpyxl')


def 재무제표_저장(target, path):
    ext = path.split('.')[-1]

    if ext == 'csv':
        target.to_csv(path, index=False, encoding='utf-8')
    elif ext == 'xlsx':
        target.to_excel(path, index=False)
    elif ext == 'txt':
        target.to_csv(path, sep='\t', index=False, encoding='cp949')


def 재무제표_삭제(path):
    os.remove(path)