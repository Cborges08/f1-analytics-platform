import "./globals.css";

export const metadata = {
  title: "F1 Analytics Dashboard",
  description: "ML-powered Formula 1 race predictions and analytics",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
