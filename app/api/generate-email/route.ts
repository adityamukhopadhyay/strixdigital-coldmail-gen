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

    const data = await response.json()

    if (!response.ok) {
      console.error('Python backend error:', data)
      throw new Error(data.error || 'Failed to generate email')
    }

    if (!data.email) {
      console.error('Invalid response from Python backend:', data)
      throw new Error('Invalid response from server')
    }

    return NextResponse.json(data)
  } catch (error) {
    console.error('Error in generate-email route:', error)
    return NextResponse.json(
      { error: error instanceof Error ? error.message : 'Failed to generate email' },
      { status: 500 }
    )
  }
} 