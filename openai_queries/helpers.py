import pandas as pd


def get_questions_from_xlsx(excel_path: str):
    series = pd.read_excel(excel_path, header=None).iloc[:, 0]
    return series

