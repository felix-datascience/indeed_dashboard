import pandas as pd
import numpy as np
import datetime


# load data set
all_data = pd.read_json('data_science_jobs_2020-10-01.json')

# data cleaning
all_data['company'] = all_data['company'].apply(lambda s: s[1:])
all_data['salary'] = all_data['salary'].apply(lambda s: s[1:] if type(s) == str else None)
all_data['description'] = all_data['description'].apply(lambda l: ''.join(l))

# shuffle rows
all_data = all_data.sample(frac=1)

# function for creating series with random dates in defined range
def random_date(start, end, n):
    start_u = start.value//10**9
    end_u = end.value//10**9
    return pd.Series((10**9*np.random.randint(start_u, end_u, n, dtype=np.int64)).view('M8[ns]'))


# define start and end value of time series
start = pd.to_datetime('2020-09-07')
end = pd.to_datetime('2020-10-05')

# length of time series => length of all_data dataframe
n = len(all_data)

# create time series
time_series = random_date(start, end, n)

# add to dataframe
all_data['date'] = time_series

# split all_data df into smaller dfs by weeks
split_by_week = {timestamp: sub_df for timestamp, sub_df in all_data.groupby(pd.Grouper(key='date', freq='W'))}

# from timestamp to isoformat string (yyyy-mm-dd)
for timestamp, sub_df in split_by_week.items():
    sub_df['date'] = sub_df['date'].apply(lambda d: d.isoformat()[:10])

# export each sub dataframe as json
for timestamp, sub_df in split_by_week.items():
    first_day = sub_df['date'].iloc[0]
    sub_df.to_json(f'split_up_test_data/{first_day}.json', orient='records', date_format='epoch')
