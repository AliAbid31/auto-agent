import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export', // Génère un dossier HTML/CSS/JS statique ultra-rapide pour Cloudflare
  images: {
    unoptimized: true, // Requis si vous utilisez la balise <Image /> de Next.js
  },
};

export default nextConfig;
