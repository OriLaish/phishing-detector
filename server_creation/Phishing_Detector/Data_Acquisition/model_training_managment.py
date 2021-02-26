import numpy as np
import pandas as pd
import sklearn.model_selection as skms
import tensorflow as tf
import tensorflowjs as tfjs
from .models import Web_scraping_data, Models_Helper

class traineble_data:
    def __init__():
        columns = ['having_IP_Address', 'URL_Length', 'Shortining_Service',
        'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
        'having_Sub_Domain', 'Favicon', 'port', 'HTTPS_token', 'Request_URL',
        'URL_of_Anchor', 'Links_in_tags', 'SFH', 'Iframe', 'Result']
        self.df = pd.DataFrame()
    
    def preprocess():
        pass

        


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
        that function processing the traineble data available in the database and returns theb 
        """
        untrained_urls = Web_scraping_data.objects.filter(is_trained=False)
        min_amount_of_trainebles = min(untrained_urls.filter(is_phishing=True).count(), untrained_urls.filter(is_phishing=False).count())
        data = traineble_data()
        if min_amount_of_trainebles < Model_Training_Helper.MIN_TRAINEBLE_LINES :
            return None
        for line in untrained_urls.filter(is_phishing=True)[:min_amount_of_trainebles]:
            Model_Training_Helper.enter_line_to_data(line, data)
        for line in untrained_urls.filter(is_phishing=False)[:min_amount_of_trainebles]:
            Model_Training_Helper.enter_line_to_data(line, data)
            

    
    @staticmethod
    def enter_line_to_data(line, data):
        features = [int(f) for f in line.features.split(",")]
        features.append(1 if line.is_phishing else -1)
        data.df
        
        



    @staticmethod
    def train_model():
        """
        train the opened model and save it
        """
        model = Model_Training_Helper.open_model()
        data = Model_Training_Helper.process_training_data()
        if data == None:
            return False
        early_stopping = tf.keras.callbacks.EarlyStopping(monitor='loss', min_delta=0.05, patience=5)  # to prevent over fit
        model.fit(data.x_train, data.y_train, epochs=10, batch_size=100, validation_data=(data.x_val, data.y_val), verbose=1, callbacks=[early_stopping])
        Model_Training_Helper.save_model(model)
        return  True




