import datetime


def get_current_date():
    return datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                              datetime.datetime.now().day, datetime.datetime.now().hour,
                              datetime.datetime.now().minute)