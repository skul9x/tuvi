import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/ansao",
        destination: "/api/ansao.py",
      },
      {
        source: "/api/chat",
        destination: "/api/chat.py",
      },
      {
        source: "/api/index",
        destination: "/api/index.py",
      },
    ];
  },
};

export default nextConfig;
