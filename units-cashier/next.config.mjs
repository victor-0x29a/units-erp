/** @type {import('next').NextConfig} */
const nextConfig = {
    experimental: {
        optimizePackageImports: ['@chakra-ui/react']
    },
    images: {
        remotePatterns: [
            {
                hostname: 'img.freepik.com',
                pathname: '/fotos-gratis/**',
                protocol: 'https',
                port: ''
            }
        ]
    }
};

export default nextConfig;
