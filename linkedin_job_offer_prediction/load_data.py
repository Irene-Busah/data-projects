import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def load_data(data_file):
    """Load data from a CSV file and return a DataFrame."""
    try:
        data = pd.read_csv(data_file)
        # print(f"Successfully loaded {data_file}")
        return data
    except FileNotFoundError:
        # print(f"Error: The file {data_file} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {data_file} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: There was a problem parsing the file {data_file}.")
        return None


def transform_profiles_data(data):
    """Clean and transform the LinkedIn profiles dataset."""

    # dropping the columns that are not useful for analysis
    columns_to_drop = ['timestamp', 'avatar', 'url', 'people_also_viewed', 'image']
    data = data.drop(columns=[col for col in columns_to_drop if col in data.columns], errors='ignore')

    # filling missing values for certain columns
    data.fillna({'about': '', 'experience': '', 'languages': '', 'certifications': ''}, inplace=True)

    # extracting the number of years of experience from the 'experience' column
    data['years_of_experience'] = data['experience'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0)

    # counting the number of certifications
    data['num_certifications'] = data['certifications'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0)

    # counting the number of languages
    data['num_languages'] = data['languages'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0)

    return data


def transform_companies_data(data):
    """Clean and transform the LinkedIn companies dataset."""
    # dropping columns that are not relevant
    columns_to_drop = ['timestamp', 'logo', 'image', 'crunchbase_url', 'url', 'affiliated']
    data = data.drop(columns=[col for col in columns_to_drop if col in data.columns], errors='ignore')

    # handling missing values
    data.fillna({'about': '', 'specialties': '', 'industries': ''}, inplace=True)

    # creating a feature for the number of specialties
    data['num_specialties'] = data['specialties'].apply(lambda x: len(str(x).split(',')) if pd.notna(x) else 0)

    # calculating the number of years since the company was founded
    if 'founded' in data.columns:
        data['years_since_founded'] = datetime.now().year - data['founded'].fillna(0).astype(int)

    # creating a feature indicating if the company is a large company (based on employees)
    data['is_large_company'] = data['company_size'].apply(lambda x: '1000+' in str(x))

    return data


def load_udemy_courses(json_file):
    with open(json_file, 'r') as file:
        udemy_data = json.load(file)
    # Extract the list of courses
    courses = udemy_data['results']
    return courses

def extract_course_info(course):
    return {
        'title': course['title'],
        'instructor': course['visible_instructors'][0]['display_name'] if course['visible_instructors'] else "N/A",
        'url': f"https://www.udemy.com{course['url']}",
        'headline': course['headline']
    }


def recommend_courses(user_skills, udemy_courses, top_n=5):
    # Filter courses that contain any of the user's skills in the title or headline
    recommended = []
    for course in udemy_courses:
        if any(skill.lower() in course['headline'].lower() for skill in user_skills.split(',')):
            recommended.append(extract_course_info(course))
    
    # Sort by relevance (for simplicity, use length of headline matching as a crude metric)
    recommended = sorted(recommended, key=lambda x: len(x['headline']), reverse=True)[:top_n]
    return recommended


def match_companies(user_profile, companies_data):
    """Match users with companies based on their career interests and skills."""
    # Filter companies based on industries related to user's experience
    relevant_companies = companies_data[companies_data['industries'].str.contains(user_profile['current_company'], na=False)]

    # Score companies based on the number of matching specialties
    relevant_companies['matching_score'] = relevant_companies['specialties'].apply(
        lambda x: len(set(user_profile['experience'].split(',')) & set(x.split(',')))
    )

    # Recommend top companies based on matching score
    top_companies = relevant_companies.sort_values(by='matching_score', ascending=False).head(5)

    return top_companies[['name', 'industries', 'specialties', 'years_since_founded']]


# def recommend_courses(user_skills, courses):
#     """Recommend courses based on the user's skill gaps."""

#     # vectorizing user skills and course descriptions using TF-IDF
#     vectorizer = TfidfVectorizer()
#     user_skills_vec = vectorizer.fit_transform([user_skills])
#     courses_vec = vectorizer.transform(courses)

#     # calculating similarity between user skills and each course
#     similarities = cosine_similarity(user_skills_vec, courses_vec)

#     # ranking courses by similarity score
#     ranked_courses = sorted(list(zip(courses, similarities[0])), key=lambda x: x[1], reverse=True)

#     # returning the top 5 recommended courses
#     return [course for course, score in ranked_courses[:5]]