export default function PrivacyPolicy() {
    return (
        <main className="min-h-screen w-full bg-[#020617] text-slate-300 font-sans py-20 px-6 lg:px-8 relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-[url('/stars-bg.png')] bg-repeat opacity-20 pointer-events-none"></div>
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-violet-900/20 rounded-full blur-[120px] pointer-events-none"></div>

            <div className="max-w-3xl mx-auto relative z-10">
                <div className="mb-12 text-center">
                    <h1 className="text-4xl lg:text-5xl font-bold font-serif bg-clip-text text-transparent bg-gradient-to-r from-amber-200 via-amber-400 to-amber-200 mb-4">
                        Chính Sách Bảo Mật
                    </h1>
                    <p className="text-slate-400">Cập nhật lần cuối: {new Date().toLocaleDateString('vi-VN')}</p>
                </div>

                <div className="space-y-8 glass-panel p-8 rounded-2xl border border-white/5 bg-slate-900/50 backdrop-blur-md shadow-2xl">
                    <section>
                        <h2 className="text-2xl font-bold text-amber-400 font-serif mb-4">1. Thu Thập Thông Tin</h2>
                        <p className="leading-relaxed">
                            Chúng tôi thu thập các thông tin sau để thực hiện luận giải tử vi:
                        </p>
                        <ul className="list-disc list-inside mt-2 space-y-1 text-slate-300 ml-4">
                            <li>Họ và tên</li>
                            <li>Ngày, tháng, năm sinh</li>
                            <li>Giờ sinh</li>
                            <li>Giới tính</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-amber-400 font-serif mb-4">2. Mục Đích Sử Dụng</h2>
                        <p className="leading-relaxed">
                            Thông tin của bạn CHỈ được sử dụng cho mục đích:
                        </p>
                        <ul className="list-disc list-inside mt-2 space-y-1 text-slate-300 ml-4">
                            <li>Lập lá số Tử Vi Đẩu Số.</li>
                            <li>Gửi yêu cầu đến AI để phân tích và luận giải vận mệnh.</li>
                            <li>Cải thiện chất lượng phản hồi của hệ thống.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-amber-400 font-serif mb-4">3. Bảo Mật Dữ Liệu</h2>
                        <p className="leading-relaxed">
                            Chúng tôi cam kết:
                        </p>
                        <ul className="list-disc list-inside mt-2 space-y-1 text-slate-300 ml-4">
                            <li>Không chia sẻ thông tin cá nhân của bạn với bên thứ ba.</li>
                            <li>Mọi dữ liệu truyền tải đều được mã hóa (HTTPS).</li>
                            <li>Chúng tôi không lưu trữ thông tin nhạy cảm vĩnh viễn nếu không có sự đồng ý của bạn.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-2xl font-bold text-amber-400 font-serif mb-4">4. Liên Hệ</h2>
                        <p className="leading-relaxed">
                            Nếu có thắc mắc, vui lòng liên hệ: support@tuvi-huyenbi.com
                        </p>
                    </section>
                </div>

                <div className="mt-12 text-center">
                    <a href="/" className="inline-flex items-center gap-2 text-amber-400 hover:text-amber-300 transition-colors font-bold uppercase tracking-wider text-sm">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" /></svg>
                        Quay về trang chủ
                    </a>
                </div>
            </div>
        </main>
    );
}
