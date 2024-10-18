import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pypdf import PdfReader
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

# Initialize the model with the API key
llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    groq_api_key=groq_api_key,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def get_job_description(url):
    try:
        loader = WebBaseLoader(url)
        page_data = loader.load().pop().page_content
        print("___________________________________________________________________---------------------")
        print(page_data)

        prompt_extract = PromptTemplate.from_template(
            '''
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, and `description`.
            Only return the valid JSON which has all the 4 fields.

            ### VALID JSON (NO PREAMBLE):
            '''
        )

        chain_extract = prompt_extract | llm
        res = chain_extract.invoke(input={'page_data' : page_data})
        # print(type(res.content))
        # print(res.content)
        print("--------------------------------------------------------------")
        return res.content
    except Exception as e:
        return f"Error fetching job description: {str(e)}"

def parse_in_json(content):
    json_parser = JsonOutputParser()
    json_res = json_parser.parse(content)
    return json_res

def extract_text_from_pdf(pdf):
    reader = PdfReader(pdf)
    print(len(reader.pages))
    page = reader.pages[0]
    text = page.extract_text()
    return text

def get_json_resume(resume_text):
    prompt_extract = PromptTemplate.from_template(
        '''
        ### Task: 
        Convert the following resume text into a structured JSON format. Ensure that all relevant information is correctly categorized according to the provided JSON structure template.
        
        ### Resume text:
        {resume_text}

        ### Instructions :
        1. Extract 'personal information', 'experience', 'projects', 'education', 'technical skills', 'achievements', 'extracurriculars', and 'coursework' from the resume text.
        2. Format the output into the JSON template below.
        3. Ensure that each field is accurately filled based on the resume content.

        ### VALID JSON (NO PREAMBLE):

        ### JSON Template
        {{
            "personal_information": {{
                "name": "Full Name",
                "email": "email@example.com",
                "phone": "Phone Number",
                "linkedin": "LinkedIn URL",
                "github": "GitHub URL"
            }},
            "summary": "A brief summary or objective (optional)",
            "experience": [
                {{
                "title": "Job Title",
                "company": "Company Name",
                "location": "Location",
                "start_date": "Start Date",
                "end_date": "End Date (or 'Present')",
                "responsibilities": [
                    "Responsibility 1",
                    "Responsibility 2",
                    "Responsibility 3"
                ]
                }}
            ],
            "projects": [
                {{
                "title": "Project Title",
                "technologies": ["Technology 1", "Technology 2"],
                "description": "Brief description of the project.",
                "github": "GitHub URL"
                }}
            ],
            "education": [
                {{
                "degree": "Degree",
                "institution": "Institution Name",
                "start_date": "Start Date",
                "end_date": "End Date",
                "cgpa": "CGPA or Percentage"
                }}
            ],
            "technical_skills": [
                "Skill 1", "Skill 2", "Skill 3", "Skill 4"
            ],
            "achievements": [
                {{
                "name": "Achievement Name",
                "value": "Achievement Details (Score, Rank, etc.)"
                }}
            ],
            "extracurriculars": [
                {{
                "role": "Role or Position",
                "organization": "Organization or Club Name"
                }}
            ],
            "coursework": [
                "Course 1", "Course 2", "Course 3", "Course 4"
            ]
        }}
        '''
    )

    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={'resume_text' : resume_text})
    # print(type(res.content))
    print(res.content)
    return res.content


def generate_email(job_desc, resume_desc):
    # Job description attributes
    job_role = job_desc[0]['role']
    job_experience = job_desc[0]['experience']
    job_skills = ', '.join(job_desc[0]['skills'])  # Convert skills list to a comma-separated string
    job_description = job_desc[0]['description']

    # Resume details
    personal_info = resume_desc.get("personal_information", {})
    name = personal_info.get("name", "Name")
    email = personal_info.get("email", "email@example.com")
    phone = personal_info.get("phone", "Phone Number")
    linkedin = personal_info.get("linkedin", "LinkedIn URL")
    github = personal_info.get("github", "GitHub URL")
    

    resume_experience = '\n'.join([f"- {exp['title']} at {exp['company']} ({exp['start_date']} to {exp['end_date']}): {', '.join(exp['responsibilities'])}" for exp in resume_desc.get("experience", [])])
    resume_projects = '\n'.join([f"- {proj['title']} ({', '.join(proj['technologies'])}): {proj['description']} [GitHub: {proj['github']}]" for proj in resume_desc.get("projects", [])])
    resume_education = '\n'.join([f"- {edu['degree']} from {edu['institution']} ({edu['start_date']} to {edu['end_date']}) - CGPA: {edu.get('cgpa', 'N/A')}" for edu in resume_desc.get("education", [])])
    resume_skills = ', '.join(resume_desc.get("technical_skills", []))

    print(resume_experience)
    print(resume_projects)
    print(resume_education)
    print(resume_skills)

    prompt_extract = PromptTemplate.from_template(
        """
        Write a compelling and professional cold email applying for the {job_role} position. The email should highlight my qualifications based on the job description and my resume. Use the following details:

        ### Job Description:
        - Role: {job_role}
        - Required Experience: {job_experience}
        - Key Skills: {job_skills}
        - Job Description: {job_description}

        ### My Resume:
        Personal Information:
        - Name: {name}
        - Email: {email}
        - Phone: {phone}
        - LinkedIn: {linkedin}
        - GitHub: {github}

        Professional Experience:
        {resume_experience}

        Projects:
        {resume_projects}

        Education:
        {resume_education}

        Technical Skills:
        {resume_skills}

        ### Email Structure:
        1. **Opening**: Start with a warm greeting and briefly introduce myself, specifying the position I'm applying for.
        2. **Job Alignment**: Mention why I'm interested in the role and the company. Clearly link the required skills and experience from the job description with my background, highlighting key strengths.
        3. **Achievements & Fit**: Elaborate on specific achievements or projects from my resume that demonstrate my ability to meet the job requirements. Include quantifiable results or key impacts where possible.
        4. **Company-Specific Enthusiasm**: Show genuine interest in the company and its work, and explain why I want to contribute to their team.
        5. **Closing & Call to Action**: Politely express my desire to discuss further, request an interview, and provide my contact details. Thank them for considering my application.

        ### Style Guidelines:
        - Keep the tone professional yet friendly, showing confidence without being overly formal.
        - Use concise sentences and avoid unnecessary repetition.
        - Focus on how my experience, skills, and projects solve problems relevant to the job description.
        - Ensure that the email feels personalized and tailored to this specific job and company.

        Generate the email text without any preamble.
        """
    )

    chain_extract = prompt_extract | llm
    res = chain_extract.invoke(input={
        'job_role' : job_role,
        'job_experience' : job_experience,
        'job_skills' : job_skills,
        'job_description' : job_description,
        'name' : name,
        'email' : email,
        'phone' : phone,
        'linkedin' : linkedin,
        'github' : github,
        'resume_experience' : resume_experience,
        'resume_projects' : resume_projects,
        'resume_education' : resume_education,
        'resume_skills' : resume_skills
        })
    # print(type(res.content))
    # print(res.content)
    return res.content

# Streamlit interface
st.title('Job Application Email Generator')

# URL input
job_url = st.text_input('Enter the URL of the job opening')



# Resume upload
resume_file = st.file_uploader('Upload your resume (PDF)', type=['pdf'])

# Generate button
if st.button('Generate Email'):
    if job_url and resume_file:  # Ensure both job URL and resume are provided
        job_desc = get_job_description(job_url)
        job_desc_json = parse_in_json(job_desc)
        # print(job_desc_json)

        # Extract text from uploaded PDF resume
        resume_text = extract_text_from_pdf(resume_file)
        # print(resume_text)

        resume_desc = get_json_resume(resume_text)
        resume_text_json = parse_in_json(resume_desc)
        print(resume_desc)
        print(resume_text_json)  

        email_text = generate_email(job_desc_json, resume_text_json)
        print(email_text)

        st.subheader("Generated Email")
        st.text_area("Generated Email Text", value=email_text, height=1000)
        st.code(email_text, language='text')


    else:
        st.error("Please provide both the job URL and your resume.")

