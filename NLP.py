from importlib import reload
from imp import reload
import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model, Sequential
from keras import initializers, regularizers, constraints, optimizers, layers
from keras.callbacks import EarlyStopping, ModelCheckpoint
from langdetect import detect
import pickle
import nltk
import numpy as np
import json
import underthesea

from settings import CLASSIFIED_RESULT_FN

# nltk.download('words')
# nltk.download('wordnet')
# nltk.download('stopwords')
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()
max_features = 100000
maxlen = 150


class NLP:
    def __init__(self, tokenizer_path, model_path):
        self.tokenizer, self.model = self.load_tokenizer_and_model(tokenizer_path, model_path)

    @staticmethod
    def clean_text(text):
        text = re.sub('.*♥+.*', 'fuck', text)
        text = re.sub('.*♡+.*', ' ', text)
        text = re.sub('.*🍌+.*', ' ', text)
        text = re.sub(r'[^\w\s]', '', text, re.UNICODE)
        text = text.lower()
        text = [lemmatizer.lemmatize(token) for token in text.split(" ")]
        text = [lemmatizer.lemmatize(token, "v") for token in text]
        text = [word for word in text if word not in stop_words]
        text = " ".join(text)
        return text

    @staticmethod
    def create_data_to_classify(comments):
        test_data = []
        for comment in comments:
            comment = comment.strip()
            try:
                lang = detect(comment)
                if lang == "en":
                    test_data.append(comment)
            except:
                test_data.append(comment)
        reviews = pd.DataFrame({'review': test_data})

        return reviews

    @staticmethod
    def load_tokenizer_and_model(tokenizer_path, model_path):
        with open(tokenizer_path, "rb") as f:
            tokenizer = pickle.load(f)
            f.close()

        embed_size = 128
        model = Sequential()
        model.add(Embedding(max_features, embed_size))
        model.add(Bidirectional(LSTM(32, return_sequences=True)))
        model.add(GlobalMaxPool1D())
        model.add(Dense(20, activation="relu"))
        model.add(Dropout(0.05))
        model.add(Dense(1, activation="sigmoid"))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        model.load_weights(model_path)

        return tokenizer, model

    def classify_comments(self, json_path):
        comments = []
        # data2 = []
        with open(json_path, mode="r", encoding='utf8') as f:
            data2 = json.load(f)
            for x in data2:
                x['Total'] = len(x['comments'])
                for comment in x['comments']:
                    if " …  Expand " in comment:
                        comment = comment[:-10]
                    comments.append(comment)
                data = self.create_data_to_classify(comments)
                data['test_review'] = data.review.apply(lambda x: self.clean_text(x))
                list_sentences_test = data["test_review"]
                list_tokenized_test = self.tokenizer.texts_to_sequences(list_sentences_test)
                X_te = pad_sequences(list_tokenized_test, maxlen=maxlen)
                # print(X_te)
                prediction = self.model.predict(X_te)
                for i in range(len(prediction)):
                    if prediction[i] > 0.5:
                        prediction[i] = True
                    else:
                        prediction[i] = False
                x['Positive'] = str(int(np.sum(prediction)))
                comments = []
            f.close()
        # print (data2)
        with open(CLASSIFIED_RESULT_FN, mode="w", encoding='utf8') as fi:
            json.dump(data2, fi)
            fi.close()
