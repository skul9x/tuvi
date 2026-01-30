"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import CalendarInput from "./components/CalendarInput";

export default function Home() {
    const router = useRouter();

    const [name, setName] = useState("");
    const [day, setDay] = useState(15);
    const [month, setMonth] = useState(6);
    const [year, setYear] = useState(1995);
    const [hour, setHour] = useState(12);
    const [gender, setGender] = useState(1);
    const [style, setStyle] = useState("Nghiêm túc");
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        const params = new URLSearchParams({
            name,
            day: day.toString(),
            month: month.toString(),
            year: year.toString(),
            hour: hour.toString(),
            gender: gender.toString(),
            style
        });

        router.push(`/result?${params.toString()}`);
    };

    return (
        <main className="min-h-screen w-full relative overflow-hidden bg-[#020617] text-slate-50 font-sans selection:bg-amber-400 selection:text-[#020617]">

            {/* Background Gradient & Effects */}
            <div className="absolute inset-0 bg-[url('/stars-bg.png')] bg-repeat opacity-20 animate-pulse"></div>
            <div className="absolute top-[-20%] right-[-10%] w-[60vw] h-[60vw] bg-violet-600/20 rounded-full blur-[120px] mix-blend-screen animate-pulse"></div>
            <div className="absolute bottom-[-10%] left-[-10%] w-[40vw] h-[40vw] bg-amber-500/10 rounded-full blur-[100px] mix-blend-screen"></div>

            {/* Rotating Mandala Background (Subtle) */}
            <div className="absolute inset-0 pointer-events-none z-0 overflow-hidden flex items-center justify-center">
                <div className="w-[140vh] h-[140vh] border border-white/5 rounded-full flex items-center justify-center opacity-20 animate-spin">
                    <div className="w-[90%] h-[90%] border border-white/5 rounded-full border-dashed"></div>
                </div>
            </div>

            {/* Main Content Container - Split Layout */}
            <div className="relative z-10 w-full max-w-7xl mx-auto px-6 lg:px-8 min-h-screen flex flex-col lg:flex-row items-center justify-center lg:justify-between py-10 lg:py-0 gap-10 lg:gap-20">

                {/* Left Side: Hero Text (Marketing) */}
                <div className="lg:w-1/2 text-center lg:text-left space-y-8 max-w-2xl">
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-amber-400/30 bg-amber-400/5 backdrop-blur-md">
                        <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
                        <span className="text-amber-400 text-xs font-bold tracking-[0.2em] uppercase">AI Powered Horoscope</span>
                    </div>

                    <h1 className="text-5xl lg:text-7xl font-bold leading-tight font-serif drop-shadow-2xl">
                        <span className="block text-slate-50">Khám Phá</span>
                        <span className="block text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-amber-400 to-amber-200 font-decorative">Vận Mệnh Huyền Bí</span>
                    </h1>

                    <p className="text-lg lg:text-xl text-slate-400 font-light leading-relaxed max-w-lg mx-auto lg:mx-0">
                        Kết hợp tinh hoa <strong>Tử Vi Đẩu Số</strong> cổ truyền và sức mạnh <strong>AI Đạo Gia</strong>. Luận giải chi tiết, chính xác từng cung bậc cuộc đời bạn.
                    </p>

                    <div className="flex flex-wrap gap-6 justify-center lg:justify-start pt-4 text-sm text-slate-400 font-mono border-t border-white/10 mt-8">
                        <div className="flex items-center gap-2">
                            <svg className="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                            10k+ Lá số đã lập
                        </div>
                        <div className="flex items-center gap-2">
                            <svg className="w-5 h-5 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
                            AI Version 2.0
                        </div>
                    </div>
                </div>

                {/* Right Side: Action Form (Card) */}
                <div className="w-full lg:w-[480px] shrink-0">
                    <form onSubmit={handleSubmit} className="bg-slate-900/40 backdrop-blur-xl border border-white/10 shadow-xl w-full p-8 rounded-2xl relative overflow-hidden group">

                        {/* Golden Border Glow */}
                        <div className="absolute inset-0 border border-amber-400/20 rounded-2xl pointer-events-none group-hover:border-amber-400/40 transition-colors duration-500"></div>
                        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-amber-400 to-transparent opacity-50"></div>

                        <h2 className="text-3xl font-bold text-center text-slate-50 mb-8 font-serif tracking-wide">Nhập Thông Tin</h2>

                        <div className="space-y-6">
                            {/* Name */}
                            <div className="group">
                                <label className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 block">Họ và Tên</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    className="w-full bg-slate-900/50 border-b border-white/20 text-slate-50 px-4 py-3 outline-none transition-all duration-300 focus:border-amber-400 focus:bg-slate-900/80 placeholder:text-slate-500 rounded-lg focus:ring-1 focus:ring-amber-400/50"
                                    placeholder="Ví dụ: Nguyễn Văn A"
                                    required
                                />
                            </div>

                            {/* Date */}
                            <div className="group">
                                <CalendarInput day={day} month={month} year={year} onChange={(d, m, y) => {
                                    setDay(d); setMonth(m); setYear(y);
                                }} />
                            </div>

                            {/* Time & Gender */}
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 block">Giờ sinh</label>
                                    <div className="relative">
                                        <select
                                            value={hour}
                                            onChange={(e) => setHour(parseInt(e.target.value))}
                                            className="w-full bg-slate-900/50 border-b border-white/20 text-slate-50 px-4 py-3 outline-none transition-all duration-300 focus:border-amber-400 focus:bg-slate-900/80 rounded-lg appearance-none cursor-pointer"
                                        >
                                            {Array.from({ length: 24 }, (_, i) => (
                                                <option key={i} value={i} className="bg-slate-900 text-slate-50">{i} giờ</option>
                                            ))}
                                        </select>
                                    </div>
                                </div>
                                <div>
                                    <label className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 block">Giới tính</label>
                                    <div className="relative">
                                        <select
                                            value={gender}
                                            onChange={(e) => setGender(parseInt(e.target.value))}
                                            className="w-full bg-slate-900/50 border-b border-white/20 text-slate-50 px-4 py-3 outline-none transition-all duration-300 focus:border-amber-400 focus:bg-slate-900/80 rounded-lg appearance-none cursor-pointer"
                                        >
                                            <option value={1} className="bg-slate-900 text-slate-50">Nam</option>
                                            <option value={0} className="bg-slate-900 text-slate-50">Nữ</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            {/* Style */}
                            <div>
                                <label className="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2 block">Giọng văn AI</label>
                                <div className="relative">
                                    <select
                                        value={style}
                                        onChange={(e) => setStyle(e.target.value)}
                                        className="w-full bg-slate-900/50 border-b border-white/20 text-slate-50 px-4 py-3 outline-none transition-all duration-300 focus:border-amber-400 focus:bg-slate-900/80 rounded-lg appearance-none cursor-pointer"
                                    >
                                        <option value="Nghiêm túc" className="bg-slate-900 text-slate-50">📜 Nghiêm túc (Thầy đồ)</option>
                                        <option value="Hài hước" className="bg-slate-900 text-slate-50">🤪 Hài hước (Gen Z)</option>
                                        <option value="Đời thường" className="bg-slate-900 text-slate-50">🍵 Đời thường (Dễ hiểu)</option>
                                        <option value="Kiếm hiệp" className="bg-slate-900 text-slate-50">⚔️ Kiếm hiệp (Cổ trang)</option>
                                        <option value="Chữa lành" className="bg-slate-900 text-slate-50">🌿 Chữa lành (Nhẹ nhàng)</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        {/* Submit Button */}
                        <div className="mt-8">
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full relative overflow-hidden bg-gradient-to-r from-violet-600 to-indigo-600 text-white font-serif font-bold py-3 px-8 rounded shadow-lg shadow-violet-900/50 transition-all hover:scale-105 hover:shadow-violet-600/50 group-hover:shadow-violet-500/80 disabled:opacity-70 disabled:cursor-not-allowed"
                            >
                                {isLoading ? (
                                    <span className="flex items-center justify-center gap-2">
                                        <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                                        Đang Luận Giải...
                                    </span>
                                ) : "LẬP LÁ SỐ NGAY"}
                            </button>
                        </div>

                        <p className="mt-4 text-center text-xs text-slate-500/60">
                            *Thông tin được bảo mật tuyệt đối 100%
                        </p>

                    </form>
                </div>
            </div>
        </main>
    );
}
