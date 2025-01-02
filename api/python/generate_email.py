from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import traceback
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

def log_error(error: Exception, context: str = "") -> None:
    """Log error details to stderr"""
    print(f"\nERROR in {context}:", file=sys.stderr)
    print(f"Type: {type(error).__name__}", file=sys.stderr)
    print(f"Message: {str(error)}", file=sys.stderr)
    print("Traceback:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print("\n", file=sys.stderr)

def cors_headers() -> Dict[str, str]:
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

class EmailGenerator:
    def __init__(self):
        print("Initializing EmailGenerator...", file=sys.stderr)
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        try:
            self.llm = ChatGroq(
                temperature=0, 
                groq_api_key=api_key,
                model_name="llama-3.1-70b-versatile"
            )
            print("Successfully initialized Groq LLM", file=sys.stderr)
        except Exception as e:
            log_error(e, "LLM initialization")
            raise ValueError(f"Failed to initialize LLM: {str(e)}")

    def extract_job_details(self, job_url: str) -> Dict[str, Any]:
        print(f"\nExtracting job details from: {job_url}", file=sys.stderr)
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
            print("Sending job details extraction request to Groq...", file=sys.stderr)
            res = chain_extract.invoke(input={"job_url": job_url})
            print("Received response from Groq", file=sys.stderr)
            
            try:
                json_parser = JsonOutputParser()
                parsed_data = json_parser.parse(res.content)
                print("Successfully parsed job details", file=sys.stderr)
                return parsed_data
            except Exception as e:
                log_error(e, "JSON parsing")
                print(f"Raw response content: {res.content}", file=sys.stderr)
                raise ValueError(f"Unable to parse job details: {str(e)}")
                
        except Exception as e:
            log_error(e, "Job details extraction")
            raise ValueError(f"Failed to extract job details: {str(e)}")

    def generate_email(self, job_details: Dict[str, Any]) -> str:
        print("\nGenerating email from job details...", file=sys.stderr)
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
            print("Sending email generation request to Groq...", file=sys.stderr)
            chain_email = prompt_email | self.llm
            res = chain_email.invoke({
                "job_details": str(job_details), 
                "portfolio_links": ", ".join(portfolio_links)
            })
            print("Successfully generated email content", file=sys.stderr)
            return res.content
            
        except Exception as e:
            log_error(e, "Email generation")
            raise ValueError(f"Failed to generate email: {str(e)}")

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        for key, value in cors_headers().items():
            self.send_header(key, value)
        self.end_headers()

    def do_POST(self):
        print("\n=== Starting new request ===", file=sys.stderr)
        try:
            # Send response headers first
            self.send_response(200)
            for key, value in cors_headers().items():
                self.send_header(key, value)
            self.end_headers()

            # Read and parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            print(f"Request content length: {content_length}", file=sys.stderr)
            
            if content_length == 0:
                raise ValueError("Empty request body")
                
            body = self.rfile.read(content_length)
            data = json.loads(body)
            print(f"Parsed request data: {data}", file=sys.stderr)
            
            if not data.get('job_link'):
                raise ValueError("Job link is required")

            # Initialize generator and process request
            generator = EmailGenerator()
            
            job_details = generator.extract_job_details(data['job_link'])
            print(f"Extracted job details: {job_details}", file=sys.stderr)
            
            email_content = generator.generate_email(job_details)
            print(f"Generated email content length: {len(email_content)}", file=sys.stderr)

            # Send successful response
            response = {'email': email_content}
            self.wfile.write(json.dumps(response).encode())
            print("Successfully sent response", file=sys.stderr)
            
        except Exception as e:
            log_error(e, "Request handler")
            error_response = {
                'error': str(e),
                'type': type(e).__name__
            }
            self.wfile.write(json.dumps(error_response).encode()) 