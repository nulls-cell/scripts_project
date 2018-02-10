import datetime

# n天之后，n可以是负数
def add_date(n):
    assert(isinstance(n, int))
    return datetime.datetime.now() + datetime.timedelta(days=n)

