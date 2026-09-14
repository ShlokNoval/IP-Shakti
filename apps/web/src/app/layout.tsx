import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "IP-SHAKTI Sahayak | Ayurvedic IP Advisor",
  description: "Advanced Ayurvedic Regulatory & IP Assistant.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
