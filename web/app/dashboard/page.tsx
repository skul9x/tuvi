"use client";

import { useEffect, useState } from "react";
import { createClient } from "../lib/supabase";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { LogOut, Plus, Trash2, Calendar, User } from "lucide-react";
import { Database } from "@/types/database.types";

type Horoscope = Database["public"]["Tables"]["saved_horoscopes"]["Row"];

export default function DashboardPage() {
    const [horoscopes, setHoroscopes] = useState<Horoscope[]>([]);
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState<any>(null);
    const router = useRouter();
    const supabase = createClient();

    useEffect(() => {
        const checkUser = async () => {
            const {
                data: { user },
            } = await supabase.auth.getUser();

            if (!user) {
                router.push("/login");
                return;
            }
            setUser(user);
            fetchHoroscopes(user.id);
        };

        checkUser();
    }, [router, supabase]);

    const fetchHoroscopes = async (userId: string) => {
        try {
            const { data, error } = await supabase
                .from("saved_horoscopes")
                .select("*")
                .eq("user_id", userId)
                .order("created_at", { ascending: false });

            if (error) throw error;
            setHoroscopes(data || []);
        } catch (error) {
            console.error("Error fetching horoscopes:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        await supabase.auth.signOut();
        router.push("/login");
    };

    const handleDelete = async (id: string) => {
        if (!confirm("Bạn có chắc chắn muốn xóa lá số này?")) return;

        try {
            const { error } = await supabase
                .from("saved_horoscopes")
                .delete()
                .eq("id", id);

            if (error) throw error;
            setHoroscopes(horoscopes.filter((h) => h.id !== id));
        } catch (error) {
            console.error("Error deleting horoscope:", error);
            alert("Xóa thất bại");
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
                <div className="animate-spin w-8 h-8 border-4 border-amber-500 border-t-transparent rounded-full"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 text-white p-4 md:p-8">
            <header className="max-w-6xl mx-auto flex justify-between items-center mb-12">
                <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-full bg-amber-600 flex items-center justify-center font-bold text-lg">
                        {user?.user_metadata?.full_name?.charAt(0) || user?.email?.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <h1 className="font-bold text-lg">{user?.user_metadata?.full_name || "Thành viên"}</h1>
                        <p className="text-xs text-slate-400">{user?.email}</p>
                    </div>
                </div>

                <button
                    onClick={handleLogout}
                    className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg transition-colors text-sm"
                >
                    <LogOut size={16} /> Đăng xuất
                </button>
            </header>

            <main className="max-w-6xl mx-auto">
                <div className="flex justify-between items-end mb-6">
                    <div>
                        <h2 className="text-2xl font-bold text-amber-100">Kho Lá Số</h2>
                        <p className="text-slate-400 text-sm mt-1">Lưu trữ và quản lý các lá số đã lập</p>
                    </div>
                    <Link href="/" className="flex items-center gap-2 bg-amber-600 hover:bg-amber-500 px-4 py-2 rounded-lg font-medium transition-all shadow-lg hover:shadow-amber-500/20">
                        <Plus size={18} /> Lập Lá Số Mới
                    </Link>
                </div>

                {horoscopes.length === 0 ? (
                    <div className="text-center py-20 bg-slate-900/50 border border-slate-800 rounded-2xl border-dashed">
                        <p className="text-slate-500 mb-4">Chưa có lá số nào được lưu.</p>
                        <Link href="/" className="text-amber-400 hover:text-amber-300 underline">
                            Tạo lá số đầu tiên ngay
                        </Link>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {horoscopes.map((h) => (
                            <div
                                key={h.id}
                                className="bg-slate-900 border border-slate-800 rounded-xl p-6 hover:border-amber-500/50 transition-all group relative overflow-hidden"
                            >
                                <div className="absolute top-0 left-0 w-1 h-full bg-amber-500 opacity-50"></div>
                                <div className="flex justify-between items-start mb-4">
                                    <h3 className="font-bold text-lg text-amber-100 group-hover:text-amber-400 transition-colors">
                                        {h.name}
                                    </h3>
                                    <div className="flex gap-2">
                                        <Link
                                            href={`/result?name=${encodeURIComponent(h.name)}&day=${h.dob_solar.includes('/') ? h.dob_solar.split('/')[0] : h.dob_solar.split('-')[2]}&month=${h.dob_solar.includes('/') ? h.dob_solar.split('/')[1] : h.dob_solar.split('-')[1]}&year=${h.dob_solar.includes('/') ? h.dob_solar.split('/')[2] : h.dob_solar.split('-')[0]}&hour=0&gender=${h.gender}&style=${encodeURIComponent("Nghiêm túc")}`}
                                            className="p-2 bg-slate-800 rounded hover:bg-slate-700 text-xs"
                                        >
                                            Xem
                                        </Link>
                                        <button
                                            onClick={() => handleDelete(h.id)}
                                            className="p-2 bg-slate-800 rounded hover:bg-red-900/50 hover:text-red-400 transition-colors"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                </div>

                                <div className="space-y-2 text-sm text-slate-400">
                                    <div className="flex items-center gap-2">
                                        <Calendar size={14} className="text-slate-500" />
                                        <span>DL: {h.dob_solar}</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <User size={14} className="text-slate-500" />
                                        <span>Giới tính: {h.gender === 1 ? "Nam" : "Nữ"}</span>
                                    </div>
                                </div>

                                <div className="mt-4 text-xs text-slate-600 pt-4 border-t border-slate-800">
                                    Đã tạo: {new Date(h.created_at).toLocaleDateString('vi-VN')}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}
