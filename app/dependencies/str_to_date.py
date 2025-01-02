import datetime
def str_to_date(txt : str):
    return datetime.date(int(txt.split('-')[0]),int(txt.split('-')[1]),int(txt.split('-')[2]))