"use client";

import React from 'react';

interface Star {
    name: string;
    ngu_hanh: string;
    dac_tinh?: string;
    am_duong_ngu_hanh?: string;
}

interface Cung {
    name: string;
    hanh: string;
    vi_tri_dia_ban: string;
    vi_tri_dia_ban_idx: number;
    chinh_tinh: Star[] | string[];
    phu_tinh: Star[] | string[];
    dai_van_idx?: number;
    tieu_van_idx?: string;
    cuc_idx?: string;
    am_duong?: number;
}

interface HoroscopeGridProps {
    data: any;
}

export default function HoroscopeGrid({ data }: HoroscopeGridProps) {
    if (!data || !data.cung) return <div className="text-center p-10 text-amber-200">Đang tải dữ liệu lá số...</div>;

    const getCungByIndex = (idx: number) => {
        if (Array.isArray(data.cung)) {
            return data.cung.find((c: any) => c.vitri_dia_ban_idx === idx) || data.cung[idx];
        }
        return data.cung[String(idx)] || data.cung[idx];
    };

    // Helper to render stars safely
    const renderStars = (stars: any[], className: string) => {
        if (!stars || !Array.isArray(stars)) return null;
        return stars.map((star, i) => {
            const name = typeof star === 'string' ? star : star.name;
            const dacTinh = typeof star === 'string' ? '' : star.dac_tinh;
            // Highlight Vượng/Miếu
            const isGood = dacTinh === 'V' || dacTinh === 'M';
            const isBad = dacTinh === 'H';

            let colorClass = className;
            if (isGood) colorClass = "font-bold text-red-700";
            if (isBad) colorClass = "text-slate-500";
            if (className.includes("text-blue") || className.includes("text-purple")) {
                // Keep intended color for Phu Tinh groups if not V/M overrides
                if (isBad) colorClass = "text-slate-500";
            }

            return (
                <span key={i} className={`block leading-tight ${colorClass} text-[10px] sm:text-xs`}>
                    {name} <span className="text-[9px] font-normal opacity-70">{dacTinh}</span>
                </span>
            );
        });
    };

    const CungCell = ({ idx, area }: { idx: number, area: string }) => {
        const cung = getCungByIndex(idx);
        if (!cung) return null;

        return (
            <div className="relative border border-amber-900/30 p-1 md:p-2 flex flex-col justify-between h-full overflow-hidden hover:bg-amber-500/5 transition-colors group"
                style={{ gridArea: area }}>

                {/* Header: Cung Name & Dai Van */}
                <div className="flex justify-between items-start border-b border-amber-900/10 pb-1 mb-1 shadow-sm">
                    <span className="font-bold text-red-800 uppercase text-xs md:text-sm bg-amber-200/50 px-1 rounded">
                        {cung.name}
                    </span>
                    <span className="font-bold text-gray-500 text-xs">
                        {cung.cuc_idx || cung.dai_van_idx}
                    </span>
                </div>

                {/* Stars Content */}
                <div className="flex-1 flex flex-wrap gap-1 content-start overflow-y-auto hidden-scrollbar">
                    <div className="w-1/2 pr-1 border-r border-amber-900/10">
                        {/* Chinh Tinh */}
                        {renderStars(cung.chinh_tinh, "text-black font-semibold")}
                    </div>
                    <div className="w-1/2 pl-1">
                        {/* Phu Tinh (Simplified grouping for display) */}
                        {renderStars(cung.phu_tinh, "text-indigo-800")}
                    </div>
                </div>

                {/* Footer: Position & Tieu Van */}
                <div className="mt-1 pt-1 border-t border-amber-900/10 flex justify-between items-end">
                    <span className="text-[10px] text-gray-500 font-serif italic">
                        {cung.tieu_van_idx}
                    </span>
                    <span className="font-serif font-bold text-amber-900/40 uppercase text-xs tracking-widest absolute bottom-0 right-1 pointer-events-none group-hover:text-amber-900/80 transition-colors">
                        {cung.vi_tri_dia_ban}
                    </span>
                </div>
            </div>
        );
    };

    return (
        <div className="w-full max-w-5xl mx-auto shadow-2xl rounded-sm border-4 border-double border-amber-900 bg-[#fdfbf7] p-1 parchment-bg text-amber-950 font-serif">
            <div className="grid gap-0 w-full aspect-square md:aspect-[4/3] min-h-[600px]"
                style={{
                    gridTemplateColumns: "1fr 1fr 1fr 1fr",
                    gridTemplateRows: "1fr 1fr 1fr 1fr",
                    gridTemplateAreas: `
                        "c5 c6 c7 c8"
                        "c4 ct ct c9"
                        "c3 ct ct c10"
                        "c2 c1 c0 c11"
                     `
                }}>

                {/* Top Row */}
                <CungCell idx={5} area="c5" />
                <CungCell idx={6} area="c6" />
                <CungCell idx={7} area="c7" />
                <CungCell idx={8} area="c8" />

                {/* Middle Left */}
                <CungCell idx={4} area="c4" />
                <CungCell idx={3} area="c3" />

                {/* Center Box */}
                <div style={{ gridArea: "ct" }} className="flex flex-col items-center justify-center text-center p-4 border-4 border-double border-amber-900/20 m-2 bg-white/40 shadow-inner rounded-xl">
                    <h1 className="text-2xl md:text-4xl font-bold text-red-800 uppercase mb-2 drop-shadow-sm tracking-wider">
                        {data.info.name}
                    </h1>
                    <div className="space-y-1 text-sm md:text-base font-medium text-amber-950">
                        <p>Dương Lịch: {data.info.solar_date} - {data.info.time}</p>
                        <p>Âm Lịch: {data.info.lunar_date}</p>
                        <p>Bát Tự: {data.info.can_chi}</p>
                        <div className="w-full h-px bg-amber-900/30 my-3"></div>
                        <p className="font-bold text-indigo-900">
                            {data.info.menh_text || data.info.menh_tai}
                            <span className="mx-2">•</span>
                            Cục: {data.info.cuc}
                        </p>
                        <p>Chủ Mệnh: {data.info.chu_menh} • Chủ Thân: {data.info.chu_than}</p>
                        <p className="font-bold text-amber-900 mt-1">Giới tính: {data.info.gender}</p>
                    </div>
                    <div className="mt-6">
                        <img src="/yin-yang.png" alt="Yin Yang" className="w-12 h-12 opacity-20 animate-spin-slow" onError={(e) => e.currentTarget.style.display = 'none'} />
                    </div>
                </div>

                {/* Middle Right */}
                <CungCell idx={9} area="c9" />
                <CungCell idx={10} area="c10" />

                {/* Bottom Row */}
                <CungCell idx={2} area="c2" />
                <CungCell idx={1} area="c1" />
                <CungCell idx={0} area="c0" />
                <CungCell idx={11} area="c11" />
            </div>
        </div>
    );
}
