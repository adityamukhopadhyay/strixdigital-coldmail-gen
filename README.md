# Strix Digital - Cold Email Generator

A proprietary web application for generating personalized cold emails based on job requirements. Built with Next.js and React, featuring a Python serverless backend powered by Groq AI.

![Strix Digital Logo](/public/strix-digital-logo.png)

## Features
- Modern, responsive UI built with Next.js 14
- AI-powered email generation using Groq
- Automatic job details extraction
- Real-time email preview
- Copy to clipboard functionality
- Dark mode design
- Smooth animations using Framer Motion
- Serverless architecture with Vercel

## Tech Stack
### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom components with Radix UI
- **Animations**: Framer Motion
- **Icons**: Lucide React

### Backend
- **Runtime**: Python 3.9+
- **AI Integration**: Groq API
- **Architecture**: Serverless Functions
- **Deployment**: Vercel
- **API Client**: OpenAI-compatible client

## Getting Started

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- Groq API Key

### Installation

1. Clone the repository
```bash
git clone https://github.com/adityamukhopadhyay/strixdigital-coldmail-gen.git
cd strixdigital-coldmail-gen
```

2. Install frontend dependencies
```bash
npm install
```

3. Set up environment variables
Create a `.env.local` file with:
```
NEXT_PUBLIC_BACKEND_URL=http://localhost:3000
GROQ_API_KEY=your_groq_api_key_here
```

4. Run the development server
```bash
npm run dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure
```
strixdigital-coldmail-gen/
├── api/
│   └── python/              # Python serverless backend
│       ├── generate_email.py  # Main serverless function
│       ├── config.py         # AI client configuration
│       └── requirements.txt  # Python dependencies
├── app/                     # Next.js frontend
├── public/                  # Static assets
└── [Next.js config files]  # Frontend configuration
```

## How It Works
1. Frontend sends job link to `/api/generate-email`
2. Python serverless function extracts job details using Groq AI
3. AI generates personalized email based on job requirements
4. Response is sent back to frontend for display

## Deployment
The project is deployed on Vercel with serverless functions:
1. Frontend is automatically built and deployed
2. Python backend runs as serverless functions
3. Environment variables are configured in Vercel dashboard

## License
This project is proprietary software owned by Strix Digital. All rights reserved.

## Contact
For any inquiries about this project, please contact:
- Strix Digital
- Project Manager: Aditya Mukhopadhyay
- Email: aditya@strixdigital.in
