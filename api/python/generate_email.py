from http.server import BaseHTTPRequestHandler
import json
import os
import sys
from typing import Dict, Any
import groq

def log_error(error: Exception, context: str = "") -> None:
    """Log error details to stderr"""
    print(f"\nERROR in {context}:", file=sys.stderr)
    print(f"Type: {type(error).__name__}", file=sys.stderr)
    print(f"Message: {str(error)}", file=sys.stderr)
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
            self.client = groq.Groq(api_key=api_key)
            print("Successfully initialized Groq client", file=sys.stderr)
        except Exception as e:
            log_error(e, "Groq client initialization")
            raise ValueError(f"Failed to initialize Groq client: {str(e)}")

    def extract_job_details(self, job_url: str) -> Dict[str, Any]:
        print(f"\nExtracting job details from: {job_url}", file=sys.stderr)
        try:
            prompt = f"""
            ### JOB URL:
            {job_url}
            ### INSTRUCTION:
            The provided URL is for a job posting. Extract the key details and return them in JSON format 
            containing the following keys: `role`, `company`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
            
            print("Sending job details extraction request to Groq...", file=sys.stderr)
            completion = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            response_content = completion.choices[0].message.content
            print("Received response from Groq", file=sys.stderr)
            
            try:
                # Try to parse the response as JSON
                parsed_data = json.loads(response_content)
                print("Successfully parsed job details", file=sys.stderr)
                return parsed_data
            except Exception as e:
                log_error(e, "JSON parsing")
                print(f"Raw response content: {response_content}", file=sys.stderr)
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

            prompt = f"""
            ### JOB DETAILS:
            {str(job_details)}

            ### INSTRUCTION:
            You are Aditya Mukhopadhyay, Project Management Officer (PMO) at Strix Digital. 
            Strix Digital is a leading AI & Software Consulting company specializing in cutting-edge 
            technology solutions and digital transformation.

            Write a compelling cold email for this job opportunity that:
            1. Introduces Strix Digital and its expertise
            2. Highlights how Strix Digital can address their specific needs based on the job requirements
            3. Mentions our work with notable clients like Indian Army, Tata Digital, Yes Bank, HDFC Bank, and General Mills
            4. Includes 2-3 most relevant portfolio links from: {", ".join(portfolio_links)}
            5. Maintains a professional yet engaging tone
            6. Ends with a clear call to action for a meeting/call

            Remember: You are Aditya Mukhopadhyay, PMO at Strix Digital.
            Do not provide any preamble, just the email content.
            
            ### EMAIL (NO PREAMBLE):
            """
            
            print("Sending email generation request to Groq...", file=sys.stderr)
            completion = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            email_content = completion.choices[0].message.content
            print("Successfully generated email content", file=sys.stderr)
            return email_content
            
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
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body)
                print(f"Parsed request data: {data}", file=sys.stderr)
            except Exception as e:
                log_error(e, "Request body parsing")
                raise ValueError("Invalid request body")
            
            if not data.get('job_link'):
                raise ValueError("Job link is required")

            # Initialize generator and process request
            generator = EmailGenerator()
            
            job_details = generator.extract_job_details(data['job_link'])
            print(f"Extracted job details: {job_details}", file=sys.stderr)
            
            email_content = generator.generate_email(job_details)
            print(f"Generated email content length: {len(email_content)}", file=sys.stderr)

            # Send successful response
            self.send_response(200)
            for key, value in cors_headers().items():
                self.send_header(key, value)
            self.end_headers()

            response = {'email': email_content}
            self.wfile.write(json.dumps(response).encode())
            print("Successfully sent response", file=sys.stderr)

        except Exception as e:
            log_error(e, "Request handler")
            
            self.send_response(500)
            for key, value in cors_headers().items():
                self.send_header(key, value)
            self.end_headers()
            
            error_response = {
                'error': str(e),
                'type': type(e).__name__
            }
            self.wfile.write(json.dumps(error_response).encode()) 