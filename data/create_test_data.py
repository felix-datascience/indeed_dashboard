import pandas as pd
import numpy as np


# load data set
all_data = pd.read_json('data_science_jobs_2020-10-01.json')

# shuffle rows
all_data = all_data.sample(frac=1)

# function for creating series with random dates in defined range
def random_date(start, end, n):
    start_u = start.value//10**9
    end_u = end.value//10**9
    return pd.Series((10**9*np.random.randint(start_u, end_u, n, dtype=np.int64)).view('M8[ns]'))

# define start and end value of time series
start = pd.to_datetime('2020-09-01')
end = pd.to_datetime('2020-11-01')

# length of time series => length of all_data dataframe
n = len(all_data)

# create time series
test_series = random_date(start, end, n)

# add to dataframe
all_data['date'] = test_series

#print(type(all_data.date.iloc[1]))
# split all_data df into smaller dfs by weeks
split_by_week = {timestamp: sub_df for timestamp, sub_df in all_data.groupby(pd.Grouper(key='date', freq='W'))}

# export each sub dataframe as json
for timestamp, sub_df in split_by_week.items():
    sub_df.to_json(f'split_up_test_data/{timestamp.date()}.json', orient='records', date_format='epoch')
