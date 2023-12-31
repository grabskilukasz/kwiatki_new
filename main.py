import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

df = pd.read_csv('Iris.csv')
X = df.drop(['Id', 'Species'], axis=1)
y = df['Species']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

knc = KNeighborsClassifier(n_neighbors=3)
knc.fit(X_train,y_train)
y_pred = knc.predict(X_test)
acc_knn = metrics.accuracy_score(y_pred,y_test)
print('The accuracy of the KNN is', acc_knn)
print(X_test[:1])

with open('knn_model.pkl', 'wb') as file:
    pickle.dump(knc, file)


class IrisItem(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.post("/predict")
def predict_species(item: IrisItem):
    try:
        # Przygotuj dane wejściowe dla modelu
        input_data = [[item.sepal_length, item.sepal_width, item.petal_length, item.petal_width]]

        # Dokonaj predykcji przy użyciu wcześniej wytrenowanego modelu
        prediction = knc.predict(input_data)

        # Zwróć wynik predykcji
        return {"predicted_species": prediction[0]}

    except Exception as e:
        # W przypadku błędu zwróć informację o błędzie
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/1")
def root():
    return {"Hello": "World"}