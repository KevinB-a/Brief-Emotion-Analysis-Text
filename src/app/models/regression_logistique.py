# Import of all the libraries we need to work

import sys
from altair.vegalite.v4.api import value
sys.path.insert(0, "/home/apprenant/Documents/Brief-Emotion-Analysis-Text/")
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, roc_curve, auc

from src.functions import *
import joblib
filename = 'regression_logistique.sav'

#### Etape 1

emotion_final, text_emotion = import_database()

# Database 1

label_encoding(emotion_final, [(emotion_final['label'] == "sadness") | (emotion_final['label'] == "fear") | (emotion_final['label'] == "anger"), (emotion_final['label'] == "love") | (emotion_final['label'] == "surprise") | (emotion_final['label'] == "happy")], [0, 1])

X_train, X_test, y_train, y_test = variables_selection(emotion_final['text'], emotion_final['binary_emotion'])
vectorizer = vectorize_data(CountVectorizer, emotion_final['text'], None)
text_train, text_test = transform_training_data(vectorizer, X_train, X_test)
model = define_model(LogisticRegression(), text_train, y_train)
y_pred, dataframe = predict_model(model, text_test, X_test)
accuracy1 = calculate_score(model, text_test, y_test)

# Database 2

label_encoding(text_emotion, [(text_emotion['label'] == "empty") | (text_emotion['label'] == "sadness") | (text_emotion['label'] == "worry") | (text_emotion['label'] == "hate") | (text_emotion['label'] == "boredom") | (text_emotion['label'] == "anger"), (text_emotion['label'] == "enthusiasm") | (text_emotion['label'] == "neutral") | (text_emotion['label'] == "surprise") | (text_emotion['label'] == "love") | (text_emotion['label'] == "fun") | (text_emotion['label'] == "happiness") | (text_emotion['label'] == "relief")] ,[0, 1])

X_train2, X_test2, y_train2, y_test2 = variables_selection(text_emotion['text'], text_emotion['binary_emotion'])
vectorizer2 = vectorize_data(CountVectorizer, text_emotion['text'], None)
text_train2, text_test2 = transform_training_data(vectorizer2, X_train2, X_test2)
model2 = define_model(LogisticRegression(), text_train2, y_train2)
y_pred2, dataframe2 = predict_model(model2, text_test2, X_test2)
accuracy2 = calculate_score(model2, text_test2, y_test2)


#### Etape 2

new_emotion_text = concat_databases(emotion_final, text_emotion)
new_emotion_text["label"].replace({'happiness': 'happy'}, inplace=True)

label_encoding(new_emotion_text, [(new_emotion_text['label'] == "empty") | (new_emotion_text['label'] == "sadness") | (new_emotion_text['label'] == "worry") | (new_emotion_text['label'] == "hate") | (new_emotion_text['label'] == "boredom") | (new_emotion_text['label'] == "anger") | new_emotion_text['label'] == "fear", (new_emotion_text['label'] == "enthusiasm") | (new_emotion_text['label'] == "neutral") | (new_emotion_text['label'] == "surprise") | (new_emotion_text['label'] == "love") | (new_emotion_text['label'] == "fun") | (new_emotion_text['label'] == "happy") | (new_emotion_text['label'] == "relief")] ,[0, 1])

X_train3, X_test3, y_train3, y_test3 = variables_selection(new_emotion_text['text'], new_emotion_text['binary_emotion'])
vectorizer3 = vectorize_data(CountVectorizer, new_emotion_text['text'], None)
text_train3, text_test3 = transform_training_data(vectorizer3, X_train3, X_test3)
model3 = define_model(LogisticRegression(), text_train3, y_train3)
y_pred3, dataframe3 = predict_model(model3, text_test3, X_test3)
accuracy3 = calculate_score(model3, text_test3, y_test3)


#### Etape 3

X, y, X_test4, y_test4 = step3_variables(emotion_final, text_emotion)
vectorizer4 = vectorize_data(CountVectorizer, X, X_test4, 1)
text_train4, text_test4 = transform_training_data(vectorizer4, X, X_test4)
model4 = define_model(LogisticRegression(), text_train4, y)
y_pred4, dataframe4 = predict_model(model4, text_test4, X_test4)
accuracy4 = calculate_accuracy_score(y_test4, y_pred4)

joblib.dump([dataframe, accuracy1, dataframe2, accuracy2, dataframe3, accuracy3, dataframe4, accuracy4, y_pred, y_pred2, y_pred3, y_test, y_test2, y_test3], filename)

