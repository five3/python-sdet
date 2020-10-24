import records


def get_db():
    return records.Database('mysql+pymysql://root:changeit!@www.testqa.cn:3306/sdet')
