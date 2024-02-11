import streamlit as st
import sqlite3
import pandas as pd

class StudentInformationViewer:
    def __init__(self):
        self.db_file = None
        self.conn = None
        self.students_df = pd.read_csv("students.csv")

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
        except sqlite3.Error:
            pass

    def get_student_info(self, student_name):
        try:
            c = self.conn.cursor()
            c.execute('''SELECT * FROM student_info WHERE student_name=?''', (student_name,))
            rows = c.fetchall()
            return rows
        except sqlite3.Error:
            return None

    def run(self):
        st.title("Explore Your Response")
        student_name = st.text_input("Enter Student Name:")
        password_ = st.text_input("Personal Password", type="password")
        enter = st.button("Explore")

        if enter:
            if student_name in self.students_df['Name'].tolist():
                correct_password = self.students_df.loc[self.students_df['Name'] == student_name, 'Password'].iloc[0]
                if password_ == correct_password:
                    self.db_file = f"student_databases/{student_name}.db"
                    self.create_connection(self.db_file)

                    if self.conn:
                        st.subheader(f"Information for {student_name}:")

                        rows = self.get_student_info(student_name)

                        if rows is not None:
                            if rows:
                                for row in rows:
                                   with st.expander("You Have An Update From Your Advisor!!! Click To View More", expanded=False): 
                                    st.warning("Note : Please review the entire report for insights on your personal growth and development. Your advisors have invested their time in crafting it. Additionally, refer to the materials provided and follow the prescribed solutions and plans.")
                                    st.write("----")
                                    st.markdown(f"<h6>{row[2]}</h6>", unsafe_allow_html=True)
                                    st.write("******************")
                                    st.markdown(f"<h6>{row[3]}</h6>", unsafe_allow_html=True)
                                    st.write("******************")
                                    
                                    study_plan = row[4]
                                    if study_plan:
                                        for i, line in enumerate(study_plan.split('\n'), start=1):
                                            st.markdown(f"<h6>{line}</h6>", unsafe_allow_html=True)
                                    st.write("***********")

                                    links = row[5]
                                    if links:
                                        for i, lines in enumerate(links.split('\n'), start =1):
                                           st.markdown(f"<h6>{lines}</h6>", unsafe_allow_html=True)
                                    st.write("********")
                                    st.markdown("*You can always contact the faculties in times of need we are always here to help you*")
                                    st.write("*******")

                                # Button to hide the details
                                if st.button("Hide"):
                                    st.write("Details hidden.")
                            else:
                                st.info("No information found for this student.")
                        else:
                            st.info("You are all good to go dont worry .")
                    else:
                        st.info("Please enter a valid student name.")
                else:
                    st.error("Unauthorized access! Please enter the correct password.")
            else:
                st.error("Unauthorized access! Please enter a valid student name.")

if __name__ == "__main__":
    viewer = StudentInformationViewer()
    viewer.run()
