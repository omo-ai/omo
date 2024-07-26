import "@/styles/globals.css";
import { Inter, Karla } from "next/font/google";
const inter = Inter({
  weight: ["500", "600", "700"],
  subsets: ["latin"],
  display: "block",
  variable: "--font-inter",
});

const karla = Karla({
  weight: ["400", "700"],
  subsets: ["latin"],
  display: "block",
  variable: "--font-karla",
});

export const metadata = {
  title: 'OmoAI',
  description: 'Combine private data with LLMs',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${karla.variable} ${inter.variable} font-sans`}>
      <body>{children}</body>
    </html>
  )
}
