/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "media.formula1.com",
      },
    ],
  },
};

module.exports = nextConfig;
