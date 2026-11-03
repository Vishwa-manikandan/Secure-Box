import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
import { TopNav } from "@/components/TopNav";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Securebox | AI Security Intelligence",
  description: "Professional AI-powered code security and skill intelligence platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={cn(inter.className, "bg-background text-foreground antialiased")}>
        <div className="flex min-h-screen">
          <Sidebar />
          <div className="flex-1 ml-64 flex flex-col">
            <TopNav />
            <main className="p-6 flex-1 overflow-auto">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}

// Helper function for the body class to avoid import issues in layout.tsx
function cn(...classes: (string | boolean | undefined)[]) {
  return classes.filter(Boolean).join(" ");
}
