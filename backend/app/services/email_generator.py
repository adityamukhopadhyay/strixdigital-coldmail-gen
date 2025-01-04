import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class EmailGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0, 
            groq_api_key=os.getenv("GROQ_API_KEY"), 
            model_name="mixtral-8x7b-32768"
        )

    def extract_job_details(self, job_url):
        prompt_extract = PromptTemplate.from_template(
            """
            ### JOB URL:
            {job_url}
            ### INSTRUCTION:
            The provided URL is for a job posting. Extract the key details and return them in JSON format 
            containing the following keys: `role`, `company`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"job_url": job_url})
        try:
            json_parser = JsonOutputParser()
            return json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Unable to parse job details.")

    def generate_email(self, job_details):
        portfolio_links = [
            "Machine Learning with Python: https://strixdigital.in/portfolio/ml-python",
            "DevOps & Cloud: https://strixdigital.in/portfolio/devops",
            "AI Solutions: https://strixdigital.in/portfolio/ai",
            "Enterprise Software: https://strixdigital.in/portfolio/enterprise"
        ]

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DETAILS:
            {job_details}

            ### INSTRUCTION:
            You are Aditya Mukhopadhyay, Project Management Officer (PMO) at Strix Digital. 
            Strix Digital is a leading AI & Software Consulting company specializing in cutting-edge 
            technology solutions and digital transformation.

            Write a compelling cold email for this job opportunity that:
            1. Introduces Strix Digital and its expertise
            2. Highlights how Strix Digital can address their specific needs based on the job requirements
            3. Mentions our work with notable clients like Indian Army, Tata Digital, Yes Bank, HDFC Bank, and General Mills
            4. Includes 2-3 most relevant portfolio links from: {portfolio_links}
            5. Maintains a professional yet engaging tone
            6. Ends with a clear call to action for a meeting/call

            Remember: You are Aditya Mukhopadhyay, PMO at Strix Digital.
            Do not provide any preamble, just the email content.
            
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_details": str(job_details), 
            "portfolio_links": ", ".join(portfolio_links)
        })
        return res.content

if __name__ == "__main__":
    # Test the email generator
    generator = EmailGenerator()
    test_url = "https://example.com/job-posting"
    try:
        job_details = generator.extract_job_details(test_url)
        email = generator.generate_email(job_details)
        print(email)
    except Exception as e:
        print(f"Error: {str(e)}") 