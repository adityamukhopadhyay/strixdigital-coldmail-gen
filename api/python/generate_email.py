from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

class EmailGenerator:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.llm = ChatGroq(
            temperature=0, 
            groq_api_key=api_key,
            model_name="llama-3.1-70b-versatile"
        )

    def extract_job_details(self, job_url):
        try:
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
            except Exception as e:
                print(f"JSON parsing error: {str(e)}", file=sys.stderr)
                print(f"Response content: {res.content}", file=sys.stderr)
                raise ValueError(f"Unable to parse job details: {str(e)}")
                
        except Exception as e:
            print(f"Extraction error: {str(e)}", file=sys.stderr)
            raise ValueError(f"Failed to extract job details: {str(e)}")

    def generate_email(self, job_details):
        try:
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
            
        except Exception as e:
            print(f"Email generation error: {str(e)}", file=sys.stderr)
            raise ValueError(f"Failed to generate email: {str(e)}")

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        for key, value in cors_headers().items():
            self.send_header(key, value)
        self.end_headers()

    def do_POST(self):
        try:
            # Add CORS headers
            for key, value in cors_headers().items():
                self.send_header(key, value)

            # Read and parse request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            if not data.get('job_link'):
                self.send_response(400)
                self.end_headers()
                error_response = {'error': 'Job link is required'}
                self.wfile.write(json.dumps(error_response).encode())
                return

            # Initialize generator and process request
            generator = EmailGenerator()
            print(f"Processing job link: {data['job_link']}", file=sys.stderr)
            
            job_details = generator.extract_job_details(data['job_link'])
            print(f"Extracted job details: {job_details}", file=sys.stderr)
            
            email_content = generator.generate_email(job_details)
            print(f"Generated email content length: {len(email_content)}", file=sys.stderr)

            # Send successful response
            self.send_response(200)
            self.end_headers()
            response = {'email': email_content}
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            print(f"Error in handler: {str(e)}", file=sys.stderr)
            self.send_response(500)
            self.end_headers()
            error_response = {'error': str(e)}
            self.wfile.write(json.dumps(error_response).encode()) 