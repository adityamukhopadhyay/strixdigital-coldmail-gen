'use client'

import { motion } from 'framer-motion'
import Image from 'next/image'
import Link from 'next/link'

export default function Header() {
  return (
    <div className="flex items-center justify-center w-full">
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-[450px] mx-auto py-4"
      >
        <Link 
          href="https://strixdigital.in" 
          target="_blank" 
          rel="noopener noreferrer"
        >
          <Image 
            src="/strix-digital-logo.png"
            alt="Strix Digital Logo"
            width={400}
            height={133}
            className="w-full h-auto"
            priority
          />
        </Link>
      </motion.div>
    </div>
  )
}

