# JobMailer

## Introduction

**JobMailer** is an innovative web application built with Streamlit that streamlines the job application process. By simply providing a job opening URL and uploading your resume, JobMailer generates a personalized cold email tailored to the specific job and your qualifications. This automated approach saves you time and increases the effectiveness of your job applications.

## Features

- **Automated Email Generation:** Creates professional cold emails based on job descriptions and your resume.
- **Resume Parsing:** Extracts and structures information from your PDF resume.
- **Job Description Extraction:** Scrapes job details from provided URLs.
- **Customizable Templates:** Generates emails tailored to specific job requirements.
- **User-Friendly Interface:** Simple and intuitive interface built with Streamlit.

## Tech Stack

JobMailer leverages a combination of modern technologies and libraries to deliver its functionality:

- **[Streamlit](https://streamlit.io/):** For building the interactive web interface.
- **[LangChain Groq](https://github.com/langchain-ai/langchain):** Utilized for natural language processing and generating structured outputs.
- **[Python Dotenv](https://pypi.org/project/python-dotenv/):** For managing environment variables securely.
- **[LangChain Community Document Loaders](https://github.com/langchain-ai/langchain-community):** For loading and processing web content.
- **[pypdf](https://pypi.org/project/pypdf/):** For extracting text from PDF resumes.

## Code Flow

The application follows a systematic flow to generate the desired cold email:

1. **User Input:**
   - **Job URL:** User provides the URL of the job opening.
   - **Resume Upload:** User uploads their resume in PDF format.

2. **Job Description Extraction:**
   - The application scrapes the provided job URL using `WebBaseLoader` to extract relevant job details such as role, experience, skills, and description.
   - The extracted data is structured into JSON format using `LangChain Groq`.

3. **Resume Parsing:**
   - The uploaded PDF resume is parsed using `pypdf.PdfReader` to extract text content.
   - The extracted text is then converted into a structured JSON format, categorizing information like personal details, experience, projects, education, skills, and more.

4. **Email Generation:**
   - Using the structured job description and resume data, the application leverages `LangChain Groq` to generate a personalized cold email.
   - The email aligns the user's qualifications with the job requirements, highlighting relevant experiences and skills.

5. **Display Output:**
   - The generated email is displayed on the Streamlit interface, allowing the user to copy and send it directly to the prospective employer.

## Environment Variables

JobMailer requires certain environment variables to function correctly. Ensure you have a `.env` file with the following variables:

- `GROQ_API_KEY`: Your Groq API key for accessing LangChain Groq services.

**Example `.env` file:**

```env
GROQ_API_KEY=your_groq_api_key_here
