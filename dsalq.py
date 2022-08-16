import pyodbc
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
# DotEnv para usar variables de entorno
import os
from dotenv import load_dotenv

load_dotenv()
url_connection = os.getenv('URL_CONNECTION')
# Connection string to your SQL Server instance
conn_str = pyodbc.connect(url_connection)

query_str = 'SELECT Year, Month, Day, Rentalcount, Weekday, Holiday, Snow FROM dbo.rental_data'

df = pandas.read_sql(sql=query_str, con=conn_str)
# print("Data frame:", df)

# Filtre las columnas de la trama de datos para quitar las que no queremos usar en el entrenamiento. Rentalcount no debe incluirse, ya que es el destino de las predicciones.
columns = df.columns.tolist()
columns = [c for c in columns if c not in ["Year", "Rentalcount"]]

# print("Training set:", df[columns])

# Store the variable we'll be predicting on.
target = "Rentalcount"

# Generate the training set.  Set random_state to be able to replicate results.
train = df.sample(frac=0.8, random_state=1)

# Select anything not in the training set and put it in the testing set.
test = df.loc[~df.index.isin(train.index)]

# Print the shapes of both sets.
print("Training set shape:", train.shape)
print("Testing set shape:", test.shape)

# Initialize the model class.
lin_model = LinearRegression()

# Fit the model to the training data.
lin_model.fit(train[columns], train[target])

# Generate our predictions for the test set.
lin_predictions = lin_model.predict(test[columns])
print("Predictions:", lin_predictions)

# Compute error between our test predictions and the actual values.
lin_mse = mean_squared_error(lin_predictions, test[target])
print("Computed error:", lin_mse)