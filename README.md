# Strix Digital - Cold Email Generator

A proprietary web application for generating personalized cold emails based on job requirements. Built with Next.js and React, with plans for a Python backend integration.

![Strix Digital Logo](/public/strix-digital-logo.png)

## Current Status: Frontend Implementation

This repository contains the frontend implementation of the Cold Email Generator. The backend integration will be added in a future phase.

### Features
- Modern, responsive UI built with Next.js 14
- Dark mode design
- Real-time email preview
- Copy to clipboard functionality
- Smooth animations using Framer Motion
- Fully TypeScript implementation

### Tech Stack
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Custom components with Radix UI
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Development**: ESLint, TypeScript

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository (requires access)
```bash
git clone https://github.com/adityamukhopadhyay/strixdigital-coldmail-gen.git
cd strixdigital-coldmail-gen
```

2. Install dependencies
```bash
npm install
# or
yarn install
```

3. Run the development server
```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Future Plans

### Backend Integration
- Python backend for processing job requirements
- AI-powered email generation
- Template customization
- API integration for job data extraction

### How Backend Will Work
The `handleSubmit` function in `src/components/EmailGenerator.tsx` will be modified to make API calls to the Python backend:

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault()
  try {
    const response = await fetch('/api/generate-email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ jobLink })
    })
    const data = await response.json()
    setGeneratedEmail(data.email)
  } catch (error) {
    console.error('Failed to generate email:', error)
  }
}
```

## License
This project is proprietary software owned by Strix Digital. All rights reserved.

## Contact
For any inquiries about this project, please contact:
- Strix Digital
- Project Manager: Aditya Mukhopadhyay
