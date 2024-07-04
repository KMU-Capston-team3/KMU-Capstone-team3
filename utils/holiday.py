import holidays
def is_holiday(date):
    kr_holidays = holidays.KR()
    return date in kr_holidays