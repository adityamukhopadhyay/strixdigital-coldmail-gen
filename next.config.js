/** @type {import('next').NextConfig} */
const nextConfig = {
reactStrictMode: true,
swcMinify: true,
images: {
    domains: [],
    remotePatterns: [],
},
typescript: {
    ignoreBuildErrors: false,
},
experimental: {
    typedRoutes: true,
}
}

module.exports = nextConfig

