import pandas as pd
import numpy as np


np.random.seed()
df1 = pd.read_csv('rest1.csv', sep='|', engine='python', na_filter=False)
df2 = pd.read_csv('rest2.csv', sep='|', engine='python', na_filter=False)
gt = pd.read_csv('gt.csv', sep='|', engine='python', na_filter=False)

percentage = 0.1
num_pairs = int(len(df1) * len(df2) * percentage)
random_pairs = np.random.choice(len(df1) * len(df2), num_pairs, replace=False)
indices_df1 = random_pairs // len(df2)
indices_df2 = random_pairs % len(df2)

new_df = pd.DataFrame({
    'ltable_id': df1['id'].iloc[indices_df1].values,
    **df1.iloc[indices_df1].drop('id', axis=1).to_dict(orient='list'),
    'rtable_id': (df2['id'].iloc[indices_df2].values).astype(int),
    **df2.iloc[indices_df2].drop('id', axis=1).to_dict(orient='list'),
})

new_df.reset_index(drop=True, inplace=True)
merged_df = pd.merge(new_df, gt, how='left', left_on=['ltable_id', 'rtable_id'], right_on=['D1', 'D2'])
merged_df['_id'] = merged_df.reset_index().index
merged_df['label'] = ~merged_df['D1'].isnull()
merged_df['label'].fillna(False, inplace=True)
merged_df['label'] = merged_df['label'].astype(int)
merged_df.drop(['D1', 'D2'], axis=1, inplace=True)
merged_df['rtable_id'] += len(df1) 

merged_df.to_csv('labeled_data.csv', index=False)