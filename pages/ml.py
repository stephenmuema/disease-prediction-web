class ML:
    def __init__(self):
        pass
    def generate_predictions(self):
        import pandas as pd
        from matplotlib import pyplot as plt
        import numpy as np
        from tensorflow.keras.models import load_model
        plt.style.use('fivethirtyeight')
        # convert the dataframe to nparray
        df = pd.read_csv('/content/location.csv')
        df = df.tail(100)
        data = df.filter(['Number of cases'])
        dataset = data.values
        model = load_model('/content/model.h5')
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
        plt.title('Model')
        plt.xlabel('date')
        plt.ylabel('Disease cases')
        plt.plot(train['Number of cases'])
        plt.plot(valid[['Number of cases', 'predictions']])
        # plt.show()
        plt.savefig('disease.jpg')