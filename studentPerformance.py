import pickle
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_model():
    with open(r'C:\Users\y\Desktop\Academics\FullStackDS\machineLearning\linearRegression.pkl', 'rb') as file:
        model, scaler, le = pickle.load(file)
    return model, scaler, le

def preprocessing_input(data, scaler, le):
    print("data is", data)
    data['Extracurricular Activities'] = le.fit_transform([data['Extracurricular Activities']])[0]
    print("data1q is", data)
    df = pd.DataFrame([data])
    print("dataqwqw is", data)
    df_transformed = scaler.transform(df)
    return df_transformed

def predict_data(data):
    model, scaler, le = load_model()
    df_transformed = preprocessing_input(data, scaler, le)
    prediction = model.predict(df_transformed)
    return prediction

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
        user_data = {'Hours Studied': hours,
                    'Previous Scores': prev,
                    'Extracurricular Activities': ext,
                    'Sleep Hours': sleep,
                    'Sample Question Papers Practiced': sample
                    }
        prediction = predict_data(user_data)
        print(prediction)
        st.success(f"Your prediction result is: {prediction}")

if __name__ == "__main__":
    main()