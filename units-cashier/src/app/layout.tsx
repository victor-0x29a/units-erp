import { AuthProvider } from '../';
import type { Metadata } from 'next';
// import { ChakraProvider, createSystem, defineConfig } from '@chakra-ui/react';
import { Provider } from '@/components/ui/provider';
import { Inter } from 'next/font/google';
import './globals.scss';

// const uiConfig = defineConfig({
//     theme: {

//     }
// })

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'Caixa',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
};

export default function RootLayout({
    children,
}: Readonly<{
  children: React.ReactNode;
}>) {
    return (
        <html lang="pt-br" suppressHydrationWarning>
            <body className={inter.className}>
                <Provider>
                    <AuthProvider>
                        {children}
                    </AuthProvider>
                </Provider>
            </body>
        </html>
    );
}
