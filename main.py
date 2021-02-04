# # age---normal
# # gender----male/female(M,F)
# # disease----(malaria,cholera,typhoid)
# # locations----(machakos,nairobi,addis ababa)
# # time(btwn 2005 and 2018)
# import csv
# import datetime
# import random
#
# import numpy as np
#
# gender = ['m', 'f']
# disease = ['malaria', 'typhoid', 'cholera']
# locations = ['machakos', 'nairobi', 'garissa']
#
#
# def agedistro(turn, end, size):
#     totarea = turn + (end - turn) / 2  # e.g. 50 + (90-50)/2
#     areauptoturn = turn  # say 50
#     areasloped = (end - turn) / 2  # (90-50)/2
#     size1 = int(size * areauptoturn / totarea)
#     size2 = size - size1
#     s1 = np.random.uniform(low=0, high=turn, size=size1)  # (low=0.0, high=1.0, size=None)
#     s2 = np.random.triangular(left=turn, mode=turn, right=end, size=size2)  # (left, mode, right, size=None)
#     # mode : scalar-  the value where the peak of the distribution occurs.
#     # The value should fulfill the condition left <= mode <= right.
#     s3 = np.concatenate((np.ceil(s1), np.ceil(s2)))  # don't use add , it will add the numbers piecewise
#     return s3
#
#
# def rand_date():
#     start_date = datetime.date(2005, 1, 1)
#     end_date = datetime.date(2018, 2, 1)
#
#     time_between_dates = end_date - start_date
#     days_between_dates = time_between_dates.days
#     random_number_of_days = random.randrange(days_between_dates)
#     random_date = start_date + datetime.timedelta(days=random_number_of_days)
#
#     return random_date
#
#
# r = rand_date()
# print(r)
# s3 = agedistro(turn=50, end=90, size=100000)
#
# with open('file.csv', mode='w') as data_file:
#     data_writer = csv.writer(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#
#     data_writer.writerow(['age', 'location', 'disease', 'gender', 'date'])
#     for x in s3:
#         data_writer.writerow([x, random.choice(locations), random.choice(disease), random.choice(gender), rand_date()])
#     print('wrote to file')
import pandas as pd

data = pd.read_csv('{}/data/Diseases.csv'.format(BASE_DIR))
# set date as the index
data = data.set_index('date')
# get disease and location specific data
# print(type(self.disease))
# disease = data[data.disease == "{}".format(self.disease)]
# location = disease[disease.location == "{}".format(self.location)]
disease = data[data.disease == disease]
location = disease[disease.location == self.location]

# Count disease cases in the specific location
df = location.groupby('date').count()
df = df.disease.to_frame()
df = df.rename(columns={"disease": "Number of cases"})
df

# Exporting the new disease and location specific data to a csv
df.to_csv(r'{}/data/location.csv'.format(self.BASE_DIR), index=True, header=True)
df