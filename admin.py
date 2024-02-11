import pickle
import streamlit as st
import pandas as pd
import numpy as np
import os
import random
from mail import SendEmail
import string

class Uploader_UI:
    def __init__(self):
        # Load the trained model
        with open('drop.pkl', 'rb') as f:
            self.model = pickle.load(f)

    # Function to preprocess the uploaded CSV file
    def preprocess_data(self, file):
        df = pd.read_csv(file)
        return df

    # Function to reverse mapping
    def reverse_mapping(self, mapping):
        reverse = {col: {v: k for k, v in col_mapping.items()} for col, col_mapping in mapping.items()}
        return reverse

    # Function to make predictions and generate result CSV
    def make_predictions_and_generate_csv(self, df):
        # Map categorical variables to numerical values
        mapping = {
            'Displaced': {'native': 0, 'immigrant': 1},
            'Debtor': {'no': 0, 'yes': 1},
            'Tuition fees up to date': {'not paid': 0, 'paid': 1},
            'Gender': {'male': 0, 'female': 1},
            'Scholarship holder': {'no': 0, 'yes': 1}
        }

        for col, col_mapping in mapping.items():
            df[col] = df[col].map(col_mapping)

        # Make predictions
        predictions = self.model.predict(df.drop(columns=['Name','Course','Email','Student Remark','Hobbies']))  # Drop 'Name' column for prediction
        # Convert probabilities to binary predictions
        binary_predictions = (predictions > 0.5).astype(int)

        # Reverse mapping to convert binary predictions back to original format
        reverse_map = self.reverse_mapping(mapping)
        for col, col_mapping in reverse_map.items():
            df[col] = df[col].map(col_mapping)

        # Add predicted values as a new column
        df['predicted_target'] = binary_predictions

        # Convert binary predictions to "dropout" and "graduate"
        df['predicted_target'] = np.where(df['predicted_target'] == 0, 'dropout', 'graduate')

        # Save uploaded DataFrame to CSV without any conversion
        df.to_csv('result.csv', index=False)

        # Save dropout students to dropout.csv
        dropout_df = df[df['predicted_target'] == 'dropout']
        dropout_df.to_csv('dropout.csv', index=False)

        # Create students.csv with Name and Password columns
        student_names = df['Name'].tolist()
        students_email = df['Email'].tolist()
        random_passwords = [''.join(random.choices(string.ascii_letters + string.digits, k=5)) for _ in range(len(student_names))]
        students_df = pd.DataFrame({'Name': student_names,'Email': students_email ,'Password': random_passwords})
        students_df.to_csv('students.csv', index=False)

    # Streamlit app
    def run(self):
        uploaded_file = st.file_uploader("", type=["csv"])

        if uploaded_file is not None:
            df = self.preprocess_data(uploaded_file)

            # Ensure all required columns are present
            required_columns = ['Name','Course','Email','Displaced', 'Debtor', 'Tuition fees up to date', 'Gender', 'Scholarship holder',
                                'Age at enrollment', 'Curricular units 1st sem (approved)',
                                'Curricular units 1st sem (grade)', 'Curricular units 2nd sem (approved)',
                                'Curricular units 2nd sem (grade)','Student Remark','Hobbies']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Missing columns: {', '.join(missing_columns)}")
                st.error(f"Columns in uploaded file: {', '.join(df.columns)}")
                return

            st.write(df)

            # Button for making predictions
            if st.button("Make Predictions"):
                self.make_predictions_and_generate_csv(df)
                st.success("Prediction completed! Result.csv, dropout.csv, and students.csv generated.")

            # Display "Dropout List" button after predictions are made
            if os.path.isfile('dropout.csv'):
                if st.button("Dropout List"):
                    dropout_df = pd.read_csv('dropout.csv')
                    st.write(dropout_df)
                    # Close the displayed dropout.csv file
                    if st.button("Close Dropout List"):
                        os.remove('dropout.csv')

            if os.path.isfile('students.csv'):
                if st.button("Send Password Update"):
                    Student_Update_df = pd.read_csv('students.csv')
                    emails = Student_Update_df['Email']
                    
                    for ind, email in enumerate(emails):
                        studentEmail = SendEmail(email)
                        studentEmail.MessageUpdate(Student_Update_df['Name'][ind], Student_Update_df['Password'][ind])

if __name__ == "__main__":
    uploader_ui = Uploader_UI()
    uploader_ui.run()
