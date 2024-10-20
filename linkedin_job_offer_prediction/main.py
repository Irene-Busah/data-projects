# # import streamlit as st
# # import pandas as pd


# # # Load the datasets
# # profiles_data_file = 'LinkedIn people profiles datasets.csv'
# # companies_data_file = 'LinkedIn company information datasets.csv'

# # # Load and transform the data
# # profiles_data = load_data(profiles_data_file)
# # companies_data = load_data(companies_data_file)


# # # Load Udemy course data
# # udemy_courses_file = 'courses.json'
# # udemy_courses = load_udemy_courses(udemy_courses_file)

# # # Title and Description
# # st.title("Custom Learning Pathways for Career Growth")
# # st.write("Get personalized course recommendations based on your career goals and LinkedIn profile!")

# # # User Inputs
# # company = st.text_input("Enter the company you're targeting:")
# # role = st.text_input("Enter the role you want to apply for:")

# # # Button to Get Recommendations
# # if st.button("Get Course Recommendations"):
# #     if company and role:
# #         # Simulate user profile skills based on company and role (for demo purposes)
# #         user_skills = "Python, Data Analysis, Machine Learning" 

# #         # Get recommended courses from Udemy data
# #         recommended_courses = recommend_courses(user_skills, udemy_courses)

# #         # Display the recommendations
# #         st.write(f"Course recommendations for the role of '{role}' at '{company}':")
# #         for course in recommended_courses:
# #             st.write(f"- [{course['title']}]({course['url']}) by {course['instructor']}")
# #             st.write(f"  - {course['headline']}")
# #     else:
# #         st.error("Please enter both the company and the role.")


# import streamlit as st
# import pandas as pd
# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from load_data import load_data, recommend_courses, load_udemy_courses, transform_companies_data, transform_profiles_data

# # Load the datasets
# profiles_data_file = 'LinkedIn people profiles datasets.csv'
# companies_data_file = 'LinkedIn company information datasets.csv'
# udemy_courses_file = 'courses.json'

# # Load and transform the data
# profiles_data = load_data(profiles_data_file)
# companies_data = load_data(companies_data_file)
# udemy_courses = load_udemy_courses(udemy_courses_file)

# # Transform LinkedIn profile data
# profiles_data = transform_profiles_data(profiles_data)
# companies_data = transform_companies_data(companies_data)

# # # Title and Description
# # st.title("Custom Learning Pathways for Career Growth")
# # st.write("Get personalized course recommendations based on your career goals and LinkedIn profile!")

# # # User Inputs
# # company = st.text_input("Enter the company you're targeting:")
# # role = st.text_input("Enter the role you want to apply for:")

# # def get_user_skills(profile_data, role):
# #     # Use 'position' instead of 'role' to filter the profile data
# #     skills = profile_data[profile_data['position'] == role]['experience'].values
# #     if len(skills) > 0:
# #         # Assuming 'experience' contains a comma-separated list of skills
# #         return skills[0]
# #     else:
# #         return "No skills found for the specified role."


# def get_user_skills(profiles_data, user_name=None, user_url=None):
#     """
#     Retrieve user skills from LinkedIn profiles using either the name or URL.
    
#     Args:
#         profiles_data (DataFrame): The LinkedIn profiles dataset.
#         user_name (str): The user's name.
#         user_url (str): The user's LinkedIn profile URL.

#     Returns:
#         str: A comma-separated list of skills or experiences for the user.
#     """
#     if user_name:
#         # Search by user's name
#         matched_profile = profiles_data[profiles_data['name'].str.contains(user_name, case=False, na=False)]
#     elif user_url:
#         # Search by LinkedIn profile URL
#         matched_profile = profiles_data[profiles_data['url'].str.contains(user_url, case=False, na=False)]
#     else:
#         return "No user information provided."

#     if not matched_profile.empty:
#         # Assuming 'experience' column contains a list of skills or roles
#         user_skills = matched_profile.iloc[0]['experience']
#         if pd.notna(user_skills):
#             return user_skills
#         else:
#             return "No skills found for this user."
#     else:
#         return "User profile not found."



# # # Button to Get Recommendations
# # if st.button("Get Course Recommendations"):
# #     if company and role:
# #         # Extract user's skills based on role and LinkedIn profile data
# #         user_skills = get_user_skills(profiles_data, role)
        
# #         # Use TF-IDF to calculate similarity between user skills and course headlines/titles
# #         tfidf_vectorizer = TfidfVectorizer(stop_words='english')
# #         course_texts = [course['headline'] for course in udemy_courses]
# #         tfidf_matrix = tfidf_vectorizer.fit_transform([user_skills] + course_texts)
        
# #         # Calculate cosine similarity
# #         similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
# #         # Sort courses by similarity
# #         sorted_indices = similarity_scores.argsort()[::-1]
# #         top_recommendations = [udemy_courses[i] for i in sorted_indices[:5]]  # Top 5 recommendations
        
# #         # Display the recommendations
# #         st.write(f"Course recommendations for the role of '{role}' at '{company}':")
# #         for course in top_recommendations:
# #             st.write(f"- [{course['title']}]({course['url']}) by {course['visible_instructors'][0]['display_name']}")
# #             st.write(f"  - {course['headline']}")
# #     else:
# #         st.error("Please enter both the company and the role.")



# # User Inputs
# st.title("Custom Learning Pathways for Career Growth")
# st.write("Get personalized course recommendations based on your career goals and LinkedIn profile!")

# user_name = st.text_input("Enter your LinkedIn name:")
# user_url = st.text_input("Or enter your LinkedIn profile URL:")
# company = st.text_input("Enter the company you're targeting:")
# role = st.text_input("Enter the role you want to apply for:")

# # Button to Get Recommendations
# if st.button("Get Course Recommendations"):
#     if (user_name or user_url) and company and role:
#         # Extract user's skills from LinkedIn data
#         user_skills = get_user_skills(profiles_data, user_name=user_name, user_url=user_url)

#         if user_skills != "User profile not found." and user_skills != "No skills found for this user.":
#             # Use TF-IDF to calculate similarity between user skills and course headlines/titles
#             tfidf_vectorizer = TfidfVectorizer(stop_words='english')
#             course_texts = [course['headline'] for course in udemy_courses]
#             tfidf_matrix = tfidf_vectorizer.fit_transform([user_skills] + course_texts)

#             # Calculate cosine similarity
#             similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

#             # Sort courses by similarity
#             sorted_indices = similarity_scores.argsort()[::-1]
#             top_recommendations = [udemy_courses[i] for i in sorted_indices[:5]]  # Top 5 recommendations

#             # Display the recommendations
#             st.write(f"Course recommendations for the role of '{role}' at '{company}':")
#             for course in top_recommendations:
#                 st.write(f"- [{course['title']}]({course['url']}) by {course['visible_instructors'][0]['display_name']}")
#                 st.write(f"  - {course['headline']}")
#         else:
#             st.error(user_skills)  # Display the error message from get_user_skills
#     else:
#         st.error("Please provide your LinkedIn name or URL, and enter both the company and the role.")

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader
import docx
import json

# Function to load courses from JSON file
def load_courses_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Check if 'results' key is present and contains a list
            if isinstance(data, dict) and 'results' in data and isinstance(data['results'], list):
                courses = data['results']
                return courses
            else:
                st.error("The JSON file format is incorrect. It should have a 'results' key containing a list of course dictionaries.")
                return []
    except json.JSONDecodeError:
        st.error("Failed to parse the JSON file. Please check its format.")
        return []

# Extract skills from uploaded résumé or CV
def extract_skills_from_resume(file):
    if file.name.endswith('.pdf'):
        reader = PdfReader(file)
        text = ''.join([page.extract_text() for page in reader.pages])
    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    else:
        return None
    return text

# Function to get course recommendations
def get_course_recommendations(user_skills, job_title, udemy_courses):
    # Combine user skills and job title for a more accurate recommendation
    combined_input = f"{user_skills} {job_title}"
    
    # Use TF-IDF to calculate similarity between the combined input and course headlines/titles
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    course_texts = [course.get('headline', '') for course in udemy_courses]  # Safely access 'headline'
    tfidf_matrix = tfidf_vectorizer.fit_transform([combined_input] + course_texts)

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Sort courses by similarity
    sorted_indices = similarity_scores.argsort()[::-1]
    top_recommendations = [udemy_courses[i] for i in sorted_indices[:5]]  # Top 5 recommendations
    return top_recommendations

# Function to display formatted course recommendations
def display_course_recommendations(courses):
    st.write("### Here are some course recommendations based on your skills and desired job title:")
    for idx, course in enumerate(courses, start=1):
        instructor_name = course['visible_instructors'][0]['display_name'] if course['visible_instructors'] else 'Unknown Instructor'
        st.markdown(f"""
        **{idx}. [{course['title']}]({course['url']})**  
        *Instructor:* {instructor_name}  
        *Description:* {course['headline']}  
        """, unsafe_allow_html=True)
        st.write("---")

# Load Udemy courses from JSON
udemy_courses = load_courses_from_json('courses.json')

# Streamlit app layout
st.title("Course Recommendations Based on Your Skills and Job Title")
st.write("Get personalized course recommendations by providing your skills and the job title you're interested in.")

# Input for job title
job_title = st.text_input("Enter the job title you are applying for:")

# Input options
input_option = st.selectbox("How would you like to provide your skills?", 
                            ["Manual Input", "Upload Résumé/CV", "Select from Predefined List"])

user_skills = None

# Manual skill input
if input_option == "Manual Input":
    user_skills_input = st.text_area("Enter your skills, separated by commas:")
    if user_skills_input:
        user_skills = user_skills_input

# Upload résumé/CV
elif input_option == "Upload Résumé/CV":
    uploaded_file = st.file_uploader("Upload your résumé or CV (PDF or DOCX)", type=["pdf", "docx"])
    if uploaded_file is not None:
        extracted_text = extract_skills_from_resume(uploaded_file)
        if extracted_text:
            user_skills = extracted_text
            st.write("Résumé uploaded successfully!")
        else:
            st.error("Could not extract text from the uploaded file. Please try again.")

# Predefined skill selection
elif input_option == "Select from Predefined List":
    skill_options = ["Python", "Data Analysis", "Machine Learning", "Project Management", 
                     "SQL", "Marketing", "Communication", "Leadership", "Cloud Computing"]
    selected_skills = st.multiselect("Select your skills", skill_options)
    if selected_skills:
        user_skills = ', '.join(selected_skills)

# Button to Get Recommendations
if st.button("Get Course Recommendations"):
    if user_skills and job_title:
        top_recommendations = get_course_recommendations(user_skills, job_title, udemy_courses)
        # Display the recommendations
        display_course_recommendations(top_recommendations)
    else:
        st.error("Please provide both your skills and the job title.")
