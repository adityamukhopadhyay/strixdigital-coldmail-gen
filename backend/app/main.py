from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .services.email_generator import EmailGenerator

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    job_link: str

@app.post("/api/generate-email")
async def generate_email(request: JobRequest):
    try:
        generator = EmailGenerator()
        # Extract job details from the URL
        job_details = generator.extract_job_details(request.job_link)
        # Generate the email using the extracted details
        email_content = generator.generate_email(job_details)
        return {"email": email_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 