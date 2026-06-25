import type { NextConfig } from "next"

const nextConfig: NextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "img.clerk.com",
      },
      {
        protocol: "https",
        hostname: "images.clerk.dev",
      },
    ],
  },
  serverExternalPackages: ["@prisma/client", "prisma"],
  // Disable Turbopack for daemon-compatible operation
  turbopack: undefined,
}

export default nextConfig
