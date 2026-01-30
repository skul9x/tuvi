import type { Metadata } from "next";
import { Inter, Cinzel, Cinzel_Decorative } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const cinzel = Cinzel({ subsets: ["latin"], variable: "--font-cinzel" });
const cinzelDecorative = Cinzel_Decorative({
    weight: ["400", "700"],
    subsets: ["latin"],
    variable: "--font-cinzel-decorative"
});

export const metadata: Metadata = {
    metadataBase: new URL("https://tuvi-lac.vercel.app"),
    title: {
        template: "%s | Tử Vi Huyền Bí",
        default: "Tử Vi Huyền Bí - Luận Giải Vận Mệnh Bằng AI",
    },
    description: "Khám phá bản đồ vận mệnh của bạn với sự kết hợp giữa Tử Vi Đẩu Số cổ truyền và Trí tuệ nhân tạo (AI). Luận giải chi tiết, chính xác, và mang đậm phong cách huyền học.",
    keywords: ["Tử vi", "Lá số tử vi", "Xem bói AI", "Luận giải tử vi", "Phong thủy", "Vận mệnh", "Tử vi 2026"],
    authors: [{ name: "Tử Vi Huyền Bí AI" }],
    openGraph: {
        title: "Tử Vi Huyền Bí - Luận Giải Vận Mệnh Bằng AI",
        description: "Khám phá bản đồ vận mệnh của bạn với sự kết hợp giữa Tử Vi Đẩu Số cổ truyền và Trí tuệ nhân tạo (AI).",
        url: "https://tuvi-lac.vercel.app",
        siteName: "Tử Vi Huyền Bí",
        images: [
            {
                url: "/og-image.jpg",
                width: 1200,
                height: 630,
                alt: "Tử Vi Huyền Bí AI",
            },
        ],
        locale: "vi_VN",
        type: "website",
    },
    twitter: {
        card: "summary_large_image",
        title: "Tử Vi Huyền Bí - Luận Giải Vận Mệnh Bằng AI",
        description: "Xem tử vi online chuẩn xác với AI.",
        images: ["/og-image.jpg"],
    },
    icons: {
        icon: "/favicon.ico",
    },
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="vi">
            <body className={`${inter.variable} ${cinzel.variable} ${cinzelDecorative.variable} font-sans bg-[#020617] text-slate-50 relative`}>
                {children}
            </body>
        </html>
    );
}
