""" """
import datetime as dt
import pandas as pd
# yyyy-mm-dd dd-mmm yyyy


def reformat_dates(dates):
    """Function 1 """
    outl = []
    for i in dates:
        k = dt.datetime.strptime(i, '%Y-%m-%d')
        outl.append(k.strftime('%d %b %Y'))
    return outl


def date_range(start, n):
    """ Function 2"""
    if type(start) != type('abc'):
        raise TypeError
    elif type(n) != type(1):
        raise TypeError
    else:
        a1 = dt.datetime.strptime(start, '%Y-%m-%d')
        # print(a1)
        k = [a1]
        for i in range(n - 1):
            a1 += dt.timedelta(days=1)
            #print(a1)
            k.append(a1)

        return k


def add_date_range(values,start_date):
    """ Function 3 """
    date_val = date_range(start_date, len(values))
    k = []
    for i in range(len(values)):
        k.append((date_val[i], values[i]))
    return k


def fees_report(infile, outfile):
    """ Function 4"""
    df = pd.read_csv(infile)
    df = df.drop(['book_uid', 'isbn_13', 'date_checkout'], axis=1)
    df['date_due'] = pd.to_datetime(df['date_due'], format="%m/%d/%Y")
    df['date_returned'] = pd.to_datetime(df['date_returned'], format="%m/%d/%Y")
    df['extra_days'] = df['date_returned'] - df['date_due']
    df['extra_days'] = df['extra_days'].map(lambda k:int(str(k).split(' ')[0]))
    df['extra_days'] = df['extra_days'].map(lambda k:k if k>0 else 0)
    df['late_fees'] = df['extra_days'].map(lambda k:round(k*0.25,2))
    df.drop(['date_due', 'date_returned', 'extra_days'], axis=1, inplace=True)
    df = df.groupby(['patron_id']).sum()
    # return df
    df.to_csv(outfile)
