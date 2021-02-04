import os

from djangoHealthAnalytics.settings import BASE_DIR


def mergeCSVs():
    import pandas as pd

    import glob

    path = os.path.join(BASE_DIR, 'media', 'csv')  # use your path

    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        print(filename)
        df = pd.read_csv(filename, index_col=None, header=0)

        li.append(df)
        os.remove(filename)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.rename(columns={'dateprescribed': 'date', 'diagnosis': 'disease'},inplace=True)
    frame.drop('prescription', inplace=True, axis=1)
    frame["disease"]=frame["disease"].str.lower()
    frame = frame[['location', 'disease', 'gender', 'date']]
    frame.replace({'male':'m','female':'f'})
    # df.to_csv('my_csv.csv', mode='a', header=False)
    frame.to_csv('{}/data/Diseases.csv'.format(BASE_DIR), mode='a', header=False)


mergeCSVs()
