import streamlit as st
import nltk
nltk.download('stopwords')
from pyresparser import ResumeParser

# Define the Streamlit app
def app():
    st.title('Resume Parser')
    first_name = st.text_input('First Name')
    last_name = st.text_input('Last Name')
    uploaded_file = st.file_uploader("Hi! Upload your resume file in PDF format", type=['pdf'])

    if uploaded_file is not None:
        # Parse the resume file
        resume_data = ResumeParser(uploaded_file).get_extracted_data()

        # Display the extracted details
        st.header("**Resume Info**")
        if resume_data.get('name'):
            st.success("Hello "+ first_name + ' ' + last_name)
            st.subheader("**Your Basic info**")
            try:
                st.write('Name: '+ first_name + ' ' + last_name)
                st.write('Email: ' + resume_data['email'])
                st.write('Contact: ' + resume_data['mobile_number'])
            except:
                pass
        else:
            st.error("Sorry, could not extract basic info from the resume")

        # Extract the skills
        skills = resume_data.get('skills', [])
        if skills:
            st.subheader("**Skills**")
            st.write(', '.join(skills))

        # Extract the work experience
        work_experience = resume_data.get('experience', [])
        if work_experience:
            st.subheader("**Work Experience**")
            for i, exp in enumerate(work_experience):
                if isinstance(exp, dict):
                    st.write(f"{i+1}. {exp.get('company', '')}: {exp.get('title', '')}: {exp.get('date_range', '')}")
                    st.write(f"   {exp.get('description', '')}")
                else:
                    st.write(f"{i+1}. {exp}")

        # Extract the education
        education = resume_data.get('education', [])
        if education:
            st.subheader("**Education**")
            for edu in education:
                st.write(edu['degree'] + ', ' + edu['major'] + ', ' + edu['date_range'])

    else:
        st.write('Please upload a resume file')


if __name__ == '__main__':
    app()
