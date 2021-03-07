import numpy as np
import pandas as pd
import sklearn.model_selection as skms
import tensorflow as tf
import tensorflowjs as tfjs
from .models import Web_scraping_data, Models_Helper


class traineble_data:
    
    COLUMNS = ['having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'Favicon', 'port', 'HTTPS_token', 'Request_URL',
        'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Iframe', 'Result']

    NUM_OF_FEATURES = len(COLUMNS)  # updating dimension size

    def __init__(self):
        self.df = pd.DataFrame(columns=traineble_data.COLUMNS)
    
    def preprocess(self):
        # splitting features from classes(results)
        print("in preprocess")
        #x_data = self.df.iloc[0: -1, 0: traineble_data.NUM_OF_FEATURES-1]  # feature data
        #y_data = self.df.iloc[0: -1, traineble_data.NUM_OF_FEATURES-1]  # result data

        # splitting data to training, validation & testing
        #x_temp, self.x_test, y_temp, self.y_test = skms.train_test_split(x_data, y_data, test_size=0.09, random_state=18)
        #self.x_train, self.x_val, self.y_train, self.y_val = skms.train_test_split(x_temp, y_temp, test_size=0.1, random_state=27)

class Model_Training_Helper:
    MIN_TRAINEBLE_LINES = 60  

    @staticmethod 
    def open_model():
        """
        open and return model
        """
        return tfjs.converters.load_keras_model("Saved_Model\\model.json")

    @staticmethod
    def save_model(model):
        """
        saves the retrained model in the required place
        """
        tfjs.converters.save_keras_model(model, "Saved_Model")

    @staticmethod
    def process_training_data():
        """
        #that function processing the traineble data available in the database and returns theb 
        """
        #untrained_urls = Web_scraping_data.objects.filter(is_trained=False)
        untrained_urls = Web_scraping_data.objects.filter(id=1)
        print(untrained_urls[0].features)
        min_amount_of_trainebles = min(untrained_urls.filter(is_phishing=True).count(), untrained_urls.filter(is_phishing=False).count())
        print(min_amount_of_trainebles)
        data = traineble_data()
        Model_Training_Helper.enter_line_to_data(untrained_urls[0],data)
        Model_Training_Helper.enter_line_to_data(untrained_urls[0],data)
        
        #if min_amount_of_trainebles < Model_Training_Helper.MIN_TRAINEBLE_LINES :
        #    return None
        for line in untrained_urls.filter(is_phishing=True)[:min_amount_of_trainebles]:
            Model_Training_Helper.enter_line_to_data(line, data)
        for line in untrained_urls.filter(is_phishing=False)[:min_amount_of_trainebles]:
            Model_Training_Helper.enter_line_to_data(line, data)
        print(data.df)
        #data.preprocess()
        return data
            

    
    @staticmethod
    def enter_line_to_data(line, data):
        features = [int(f) for f in line.features.split(",")]
        features.append(1 if line.is_phishing else -1)
        data.df = data.df.append(dict(zip(data.df.columns, features)), ignore_index=True)
        
        



    @staticmethod
    def train_model():
        """
        #train the opened model and save it
        """
        model = Model_Training_Helper.open_model()
        data = Model_Training_Helper.process_training_data()
        if data == None:
            print("not working")
            return False
        #early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.05, patience=5)  # to prevent over fit
        #model.fit(data.x_train, data.y_train, epochs=10, batch_size=100, validation_data=(data.x_val, data.y_val), verbose=1, callbacks=[early_stopping])
        #Model_Training_Helper.save_model(model)
        print("working")
        print(data.df)
        return  True
