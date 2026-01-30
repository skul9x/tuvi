"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Lock, Sparkles, ScrollText, PlayCircle } from "lucide-react";

interface MysticUnlockProps {
    onUnlock: () => void;
}

export default function MysticUnlock({ onUnlock }: MysticUnlockProps) {
    const [isUnlocking, setIsUnlocking] = useState(false);

    const handleUnlock = () => {
        setIsUnlocking(true);
        // Add a slight delay for the animation before triggering the actual unlock
        setTimeout(() => {
            onUnlock();
        }, 1500);
    };

    return (
        <div className="relative w-full max-w-2xl mx-auto my-12">
            {/* Mystic Aura Background */}
            <div className="absolute inset-0 bg-gradient-to-r from-purple-900/40 via-indigo-900/40 to-purple-900/40 blur-3xl rounded-full opacity-50 animate-pulse"></div>

            {/* Main Container */}
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="relative bg-slate-900/80 backdrop-blur-md border border-amber-500/30 rounded-xl overflow-hidden shadow-2xl shadow-purple-900/50"
            >
                {/* Decor Border Lines */}
                <div className="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-amber-500/50 to-transparent"></div>
                <div className="absolute bottom-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-amber-500/50 to-transparent"></div>

                <div className="relative p-8 md:p-12 text-center z-10">
                    <AnimatePresence mode="wait">
                        {!isUnlocking ? (
                            <motion.div
                                key="locked"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.9, filter: "blur(10px)" }}
                                transition={{ duration: 0.5 }}
                                className="flex flex-col items-center gap-6"
                            >
                                {/* Floating Icon */}
                                <motion.div
                                    animate={{ y: [0, -10, 0] }}
                                    transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
                                    className="relative group"
                                >
                                    <div className="absolute inset-0 bg-amber-500 blur-xl opacity-20 group-hover:opacity-40 transition-opacity duration-500"></div>
                                    <div className="w-20 h-20 rounded-full border border-amber-500/30 bg-purple-950/50 flex items-center justify-center relative z-10 shadow-[0_0_30px_rgba(245,158,11,0.2)]">
                                        <Lock className="w-8 h-8 text-amber-200 group-hover:text-amber-100 transition-colors" />
                                    </div>
                                    <Sparkles className="absolute -top-2 -right-2 w-6 h-6 text-amber-300 animate-spin-slow opacity-70" />
                                </motion.div>

                                {/* Text Content */}
                                <div className="space-y-3 max-w-lg">
                                    <h3 className="text-2xl md:text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-200 via-amber-100 to-amber-200 uppercase tracking-widest font-serif">
                                        Thiên Cơ Bất Khả Lộ
                                    </h3>
                                    <p className="text-purple-200/70 text-sm md:text-base italic leading-relaxed font-serif">
                                        "Vận mệnh ẩn chứa trong các vì sao. Chỉ người hữu duyên mới mở được phong ấn này để thấu hiểu huyền cơ."
                                    </p>
                                    <p className="text-xs text-slate-500 uppercase tracking-widest mt-2 border-t border-white/5 pt-2 inline-block px-4">
                                        Phân tích chi tiết bởi AI
                                    </p>
                                </div>

                                {/* Action Button */}
                                <motion.button
                                    whileHover={{ scale: 1.05 }}
                                    whileTap={{ scale: 0.95 }}
                                    onClick={handleUnlock}
                                    className="mt-4 group relative px-8 py-4 bg-transparent overflow-hidden rounded-lg font-bold text-amber-400 transition-all hover:text-white"
                                >
                                    <span className="absolute inset-0 w-full h-full -mt-1 rounded-lg opacity-30 bg-gradient-to-b from-transparent via-transparent to-amber-900"></span>
                                    <span className="relative z-10 flex items-center gap-3 text-lg uppercase tracking-wider">
                                        <ScrollText className="w-5 h-5" />
                                        Mở Khóa Luận Giải
                                        <PlayCircle className="w-5 h-5 opacity-0 -ml-4 group-hover:opacity-100 group-hover:ml-0 transition-all duration-300" />
                                    </span>

                                    {/* Glowing Border Button */}
                                    <div className="absolute inset-0 border border-amber-500/50 rounded-lg group-hover:border-amber-400 group-hover:shadow-[0_0_20px_rgba(245,158,11,0.3)] transition-all duration-300"></div>
                                </motion.button>
                            </motion.div>
                        ) : (
                            <motion.div
                                key="unlocking"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="flex flex-col items-center justify-center py-8"
                            >
                                {/* Dissolving Lock Effect */}
                                <motion.div
                                    initial={{ rotate: 0 }}
                                    animate={{ rotate: 360, scale: [1, 1.5, 0] }}
                                    transition={{ duration: 1.5, ease: "easeInOut" }}
                                    className="relative mb-6"
                                >
                                    <div className="w-16 h-16 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <Sparkles className="w-8 h-8 text-amber-200 animate-pulse" />
                                    </div>
                                </motion.div>

                                <motion.p
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 0.5 }}
                                    className="text-amber-200 text-lg font-serif italic"
                                >
                                    Đang kết nối năng lượng vũ trụ...
                                </motion.p>

                                <motion.p
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{ delay: 1 }}
                                    className="text-xs text-purple-400 mt-2 uppercase tracking-wider animate-pulse"
                                >
                                    Đang giải mã thiên bàn
                                </motion.p>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
            </motion.div>
        </div>
    );
}
