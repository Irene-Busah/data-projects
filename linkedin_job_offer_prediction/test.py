from load_data import load_data, transform_profiles_data, transform_companies_data, recommend_courses, match_companies

# Paths to your data files
profiles_data_file = 'datasets/LinkedIn_people_profiles.csv'
companies_data_file = 'datasets/LinkedIn_companies_info.csv'

# Step 1: Load the data
profiles_data = load_data(profiles_data_file)
companies_data = load_data(companies_data_file)

# Check if data loaded successfully
if profiles_data is not None:
    print("Profiles data loaded successfully.")
else:
    print("Failed to load profiles data.")

if companies_data is not None:
    print("Companies data loaded successfully.")
else:
    print("Failed to load companies data.")

# Step 2: Transform the data
if profiles_data is not None:
    profiles_data = transform_profiles_data(profiles_data)
    print("Profiles data transformed successfully.")

if companies_data is not None:
    companies_data = transform_companies_data(companies_data)
    print("Companies data transformed successfully.")

# Step 3: Test the recommendation functions
# Example user profile with skills and career interests
user_skills = "Python, Data Analysis, Machine Learning"
courses_list = ["Introduction to Data Science", "Machine Learning with Python", 
                "Advanced Python Programming", "Data Visualization Techniques", 
                "Big Data Analytics"]

# Test course recommendation
recommended_courses = recommend_courses(user_skills, courses_list)
print("Recommended Courses:", recommended_courses)

# Example user profile for company matching
user_profile = {
    'current_company': 'Tech',  # Assume this is an industry-related keyword
    'experience': 'Data Science, AI, Machine Learning'
}

# Test company matching
if companies_data is not None:
    matched_companies = match_companies(user_profile, companies_data)
    print("Top Companies Recommended for User:")
    print(matched_companies)