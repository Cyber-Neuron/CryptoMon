/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    DATABASE_URL: process.env.DATABASE_URL,
  },
  allowedDevOrigins: ['http://localhost:3000', 'https://gentle-llama-luckily.ngrok-free.app'], // Add your development origins here
}

export default nextConfig; 