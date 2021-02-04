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
    frame.rename(columns={'dateprescribed': 'date', 'diagnosis': 'disease'}, inplace=True)
    frame.drop('prescription', inplace=True, axis=1)
    frame["disease"] = frame["disease"].str.lower()
    frame["location"] = frame["location"].str.lower()
    frame = frame[['date','location', 'disease', 'gender']]
    frame.replace({'male': 'm', 'female': 'f'})
    # df.to_csv('my_csv.csv', mode='a', header=False)
    frame.to_csv('{}/data/Diseases.csv'.format(BASE_DIR), mode='a', header=False)


def cleanCSV():
    import pandas as pd

    import glob

    path = os.path.join(BASE_DIR, 'data','nigeria.csv')  # use your path

    df = pd.read_csv(path, index_col=None, header=0)
    df.rename(columns={'report_date': 'date', 'state': 'location'}, inplace=True)
    df["disease"] = df["disease"].str.lower()
    df["location"] = df["location"].str.lower()
    df["gender"] = df["gender"].str.lower()
    df = df[['date', 'location', 'disease', 'gender']]

    df=df.set_index('date')
    df.to_csv('{}/data/Diseases.csv'.format(BASE_DIR), mode='w', header=True)
    print(df.head())
cleanCSV()