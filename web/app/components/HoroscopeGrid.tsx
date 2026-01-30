"use client";

import React from 'react';

// Define simplified types just for UI
interface Star {
    name: string;
    ngu_hanh: string;
    dac_tinh?: string;
}

interface Cung {
    name: string;
    hanh: string;
    vi_tri_dia_ban: string;
    chinh_tinh: Star[];
    phu_tinh: Star[];
    // Add other properties as needed
}

interface HoroscopeGridProps {
    data: any; // Using any for rapid prototyping, better to define full type later
}

export default function HoroscopeGrid({ data }: HoroscopeGridProps) {
    if (!data || !data.cung) return <div className="text-center p-10">Chưa có dữ liệu</div>;

    // Map 12 Cung to 4x4 Grid positions
    // Grid layout:
    // Ty   Ngo  Mui  Than
    // Thin           Dau
    // Mao            Tuat
    // Dan  Suu  Ty   Hoi

    // Actually, standard Tu Vi is:
    // Tị   Ngọ  Mùi  Thân (Top: SSE, S, SSW, WSW...) -> Wait, mapping standard:
    // 0: Ty (North) -> Usually Bottom-Right or Bottom-Center?
    // Let's us standard "Dia Ban" index from 0-11 (Ty -> Hoi)
    // 0: Ty, 1: Suu, 2: Dan, 3: Mao, 4: Thin, 5: Ti, 6: Ngo, 7: Mui, 8: Than, 9: Dau, 10: Tuat, 11: Hoi

    // Visual Grid 4x4 (indices 0..15)
    // [0]  [1]  [2]  [3]
    // [4]  [Center]  [7]
    // [8]  [Center]  [11]
    // [12] [13] [14] [15]

    // Standard Layout (Clockwise from Bottom-Left? Or Standard convention?)
    // Top Row:    Ty(SE) Ngo(S) Mui(SW) Than(W)  -> 5, 6, 7, 8
    // Right Col:  Than(W) Dau(NW) Tuat(NW) Hoi(N)-> 8, 9, 10, 11 ?

    // Let's stick to standard Vietnamese Tu Vi layout:
    // Tị(5)  Ngọ(6)  Mùi(7)  Thân(8)
    // Thìn(4)                Dậu(9)
    // Mão(3)                 Tuất(10)
    // Dần(2)  Sửu(1)  Tý(0)   Hợi(11)

    // So:
    // Row 1: 5 6 7 8
    // Row 2: 4, Center, 9
    // Row 3: 3, Center, 10
    // Row 4: 2 1 0 11

    const getCungByIndex = (idx: number) => data.cung.find((c: any) => c.vitri_dia_ban_idx === idx);

    // Helper to Render a Cell
    const CungCell = ({ idx }: { idx: number }) => {
        const cung = getCungByIndex(idx);
        if (!cung) return <div className="border border-gray-700 bg-gray-900"></div>;

        return (
            <div className="border border-gray-700 bg-white dark:bg-slate-900 p-1 flex flex-col justify-between h-32 md:h-48 text-[10px] md:text-xs overflow-hidden relative">
                {/* Header: Name + Dai Van */}
                <div className="flex justify-between items-center font-bold text-red-600 dark:text-red-400 border-b border-gray-100 dark:border-gray-700 pb-1">
                    <span>{cung.name}</span>
                    <span className="text-gray-400">{cung.cuc_idx || ''}</span>
                    {/* Note: cung.cuc_idx might not be Dai Van numeral. Adjust later based on real data structure */}
                </div>

                {/* Chinh Tinh */}
                <div className="flex flex-col mt-1">
                    {cung.chinh_tinh.map((star: any, i: number) => (
                        <span key={i} className={`font-bold ${star.dac_tinh === 'V' || star.dac_tinh === 'M' ? 'text-yellow-600 dark:text-yellow-400' : 'text-gray-800 dark:text-white'
                            }`}>
                            {star.name} <span className="text-[9px] font-normal opacity-70">({star.dac_tinh})</span>
                        </span>
                    ))}
                </div>

                {/* Footer: Position Name */}
                <div className="absolute bottom-1 right-1 text-gray-300 font-serif uppercase tracking-widest text-[10px]">
                    {cung.vi_tri_dia_ban}
                </div>
            </div>
        );
    };

    // Center Box (Thien Ban)
    const CenterBox = () => (
        <div className="col-span-2 row-span-2 border border-gray-700 bg-amber-50 dark:bg-slate-800 p-4 flex flex-col items-center justify-center text-center">
            <h2 className="text-lg font-bold text-red-700 uppercase mb-2">{data.info.name}</h2>
            <p className="text-sm">Âm Dương: {data.info.can_chi} ({data.info.nam_nu})</p>
            <p className="text-sm">Mệnh: {data.info.menh_text}</p>
            <p className="text-sm">Cục: {data.info.cuc}</p>
            <div className="mt-4 text-xs text-gray-500">
                An Sao bởi TuViHuyenBi
            </div>
        </div>
    );

    return (
        <div className="grid grid-cols-4 gap-0 border-2 border-slate-800 rounded-lg overflow-hidden shadow-2xl max-w-4xl mx-auto">
            {/* Row 1 */}
            <CungCell idx={5} /> <CungCell idx={6} /> <CungCell idx={7} /> <CungCell idx={8} />

            {/* Row 2 */}
            <CungCell idx={4} />
            <CenterBox />
            <CungCell idx={9} />

            {/* Row 3 */}
            <CungCell idx={3} />
            {/* Center Box spans 2 rows, so explicit grid placement is better actually if strict grid. 
            Standard Grid auto-placement can be tricky with row-spans in middle.
            Let's accept CSS Grid implicit auto-placement logic:
            R1: [5][6][7][8]
            R2: [4][Center][9] -> Center spans 2 cols, 2 rows. 
            R3: [3][10] -> Wait, if center takes 2x2, R2 has [4][Center][Center][9]. R3 has [3][Center][Center][10].
        */}
            <CungCell idx={10} />

            {/* Row 4 */}
            <CungCell idx={2} /> <CungCell idx={1} /> <CungCell idx={0} /> <CungCell idx={11} />
        </div>
    );
}
