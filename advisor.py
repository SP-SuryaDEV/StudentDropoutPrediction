import streamlit as st
import pandas as pd
import PIL
import sqlite3
import os

class StudentReportMaker:
    def __init__(self):
        pass
    
    @staticmethod
    @st.cache_data
    def load_data(file):
        return pd.read_csv(file)

    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            folder_path = "student_databases"
            os.makedirs(folder_path, exist_ok=True)
            db_path = os.path.join(folder_path, db_file)
            conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            st.error(e)
        return conn

    @staticmethod
    def create_table(conn, student_name):
        try:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS student_info (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            student_name TEXT NOT NULL,
                            advice TEXT,
                            motivation TEXT,
                            study_plan TEXT,
                            study_materials TEXT
                        )''')
            conn.commit()
        except sqlite3.Error as e:
            st.error(e)

    @staticmethod
    def insert_data(conn, student_name, advice, motivation, study_plan, study_materials):
        try:
            c = conn.cursor()
            c.execute("DELETE FROM student_info")
            advice_text = f" {advice}" if advice else ""
            motivation_text = f" {motivation}" if motivation else ""
            study_plan_text = "\n".join([f"{line.strip()}" for line in study_plan.split('\n')]) if study_plan else ""
            study_plan_text = f"\n{study_plan_text}" if study_plan_text else ""
            materials_text = "\n".join([f"{line}" for line in study_materials.split('\n') if line.strip()]) if study_materials else ""
            c.execute('''INSERT INTO student_info (student_name, advice, motivation, study_plan, study_materials)
                         VALUES (?, ?, ?, ?, ?)''', (student_name, advice_text, motivation_text, study_plan_text, materials_text))
            conn.commit()
            st.success("Data inserted successfully!")
        except sqlite3.Error as e:
            st.error(e)

    @staticmethod
    def display_student_details(df, student_name, conn):
        st.title(f"Details Of {student_name} : ")
        student_data = df[df["Name"] == student_name].squeeze()
        Image_Place = "MK.jpeg"
        image = PIL.Image.open(Image_Place)
        resized_image = image.resize((200,200))
        st.image(resized_image)
        st.markdown('<style>div.stDataFrame > div[data-baseweb="card"] {border: 1px solid #ccc; border-radius: 5px; padding: 10px;}</style>', unsafe_allow_html=True)
        with st.expander("**General Information**", expanded=False):
            try:
                st.write(f"**Name:** {student_data['Name']}")
                st.write(f"**Course:** {student_data['Course']}")
                st.write(f"**Age:** {student_data['Age at enrollment']}")
                st.write(f"**Resident:** {student_data['Displaced']}")
            except KeyError as e:
                st.warning(f"Column '{e.args[0]}' not found. Please check the uploaded file.")

        with st.expander("**Financial Information**", expanded=False):
            try:
                st.write(f"**Does the Student have any debt in his name:** {student_data['Debtor']}")
                st.write(f"**Has the Student Paid the due fees:** {student_data['Tuition fees up to date']}")
                st.write(f"**Does the student have any scholarly Benefits:** {student_data['Scholarship holder']}")
            except KeyError as e:
                st.warning(f"Column '{e.args[0]}' not found. Please check the uploaded file.")

        with st.expander("**Academic Information**", expanded=False):
            try:
                st.write(f"**1st Sem GPA:** {student_data['Curricular units 1st sem (grade)']}")
                st.write(f"**2nd Sem GPA:** {student_data['Curricular units 2nd sem (grade)']}")
                #st.write(f"**1st Sem No of Units Allocated:** {student_data['Curricular units 1st sem (approved)']}")
                #st.write(f"**2nd Sem No of Units Allocated:** {student_data['Curricular units 2nd sem (approved)']}")
            except KeyError as e:
                st.warning(f"Column '{e.args[0]}' not found. Please check the uploaded file.")

        with st.expander("**Additional Information**", expanded=False):
            try:
                st.write(f"**Student's General Remark:** {student_data['Student Remark']}")
                st.write(f"**Extracurricular Activities:** {student_data['Hobbies']}")
                st.write(f"**If same continues What will happen? :** {student_data['predicted_target']}")
            except KeyError as e:
                st.warning(f"Column '{e.args[0]}' not found. Please check the uploaded file.")

        st.warning("Please Give Priority Care for Students in need")
        st.success("Upon giving individual reviews for the prioritized students, suggestions can be provided to other students as well")

        with st.expander("**Guidance Track**", expanded=True):
            st.write("Please guide the students after reviewing their profile.")
            st.subheader("Advice:")
            advice_placeholder = st.empty()
            advice = advice_placeholder.text_area("Write your advice here", height=100)
            st.subheader("Motivation Message:")
            motivation_templates = [
                "You have great potential. Keep pushing forward!",
                "Believe in yourself. You can achieve anything you set your mind to!",
                "Success is not final, failure is not fatal: It is the courage to continue that counts."
            ]
            selected_motivation = st.selectbox("Select Motivation Template", ['Choose a template'] + motivation_templates)
            if selected_motivation == 'Choose a template':
                motivation_placeholder = st.empty()
                motivation = motivation_placeholder.text_area("Write your motivation message here", height=100)
            else:
                motivation_placeholder = st.empty()
                motivation = motivation_placeholder.text_area("Write your motivation message here", value=selected_motivation, height=100)
            st.subheader("Study Plan:")
            study_plan_templates = [
                "1. Review lecture notes daily\n2. Complete assignments on time\n3. Seek help when needed",
                "1. Break down tasks into smaller chunks\n2. Set specific goals for each study session\n3. Stay consistent and focused",
                "1. Prioritize tasks based on importance\n2. Use techniques like the Pomodoro method for efficient studying\n3. Take breaks to recharge"
            ]
            selected_study_plan = st.selectbox("Select Study Plan Template", ['Choose a template'] + study_plan_templates)
            if selected_study_plan == 'Choose a template':
                study_plan_placeholder = st.empty()
                study_plan = study_plan_placeholder.text_area("Write your study plan here in numbered", height=100)
            else:
                study_plan_placeholder = st.empty()
                study_plan = study_plan_placeholder.text_area("Write your study plan here", value=selected_study_plan, height=100)
            st.subheader("Study Materials:")
            st.write("Provide URLs in the format '1. URL'. For example:")
            st.write("```1.(Your Drive Link)```")
            st.write("```2.(Your Drive Link)```")
            material_urls_placeholder = st.empty()
            material_urls = material_urls_placeholder.text_area("Enter URLs for study materials (one per line)", height=100)
            st.warning("Before Hitting *confirm* Check once again for any changes ")
            if st.button("Clear All Text"):
                advice = advice_placeholder.text_area("Write your advice here")
                motivation = motivation_placeholder.text_area("Write your motivation message here")
                study_plan = study_plan_placeholder.text_area("Write your study plan here")
                material_urls = material_urls_placeholder.text_area("Enter URLs for study materials (one per line)")
            if st.button("Confirm"):
                advice_text = f"Review: {advice}" if advice else ""
                motivation_text = f"Personal Advice : {motivation}" if motivation else ""
                study_plan_text = f"Study Plan:\n{study_plan}" if study_plan else ""
                materials_text = "Study Materials:\n" + "\n".join([f"{line}" for line in material_urls.split('\n') if line.strip()]) if material_urls else ""
                data = (student_name, advice_text, motivation_text, study_plan_text, materials_text)
                StudentReportMaker.insert_data(conn, *data)
                st.warning("Please Press *Clear All Text* to erase the contents before moving on to next person")

    def run(self):
        st.title("Student Report Maker")
        photo_placeholder = st.empty()
        uploaded_file = 'dropout.csv'
        if uploaded_file is not None:
            df = StudentReportMaker.load_data(uploaded_file)
            st.subheader("Select a student:")
            selected_name = st.selectbox("Select Name", [None] + list(df["Name"].unique()))
            if selected_name is not None:
                db_file = f"{selected_name}.db"
                conn = StudentReportMaker.create_connection(db_file)
                StudentReportMaker.create_table(conn, selected_name)
                StudentReportMaker.display_student_details(df, selected_name, conn)

if __name__ == "__main__":
    app = StudentReportMaker()
    app.run()
