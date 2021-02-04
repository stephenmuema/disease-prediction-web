import io
import os
from time import sleep

import pandas as pd
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from matplotlib import pyplot as plt
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import load_model

from accounts.models import User
from djangoHealthAnalytics.settings import BASE_DIR
from pathlib import Path

from pages.models import Images


class ML:
    BASE_DIR = Path(__file__).resolve().parent.parent
    location = disease = None

    def __init__(self, location, disease):
        self.location = location
        self.disease = disease


    def generate_csv(self):
        # Code to Rearrange and sort data to desired location and disease
        # The code also counts the disease cases
        # At the end it creates a new csv file containing the new data
        # get all data from csv file
        data = pd.read_csv('{}/data/Diseases.csv'.format(self.BASE_DIR))
        # set date as the index
        data = data.set_index('date')
        # get disease and location specific data
        # print(type(self.disease))
        # disease = data[data.disease == "{}".format(self.disease)]
        # location = disease[disease.location == "{}".format(self.location)]
        disease = data[data.disease == self.disease]
        location = disease[disease.location == self.location]

        # Count disease cases in the specific location
        df = location.groupby('date').count()
        df = df.disease.to_frame()
        df = df.rename(columns={"disease": "Number of cases"})
        df

        # Exporting the new disease and location specific data to a csv
        df.to_csv(r'{}/data/location.csv'.format(self.BASE_DIR), index=True, header=True)
        df

    def generate_predictions(self, user):

        plt.style.use('fivethirtyeight')
        # convert the dataframe to nparray
        df = pd.read_csv('{}/data/location.csv'.format(self.BASE_DIR))
        df = df.tail(100)
        data = df.filter(['Number of cases'])
        dataset = data.values
        # get the number of rows to train the model
        training_data_len = math.ceil(len(dataset) * 0.8)
        print(data)
        # Scaling the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)

        scaled_data
        # Create the training dataset
        # create the scaled training dataset
        train_data = scaled_data[0:training_data_len, :]
        # Split the data into x_train and y_train datasets
        x_train = []
        y_train = []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i - 60:i, 0])
            y_train.append(train_data[i, 0])
        model = load_model('{}/data/model.h5'.format(self.BASE_DIR))

        # Create the testing dataset
        test_data = scaled_data[training_data_len - 60:, :]
        # create the x_test and y_test datasets
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range(60, len(test_data)):
            x_test.append(test_data[i - 60:i, 0])

        # convert the data to nparray
        x_test = np.array(x_test)
        # Reshape the data
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        # Get the models predicted disease cases
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)
        # Get the root mean squared error
        rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
        rmse
        # Plot the data
        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid['predictions'] = predictions
        # visualize the data
        plt.figure(figsize=(16, 8))
        plt.title('{} prediction for {}'.upper().format(self.disease.upper(), self.location.upper()))
        plt.xlabel('date')
        plt.ylabel('{} cases'.format(self.disease))
        plt.plot(train['Number of cases'])
        plt.plot(valid[['Number of cases', 'predictions']])
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
