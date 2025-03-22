import pickle
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pymysql

def build_connection():
    # Database connection parameters
    host = "localhost"
    port = 3306
    user = "root"
    password = "Manthan@456"
    database = "student"
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("Connected to MySQL database")        
        # Perform database operations here
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
    finally:
        return connection
    
def insert(cnx, query):
    cursor = cnx.cursor()
    cursor.execute(query)
    cnx.commit()

def load_model():
    with open(r'linearRegression.pkl', 'rb') as file:
        model, scaler, le = pickle.load(file)
    return model, scaler, le

def preprocessing_input(data, scaler, le):
    print("data is", data)
    data['Extracurricular Activities'] = int(le.fit_transform([data['Extracurricular Activities']])[0])
    print("data1q is", data)
    df = pd.DataFrame([data])
    print("dataqwqw is", data)
    df_transformed = scaler.transform(df)
    return df_transformed, df

def predict_data(data):
    model, scaler, le = load_model()
    df_transformed, df = preprocessing_input(data, scaler, le)
    prediction = model.predict(df_transformed)
    df['Performance_Index'] = int(prediction)
    return prediction, df

def main():
    st.title("Student Performance Prediction.")
    st.write("Enter your data to get the prediction for your preformance.")

    hours = st.number_input("Hours studied")
    prev = st.number_input("Previous Score")
    ext = str(st.selectbox("Extras", ['Yes', 'No']))
    print(f"ext is: {ext}")
    sleep = st.number_input("Sleep hours")
    sample = st.number_input("sample studied")
    if st.button("predict"):
        user_data = {'Hours Studied': int(hours),
                    'Previous Scores': int(prev),
                    'Extracurricular Activities': ext,
                    'Sleep Hours': int(sleep),
                    'Sample Question Papers Practiced': int(sample)
                    }
        prediction, df = predict_data(user_data)
        final_values = []
        for i in df.iloc[0].values:
            final_values.append(int(i))
        query = f"INSERT INTO performance (Hours_Studied,Previous_Scores,Extracurricular_Activities,Sleep_Hours,Sample_Question_Papers_Practiced,Performance_Index) VALUES {tuple(final_values)}"
        cnx = build_connection()
        print(f"QUERY IS: {query}")
        insert(cnx, query)
        print(prediction)
        st.success(f"Your prediction result is: {prediction}")

if __name__ == "__main__":
    main()