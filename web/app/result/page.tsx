"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Save, Loader2 } from "lucide-react";
import HoroscopeGrid from "../components/HoroscopeGrid";
import ReadingStream from "../components/ReadingStream";
import { api } from "../lib/api";
import { createClient } from "../lib/supabase";

function ResultContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [user, setUser] = useState<any>(null);
    const [saving, setSaving] = useState(false);
    const [showAI, setShowAI] = useState(false);
    const supabase = createClient();

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

        const checkUser = async () => {
            const { data: { user } } = await supabase.auth.getUser();
            setUser(user);
        };

        checkUser();
        fetchHoroscope();
    }, [name, day, month, year, hour, gender, style, supabase]);

    const handleSave = async () => {
        if (!user) {
            router.push("/login");
            return;
        }
        if (!data) return;

        setSaving(true);
        try {
            const { error } = await (supabase.from("saved_horoscopes") as any).insert({
                user_id: user.id,
                name: data.info.name,
                dob_solar: data.info.solar_date, // Assumes format "DD/MM/YYYY" or similar, better to normalize if needed
                dob_lunar: data.info.lunar_date,
                gender: data.info.gender === "Nam" ? 1 : 0, // Normalize based on API response
                data_json: data
            });

            if (error) throw error;
            alert("Đã lưu lá số thành công!");
        } catch (error: any) {
            console.error("Save error:", error);
            alert("Lỗi khi lưu: " + error.message);
        } finally {
            setSaving(false);
        }
    };

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
                {user ? (
                    <button
                        onClick={handleSave}
                        disabled={saving}
                        className="flex items-center gap-2 text-sm bg-purple-600 hover:bg-purple-500 text-white px-4 py-2 rounded-lg transition-all shadow-lg hover:shadow-purple-500/30 disabled:opacity-50"
                    >
                        {saving ? <Loader2 className="animate-spin" size={16} /> : <Save size={16} />}
                        Lưu Lá Số
                    </button>
                ) : (
                    <Link href="/login" className="text-sm bg-slate-800 hover:bg-slate-700 text-white px-4 py-2 rounded-lg border border-slate-700 transition-colors">
                        Đăng nhập để lưu
                    </Link>
                )}
            </div>

            {/* Grid */}
            <div className="overflow-x-auto pb-4">
                <div className="min-w-[800px] md:min-w-0">
                    <HoroscopeGrid data={data} />
                </div>
            </div>

            {/* AI Reading (Lazy Load) */}
            <div className="mt-8">
                {!showAI ? (
                    <div className="text-center p-8 border border-purple-500/30 rounded-lg bg-purple-900/10 backdrop-blur-sm">
                        <h3 className="text-xl font-bold text-purple-300 mb-4">🔮 Luận Giải Chi Tiết Bởi AI</h3>
                        <p className="text-slate-400 mb-6 text-sm">
                            Hệ thống sẽ sử dụng AI để bình giải chi tiết về Mệnh, Thân, Tài, Quan dựa trên lá số của bạn.
                        </p>
                        <button
                            onClick={() => setShowAI(true)}
                            className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold py-3 px-8 rounded-full shadow-lg hover:shadow-purple-500/40 transition-all transform hover:-translate-y-1 animate-pulse"
                        >
                            ✨ Bấm Để Xem Luận Giải (AI)
                        </button>
                    </div>
                ) : (
                    <ReadingStream dataJson={data} style={style} />
                )}
            </div>
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
