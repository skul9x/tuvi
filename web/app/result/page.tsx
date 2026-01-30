"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import HoroscopeGrid from "../components/HoroscopeGrid";
import ReadingStream from "../components/ReadingStream";
import { api } from "../lib/api";

function ResultContent() {
    const searchParams = useSearchParams();
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const name = searchParams.get("name");
    const day = searchParams.get("day");
    const month = searchParams.get("month");
    const year = searchParams.get("year");
    const hour = searchParams.get("hour");
    const gender = searchParams.get("gender");
    const style = searchParams.get("style") || "Nghiêm túc";

    useEffect(() => {
        if (!name || !day || !month || !year) return;

        const fetchHoroscope = async () => {
            try {
                setLoading(true);
                const jsonData = await api.ansao({
                    name,
                    day: parseInt(day!),
                    month: parseInt(month!),
                    year: parseInt(year!),
                    hour: parseInt(hour || "0"),
                    gender: parseInt(gender || "1"),
                    viewing_year: new Date().getFullYear()
                });
                // Inject style into data for prompt construction later checks
                jsonData.info.reading_style = style;

                setData(jsonData);
            } catch (err: any) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchHoroscope();
    }, [name, day, month, year, hour, gender, style]);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[50vh] text-white">
                <div className="w-16 h-16 border-4 border-t-purple-500 border-white/20 rounded-full animate-spin mb-4"></div>
                <p className="animate-pulse text-purple-300">Đang lập lá số thiên bàn...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="text-center p-8 bg-red-900/50 rounded-lg border border-red-500 text-white">
                <h2 className="text-xl font-bold mb-2">Lỗi</h2>
                <p>{error}</p>
                <Link href="/" className="inline-block mt-4 text-sm underline hover:text-red-300">Quay lại</Link>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            {/* Actions */}
            <div className="flex justify-between items-center">
                <Link href="/" className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors">
                    <ArrowLeft size={16} /> Lập lá số khác
                </Link>
                <button className="text-sm bg-purple-600 hover:bg-purple-500 text-white px-3 py-1 rounded">
                    Lưu Lá Số (Comming Soon)
                </button>
            </div>

            {/* Grid */}
            <div className="overflow-x-auto pb-4">
                <div className="min-w-[800px] md:min-w-0">
                    <HoroscopeGrid data={data} />
                </div>
            </div>

            {/* AI Reading */}
            <ReadingStream dataJson={data} style={style} />
        </div>
    );
}

export default function ResultPage() {
    return (
        <main className="min-h-screen bg-slate-950 p-4 md:p-8">
            <Suspense fallback={<div className="text-white text-center">Loading...</div>}>
                <ResultContent />
            </Suspense>
        </main>
    );
}
