import io
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile

warnings.filterwarnings("ignore")
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import load_model

from accounts.models import User
from pathlib import Path

from pages.models import Images


class ML:
    BASE_DIR = Path(__file__).resolve().parent.parent
    location = disease = None

    def __init__(self, location, disease):
        self.location = location
        self.disease = disease

    def generate_csv(self):

        # # get all data from csv file
        # data = pd.read_csv('{}/data/nigeria.csv'.format(self.BASE_DIR))
        # print("Nigeria\n")
        # print(self.disease)
        # data = data.sort_values(by=["report_date"], ascending=True)
        # # remove null dates
        # data = data[~data['report_date'].isin(['0000-00-00'])]
        # # get disease specific data
        # disease = data[data.disease ==self.disease]
        # print(disease.head())
        #
        # disease['Date'] = pd.to_datetime(disease['report_date'])
        # per = disease.Date.dt.to_period("M")
        # dfg = disease.groupby(per)
        # dfg.sum()
        #
        # df = dfg.aggregate(np.sum)
        #
        # df = df.rename(columns={self.disease.lower(): "Number of Cases"})
        # df = df[['Number of Cases']]
        # # Exporting the new disease specific data to a csv
        # df.to_csv(r'{}/data/disease.csv'.format(self.BASE_DIR), index=True, header=True)

        # get all data from csv file
        data = pd.read_csv('{}/data/nigeria.csv'.format(self.BASE_DIR))
        data = data.sort_values(by=["report_date"], ascending=True)
        # remove null dates
        data = data[~data['report_date'].isin(['0000-00-00'])]
        dname = self.disease
        statename = self.location
        location = data[data.state == statename]
        # get disease specific data
        disease = location[location.disease == dname]

        disease['Date'] = pd.to_datetime(disease['report_date'])
        disease = disease.filter(["Date", "state", dname.lower()])

        per = disease.Date.dt.to_period("M")
        dfg = disease.groupby(per)
        dfg.sum()
        df = dfg.aggregate(np.sum)

        sLength = len(df[dname.lower()])
        df['state'] = pd.Series(np.random.randn(sLength), index=df.index)
        df['state'] = statename

        print(df)
        # print(df1)

        df = df.rename(columns={dname.lower(): "Number of Cases", "state": "location"})

        # new = df[['Date','Number of Cases', 'state']].copy()

        df = df[['Number of Cases', 'location']]

        # Exporting the new disease and location specific data to a csv
        df.to_csv(r'{}/data/disease.csv'.format(self.BASE_DIR), index=True, header=True)

    def generate_predictions(self, user):

        df = pd.read_csv('{}/data/disease.csv'.format(self.BASE_DIR))
        df = df.drop(columns=['location'])
        if self.disease == 'Measles':
            model = load_model('{}/data/measlesmodel.h5'.format(self.BASE_DIR))
        elif self.disease == 'Malaria':
            model = load_model('{}/data/malariamodel.h5'.format(self.BASE_DIR))
        else:
            print("Invalid model")

        df.Month = pd.to_datetime(df.Date)
        df = df.set_index("Date")
        train, test = df[:-8], df[-8:]
        scaler = MinMaxScaler()
        scaler.fit(train)
        train = scaler.transform(train)
        test = scaler.transform(test)
        n_input = 8
        n_features = 1

        pred_list = []

        batch = train[-n_input:].reshape((1, n_input, n_features))

        for i in range(n_input):
            pred_list.append(model.predict(batch)[0])
            batch = np.append(batch[:, 1:, :], [[pred_list[i]]], axis=1)

        df.index = pd.to_datetime(df.index)
        from pandas.tseries.offsets import DateOffset
        add_dates = [df.index[-3] + DateOffset(months=x) for x in range(0, 10)]
        future_dates = pd.DataFrame(index=add_dates[1:], columns=df.columns)
        df_predict = pd.DataFrame(scaler.inverse_transform(pred_list),
                                  index=future_dates[-n_input:].index, columns=['Prediction'])

        df_proj = pd.concat([df, df_predict], axis=1)

        plt.figure(figsize=(20, 10))
        plt.plot(df_proj.index, df_proj['Number of Cases'])
        plt.plot(df_proj.index, df_proj['Prediction'], color='r')
        plt.legend(loc='best', fontsize='xx-large')
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=16)
        # plt.show()
        plt.savefig('disease.jpg')

        # plot_data = [
        #     go.Scatter(
        #         x=df_proj.index,
        #         y=df_proj['Number of Cases'],
        #         name='actual'
        #     ),
        #     go.Scatter(
        #         x=df_proj.index,
        #         y=df_proj['Prediction'],
        #         name='predicted'
        #     )
        #
        # ]
        # plot_layout = go.Layout(
        #     title='Cases Prediction'
        # )
        # fig = go.Figure(data=plot_data, layout=plot_layout)
        # pyoff.iplot(fig)
        #
        # fig.write_image('{}/data/image.jpeg'.format(self.BASE_DIR))

        # plt.style.use('fivethirtyeight')
        # # convert the dataframe to nparray
        # df = pd.read_csv('{}/data/location.csv'.format(self.BASE_DIR))
        # df = df.tail(100)
        # data = df.filter(['Number of cases'])
        # dataset = data.values
        # # get the number of rows to train the model
        # training_data_len = math.ceil(len(dataset) * 0.8)
        # print(data)
        # # Scaling the data
        # scaler = MinMaxScaler(feature_range=(0, 1))
        # scaled_data = scaler.fit_transform(dataset)
        #
        # scaled_data
        # # Create the training dataset
        # # create the scaled training dataset
        # train_data = scaled_data[0:training_data_len, :]
        # # Split the data into x_train and y_train datasets
        # x_train = []
        # y_train = []
        #
        # for i in range(60, len(train_data)):
        #     x_train.append(train_data[i - 60:i, 0])
        #     y_train.append(train_data[i, 0])
        # model = load_model('{}/data/model.h5'.format(self.BASE_DIR))
        #
        # # Create the testing dataset
        # test_data = scaled_data[training_data_len - 60:, :]
        # # create the x_test and y_test datasets
        # x_test = []
        # y_test = dataset[training_data_len:, :]
        # for i in range(60, len(test_data)):
        #     x_test.append(test_data[i - 60:i, 0])
        #
        # # convert the data to nparray
        # x_test = np.array(x_test)
        # # Reshape the data
        # x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        # # Get the models predicted disease cases
        # predictions = model.predict(x_test)
        # predictions = scaler.inverse_transform(predictions)
        # # Get the root mean squared error
        # rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
        # rmse
        # # Plot the data
        # train = data[:training_data_len]
        # valid = data[training_data_len:]
        # valid['predictions'] = predictions
        # # visualize the data
        # plt.figure(figsize=(16, 8))
        # plt.title('{} prediction for {}'.upper().format(self.disease.upper(), self.location.upper()))
        # plt.xlabel('date')
        # plt.ylabel('{} cases'.format(self.disease))
        # plt.plot(train['Number of cases'])
        # plt.plot(valid[['Number of cases', 'predictions']])
        # plt.show()
        figure = io.BytesIO()
        plt.savefig(figure, format="png")
        content_file = ImageFile(figure)
        content_file = ContentFile(figure.getvalue())
        user_obj = User.objects.get(email=user)
        try:
            img_obj = Images.objects.get(user=user_obj)
            img_obj.image.save("image_file.png", content_file)
            img_obj.save()
        except:
            plot_instance = Images(user=user_obj)
            plot_instance.image.save("image_file.png", content_file)
            plot_instance.save()

        # plt.savefig('{}/data/{}disease.jpg'.format(self.BASE_DIR, user))

#
#
# ml = ML(disease='cholera', location='machakos')
# ml.generate_csv()
# ml.generate_predictions('test')
# print(BASE_DIR)
