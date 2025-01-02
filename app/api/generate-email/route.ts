import { NextResponse } from 'next/server'

interface JobRequest {
  job_link: string;
}

interface ErrorResponse {
  error: string;
  type?: string;
}

export async function POST(request: Request) {
  try {
    console.log('Starting email generation request...')
    
    const body = await request.json() as JobRequest
    console.log('Request body:', body)
    
    if (!body.job_link) {
      console.error('Missing job_link in request')
      return NextResponse.json(
        { error: 'Job link is required' },
        { status: 400 }
      )
    }

    console.log('Forwarding request to Python backend...')
    
    // Forward the request to our Python backend
    const response = await fetch(new URL('/api/python/generate_email', request.url).toString(), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    }).catch(error => {
      console.error('Network error while calling Python backend:', error)
      throw new Error('Failed to connect to email generation service')
    })

    console.log('Received response from Python backend, status:', response.status)

    let data: { email?: string } | ErrorResponse
    try {
      data = await response.json()
      console.log('Response data structure:', Object.keys(data))
    } catch (error) {
      console.error('Failed to parse Python backend response:', error)
      throw new Error('Invalid response from server')
    }

    if (!response.ok) {
      console.error('Python backend error:', {
        status: response.status,
        data: data
      })
      
      // If we have a structured error response from Python
      if ('error' in data) {
        throw new Error(data.error)
      }
      
      throw new Error('Failed to generate email')
    }

    if (!('email' in data) || !data.email) {
      console.error('Invalid response structure from Python backend:', data)
      throw new Error('Invalid response format from server')
    }

    console.log('Successfully generated email, length:', data.email.length)
    return NextResponse.json({ email: data.email })
  } catch (error: unknown) {
    console.error('Error in generate-email route:', {
      name: error instanceof Error ? error.name : 'UnknownError',
      message: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : 'No stack trace'
    })
    
    // Determine appropriate error message
    let errorMessage = 'Failed to generate email'
    if (error instanceof Error) {
      errorMessage = error.message
      if (error.message.includes('fetch') || error.message.includes('network')) {
        errorMessage = 'Connection error: Please try again'
      } else if (error.message.includes('parse') || error.message.includes('invalid')) {
        errorMessage = 'Server error: Invalid response format'
      } else if (error.message.includes('GROQ_API_KEY')) {
        errorMessage = 'Server configuration error: Please contact support'
      }
    }

    return NextResponse.json(
      { error: errorMessage },
      { status: 500 }
    )
  }
} 