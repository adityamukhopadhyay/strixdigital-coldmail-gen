import { NextResponse } from 'next/server'

interface JobRequest {
  job_link: string;
}

export async function POST(request: Request) {
  try {
    const body = await request.json() as JobRequest
    
    if (!body.job_link) {
      return NextResponse.json(
        { error: 'Job link is required' },
        { status: 400 }
      )
    }

    // Forward the request to our Python backend
    const response = await fetch('/api/python/generate_email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Failed to generate email')
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error('Error:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to generate email' },
      { status: 500 }
    )
  }
} 