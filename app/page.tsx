'use client'

import dynamic from 'next/dynamic'

const Header = dynamic(() => import('@/components/Header'), { ssr: false })
const EmailGenerator = dynamic(() => import('@/components/EmailGenerator'), { ssr: false })
const Footer = dynamic(() => import('@/components/Footer'), { ssr: false })

export default function Home() {
  return (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-2">
        <div className="flex items-center justify-center p-8 bg-[#0d1117] min-h-[200px]">
          <div className="w-full max-w-4xl px-4">
            <Header />
          </div>
        </div>
        <div className="flex flex-col bg-black">
          <EmailGenerator />
        </div>
      </div>
      <Footer />
    </>
  )
}

