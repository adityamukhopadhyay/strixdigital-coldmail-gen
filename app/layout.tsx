import './globals.css'
import { Inter } from 'next/font/google'
import type { Metadata } from 'next'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Strix Digital - Cold Email Generator',
  description: 'Internal cold email generation tool for Strix Digital team',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="bg-black">
      <body className={`${inter.className} antialiased bg-black pb-16`}>
        {children}
      </body>
    </html>
  )
}

