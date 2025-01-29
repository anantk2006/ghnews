import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    async headers() {
      return [
        {
          source: '/:path*',
          headers: [
            {
              key: 'Content-Security-Policy',
              value: `
                script-src 'self' 'unsafe-inline' https://js.stripe.com;
              `.replace(/\s{2,}/g, ' ').trim()
            }
          ],
        }
      ]
    }
  }

export default nextConfig;
