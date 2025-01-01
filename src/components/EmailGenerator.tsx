'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Copy, Sparkles, Check } from 'lucide-react'
import { toast } from 'sonner'

export default function EmailGenerator() {
  const [jobLink, setJobLink] = useState('')
  const [generatedEmail, setGeneratedEmail] = useState('')
  const [isCopied, setIsCopied] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsGenerating(true)
    try {
      const response = await fetch('/api/generate-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_link: jobLink })
      })

      if (!response.ok) {
        throw new Error('Failed to generate email')
      }

      const data = await response.json()
      setGeneratedEmail(data.email)
      toast.success('Email generated successfully!')
    } catch (error) {
      console.error('Error:', error)
      toast.error('Failed to generate email. Please try again.')
    } finally {
      setIsGenerating(false)
    }
  }

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(generatedEmail)
      setIsCopied(true)
      toast.success('Email copied to clipboard!')
      setTimeout(() => setIsCopied(false), 2000)
    } catch (err) {
      toast.error('Failed to copy email')
    }
  }

  return (
    <div className="flex-1 flex flex-col justify-center px-8 py-12 bg-black">
      <div className="space-y-8 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center space-y-4"
        >
          <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent px-4">
            Cold Emails in a Blink of an Eye!
          </h1>
          <p className="text-gray-400 text-base md:text-lg px-4">
            Transform job requirements into compelling cold emails instantly.
            Just paste the job link, and watch the magic happen! ✨
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="bg-[#0d1117] p-6 rounded-lg"
        >
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="jobLink" className="block mb-2 text-base font-medium text-gray-200">
                Job Link / Requirements
              </label>
              <Input
                id="jobLink"
                type="url"
                value={jobLink}
                onChange={(e) => setJobLink(e.target.value)}
                placeholder="https://example.com/job-posting"
                required
                className="bg-black/50 border-gray-700 text-white text-base"
                disabled={isGenerating}
              />
            </div>
            <Button 
              type="submit" 
              className="w-full bg-white text-black hover:bg-gray-100"
              disabled={isGenerating}
            >
              <Sparkles className="mr-2 h-4 w-4" />
              {isGenerating ? 'Generating...' : 'Generate Email'}
            </Button>
          </form>
        </motion.div>

        {generatedEmail && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="bg-[#0d1117] p-6 rounded-lg"
          >
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-white">Generated Email</h2>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={copyToClipboard} 
                className="hidden sm:flex border-gray-700 text-black"
                disabled={isGenerating}
              >
                {isCopied ? <Check className="mr-2 h-4 w-4" /> : <Copy className="mr-2 h-4 w-4" />}
                {isCopied ? 'Copied' : 'Copy to Clipboard'}
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={copyToClipboard} 
                className="sm:hidden border-gray-700 text-black"
                disabled={isGenerating}
              >
                {isCopied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
              </Button>
            </div>
            <Textarea
              value={generatedEmail}
              readOnly
              className="w-full h-[500px] bg-black/50 border-gray-700 text-gray-200 font-mono text-sm"
            />
          </motion.div>
        )}
      </div>
    </div>
  )
}

