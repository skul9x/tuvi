from core.constants import DIA_CHI, CHINH_TINH, CUC, THIEN_CAN
from core.lunar import LunarConverter
from core.config import ConfigManager
from core.logger import setup_logger

logger, _ = setup_logger()

class TuViLogic:
    def __init__(self, solar_day, solar_month, solar_year, hour, gender, name=""):
        self.solar_day = solar_day
        self.solar_month = solar_month
        self.solar_year = solar_year
        self.hour = hour # 0-23
        self.gender = gender # 1 = Nam, 0 = Nữ
        self.name = name
        
        # Convert to Lunar
        self.lunar_day, self.lunar_month, self.lunar_year, self.leap = LunarConverter.convert_solar_to_lunar(solar_day, solar_month, solar_year)
        logger.debug(f"Converted to Lunar: {self.lunar_day}/{self.lunar_month}/{self.lunar_year}")
        self.can_nam = LunarConverter.get_can_nam_index(self.lunar_year)
        self.chi_nam = LunarConverter.get_chi_nam_index(self.lunar_year)
        self.chi_gio = LunarConverter.get_chi_gio_index(self.hour)
        self.lunar_hour = self._get_lunar_hour(hour)
        
        # Init 12 cung
        self.cung = self._init_cung()
        
    def an_sao(self):
        logger.debug("Starting An Sao algorithm...")
        # 1. An Cung Menh/Than
        menh_index, than_index = self._an_cung_menh_than()
        
        # 2. An Cuc
        cuc_name, cuc_number = self._an_cuc(menh_index)
        
        # 3. An Chinh Tinh
        self._an_chinh_tinh(cuc_number, self.lunar_day)
        
        # 4. An Phu Tinh (Full)
        self._an_phu_tinh_full(cuc_number)
        
        logger.debug("An Sao algorithm finished.")
        
        # Calculate Scores
        scores = []
        star_scores = ConfigManager().get("star_scores")
        for i in range(12):
            score = 0
            # Base Score 5 (Neutral)
            score += 5 
            # Add Stars Score
            for star in self.cung[i]["chinh_tinh"]:
                score += star_scores.get(star, 0)
            for star in self.cung[i]["phu_tinh"]:
                score += star_scores.get(star, 0)
            scores.append(score)

        return {
            "info": {
                "name": self.name,
                "lunar_date": f"{self.lunar_day}/{self.lunar_month}/{self.lunar_year}",
                "can_chi": f"{LunarConverter.get_can_chi_nam(self.lunar_year)}",
                "cuc": cuc_name,
                "menh_tai": DIA_CHI[menh_index],
                "than_tai": DIA_CHI[than_index]
            },
            "cung": self.cung,
            "scores": scores # List of 12 numbers
        }

    def _an_cung_menh_than(self):
        """
        Mệnh: Khởi từ Dần (2), đếm thuận đến tháng sinh, nghịch đến giờ sinh.
        Thân: Khởi từ Dần (2), đếm thuận đến tháng sinh, thuận đến giờ sinh.
        """
        start_index = 2 # Dần
        
        # Tháng sinh (Lưu ý: tháng 1 là 0 bước đi từ mốc? check logic)
        # Logic chuẩn: Từ Dần (tháng 1) đếm thuận đến tháng sinh.
        # Ví dụ tháng 1 -> Dần (2 + 0). Tháng 2 -> Mão (2 + 1).
        month_step = self.lunar_month - 1
        
        # Giờ sinh (Tý = 1, Sửu = 2... trong phép đếm cung?)
        # Logic chuẩn: Từ cung tháng sinh, coi là giờ Tý, đếm Nghịch đến giờ sinh -> Mệnh.
        # Giờ Tý là bước 0.
        hour_step = self.chi_gio 
        
        # Mệnh: Thuận tháng, Nghịch giờ
        menh_pos = (start_index + month_step - hour_step) % 12
        
        # Thân: Thuận tháng, Thuận giờ
        than_pos = (start_index + month_step + hour_step) % 12
        
        self.cung[menh_pos]["chuc_nang"] = "Mệnh"
        self.cung[than_pos]["chuc_nang"] += " (Thân)" # Thân cư Quan/Phu/Tài...
        
        return menh_pos, than_pos

    def _an_cuc(self, menh_index):
        """
        Xác định Cục dựa trên Can của Năm và Vị trí Cung Mệnh.
        """
        can_nam_index = self.can_nam
        
        # Tìm Can của cung Dần để đếm tới cung Mệnh
        # (Giống logic tìm can tháng)
        start_cans = {
            0: 2, 1: 4, 2: 6, 3: 8, 4: 0, # Giáp/Kỷ -> Bính...
            5: 2, 6: 4, 7: 6, 8: 8, 9: 0
        }
        start_can_dan = start_cans[self.can_nam]
        
        # Khoảng cách từ Dần (2) đến Mệnh
        dist_from_dan = (menh_index - 2) % 12
        
        can_menh_index = (start_can_dan + dist_from_dan) % 10
        chi_menh_index = menh_index
        
        # Tra bảng Ngũ Hành Lục Thập Hoa Giáp (Simplified logic for Phase 1)
        # Để chính xác tuyệt đối cần bảng 60 hoa giáp. 
        # Ở đây dùng logic Can Chi -> Ngũ Hành nạp âm -> Cục.
        
        # Mẹo tính Cục nhanh (Thiên Can + Địa Chi)
        # Can: Giáp Ất=1, Bính Đinh=2, Mậu Kỷ=3, Canh Tân=4, Nhâm Quý=5
        val_can = (can_menh_index // 2) + 1
        
        # Chi: Tý Sửu Ngọ Mùi=0, Dần Mão Thân Dậu=1, Thìn Tỵ Tuất Hợi=2
        if chi_menh_index in [0, 1, 6, 7]: val_chi = 0
        elif chi_menh_index in [2, 3, 8, 9]: val_chi = 1
        else: val_chi = 2
        
        total = val_can + val_chi
        if total > 5: total -= 5
        
        # 1=Kim, 2=Thủy, 3=Hỏa, 4=Thổ, 5=Mộc
        cuc_map = {1: ("Kim Tứ Cục", 4), 2: ("Thủy Nhị Cục", 2), 3: ("Hỏa Lục Cục", 6), 4: ("Thổ Ngũ Cục", 5), 5: ("Mộc Tam Cục", 3)}
        
        return cuc_map[total]

    def _an_chinh_tinh(self, cuc_number, day):
        """
        An 14 Chính Tinh dựa trên Tử Vi Tinh Hệ và Thiên Phủ Tinh Hệ.
        """
        # 1. Tìm vị trí Tử Vi
        # Công thức: (Ngày sinh + X) / Cục = Y (dư 0)
        # Nếu dư khác 0 thì xử lý phức tạp hơn
        
        tu_vi_pos = -1
        if day % cuc_number == 0:
            quotient = day // cuc_number
            # Tý = 1, ... Nhưng index list là 0 -> Tý, nên Tý = Dần + (quotient-1)? No.
            # Dần là khởi điểm để đếm cung?
            # Quy tắc: từ cung Dần đếm thuận đến thương số.
            # Dần = 2.
            tu_vi_pos = (2 + (quotient - 1)) % 12
        else:
            quotient = (day // cuc_number) + 1
            remainder = day % cuc_number
            # Quy tắc dư:
            # - Dư lẻ: Thương số + Remainder
            # - Dư chẵn: Thương số - Remainder
            # Logic này khá phức tạp và có nhiều dị bản.
            # Dùng logic phổ thông:
            # X = Cục - Dư
            # Nếu Dư > 0: Cung = (Cung Dần + Thương số) +/- gì đó.
            
            # Simple version for MVP Check: dùng bảng tra hoặc loop tìm.
            # Tạm thời dùng logic chuẩn:
            # Nếu không chia hết: (Ngày + (Cục - số dư)) / Cục = Thương mới.
            # Nếu số dư là lẻ -> lùi lại số dư bước.
            # Nếu số dư là chẵn -> tiến lên số dư bước.
            
            # Re-implement standard logic:
            # B1: Tìm thương số và số dư
            q, r = divmod(day, cuc_number)
            if r == 0:
                base_pos = (2 + (q - 1)) % 12 
            else:
                # Dư khác 0
                q = q + 1 # Thương số làm tròn lên
                base_pos = (2 + (q - 1)) % 12
                # Dư lẻ thì lùi, chẵn thì tiến (tùy phái, ở đây dùng phổ biến: Lẻ thối, Chẵn tiến)
                # Nhưng cần check lại sách. 
                # Sách chuẩn: Ngày sinh chia Cục. 
                # Nếu không hết, mượn Cục số bù vào cho đủ chia?
                # VD: Thủy Nhị Cục (2), ngày 3. 3 chia 2 dư 1.
                # Bù 1 vào 3 -> 4. 4/2 = 2. Cung 2 (Mão - vì Dần là 1).
                # Vì bù 1 (lẻ) -> Lùi 1 cung -> Dần.
                
                fake_day = day + (cuc_number - r)
                new_q = fake_day // cuc_number
                base_pos = (2 + (new_q - 1)) % 12
                
                extra_step = cuc_number - r
                if extra_step % 2 != 0: # Lẻ -> Lùi
                    base_pos = (base_pos - extra_step) % 12
                else: # Chẵn -> Tiến
                    base_pos = (base_pos + extra_step) % 12

            tu_vi_pos = base_pos

        self.cung[tu_vi_pos]["chinh_tinh"].append("Tử Vi")
        
        # 2. An các sao vòng Tử Vi (Ngược chiều kim đồng hồ: Liêm, Thiên, Vũ, Dương, Cơ)
        # Tử Vi (1) -> Liêm Trinh (5) -> Thiên Đồng (8) ... 
        # Thứ tự nghịch: Tử -> Cơ (2) -> ...
        # Vòng Tử Vi: Tử Vi (1), Thiên Cơ (2 - Nghịch), Thái Dương (4 - Nghịch), Vũ Khúc (5 - Nghịch), Thiên Đồng (6 - Nghịch), Liêm Trinh (9 - Nghịch)
        # Note: đếm là đếm cung. 
        # Cung Tử Vi gọi là 1.
        self.cung[(tu_vi_pos - 1) % 12]["chinh_tinh"].append("Thiên Cơ")
        self.cung[(tu_vi_pos - 3) % 12]["chinh_tinh"].append("Thái Dương")
        self.cung[(tu_vi_pos - 4) % 12]["chinh_tinh"].append("Vũ Khúc")
        self.cung[(tu_vi_pos - 5) % 12]["chinh_tinh"].append("Thiên Đồng")
        self.cung[(tu_vi_pos - 8) % 12]["chinh_tinh"].append("Liêm Trinh") # Liêm trinh cách Tử Vi 8 cung nghịch?
        # Check lại:
        # Tử, Cơ, (bỏ 1), Dương, Vũ, Đồng, (bỏ 2), Liêm.
        # Nghịch chiều kim đồng hồ.
        
        # 3. An Thiên Phủ
        # Quy tắc: Dần Thân đối nhau qua trục Sửu Mùi? 
        # Không, Tử Vi và Thiên Phủ đối xứng nhau qua trục Dần - Thân.
        # Tổng số cung = 4 (Dần = 2, Thân = 8? 2+8=10? No)
        # Công thức: Thiên Phủ pos = (12 - Tử Vi pos) + 2. (Nếu tính Tý = 0. Dần = 2)
        # Check: Tử Vi ở Ngọ (6). Phủ ở đâu? Đối qua trục Dần (2) - Thân (8).
        # Cung 2 và 8 là trục. Cung 0 (Tý) - Cung 4 (Thìn)? Không phải.
        # Công thức chuẩn (Index 0-11):
        # Thiên Phủ index = (4 - tu_vi_pos) % 12. 
        # Ví dụ: Tử Vi ở Tý (0). Phủ = 4 (Thìn). Sai. Tử Vi cư Tý thì Thiên Phủ cư Thìn. Đúng.
        # Ví dụ: Tử Vi ở Ngọ (6). Phủ = (4 - 6) % 12 = -2 % 12 = 10 (Tuất). Sai. Tử Vi cư Ngọ Thiên Phủ cư Tuất. Đúng.
        # Ví dụ: Tử Vi ở Dần (2). Phủ = (4 - 2) = 2. Đồng cung.
        # Ví dụ: Tử Vi ở Thân (8). Phủ = (4 - 8) = -4 = 8. Đồng cung.
        
        thien_fu_pos = (4 - tu_vi_pos) % 12
        self.cung[thien_fu_pos]["chinh_tinh"].append("Thiên Phủ")
        
        # 4. An vòng Thiên Phủ (Thuận chiều kim đồng hồ)
        # Phủ -> Thái Âm (2) -> Tham Lang (3) -> Cự Môn (4) -> Thiên Tướng (5) -> Thiên Lương (6) -> Thất Sát (7) -> Phá Quân (11)
        # Phủ (1), Thái Âm (2), Tham Lang (3), Cự Môn (4), Thiên Tướng (5), Thiên Lương (6), Thất Sát (7), Phá Quân (11)
        
        self.cung[(thien_fu_pos + 1) % 12]["chinh_tinh"].append("Thái Âm")
        self.cung[(thien_fu_pos + 2) % 12]["chinh_tinh"].append("Tham Lang")
        self.cung[(thien_fu_pos + 3) % 12]["chinh_tinh"].append("Cự Môn")
        self.cung[(thien_fu_pos + 4) % 12]["chinh_tinh"].append("Thiên Tướng")
        self.cung[(thien_fu_pos + 5) % 12]["chinh_tinh"].append("Thiên Lương")
        self.cung[(thien_fu_pos + 6) % 12]["chinh_tinh"].append("Thất Sát")
        self.cung[(thien_fu_pos + 10) % 12]["chinh_tinh"].append("Phá Quân") # Cách 3 cung

    def _get_lunar_hour(self, hour):
        """
        Convert solar hour (0-23) to Lunar Hour Index (Tý=0, Sửu=1...)
        Tý: 23h-1h
        Sửu: 1h-3h
        ...
        """
        # Shift hour to align Tý (23-1) -> 0
        # If hour = 23 -> (23+1)//2 = 12%12 = 0
        # If hour = 0 -> (0+1)//2 = 0
        # If hour = 1 -> (1+1)//2 = 1 -> Sửu (Wait, 1h00 is middle of Sửu start? No. 1h-3h is Sửu.)
        # Tý: 23:00 - 00:59.
        # Sửu: 01:00 - 02:59.
        # Let's check formula: (hour + 1) // 2 % 12
        # 0h (Tý) -> (0+1)//2 = 0. Correct.
        # 1h (Sửu start) -> (1+1)//2 = 1. Correct.
        # 22h (Hợi end) -> (22+1)//2 = 11. Correct.
        # 23h (Tý start) -> (23+1)//2 = 12 -> 0. Correct.
        return (hour + 1) // 2 % 12

    def _init_cung(self):
        return {i: {"name": DIA_CHI[i], "chinh_tinh": [], "phu_tinh": [], "chuc_nang": ""} for i in range(12)}

    def _an_phu_tinh(self):
        """
        An các phụ tinh (Khôi Việt, Xương Khúc, Tả Hữu, Lộc Tồn, Kình Đà...)
        """
        from core.constants import (
            VONG_THAI_TUE, VONG_BAC_SY, VONG_TRANG_SINH, TRANG_SINH_START,
            KHOI_VIET_POS, LOC_TON_MAP, DIA_CHI, CUNG_DIA_BAN
        )
        
        # --- 1. Vòng Thái Tuế (Theo Chi Năm - Luôn Thuận) ---
        start_thai_tue = self.chi_nam
        for i, star in enumerate(VONG_THAI_TUE):
            pos = (start_thai_tue + i) % 12
            self.cung[pos]["phu_tinh"].append(star)

        # --- 2. Vòng Lộc Tồn (Theo Can Năm) ---
        # Bác Sỹ an tại Lộc Tồn
        can_nam_str = LunarConverter.get_can_nam(self.lunar_year)
        if can_nam_str not in LOC_TON_MAP:
             # Should not happen if data is correct
             loc_ton_chi = "Dần" # Fallback
        else:
            loc_ton_chi = LOC_TON_MAP[can_nam_str]
            
        loc_ton_index = DIA_CHI.index(loc_ton_chi)

        # An chính sao Lộc Tồn
        self.cung[loc_ton_index]["phu_tinh"].append("Lộc Tồn")
        
        # An Kình Dương (Tiền Kình - Trước Lộc Tồn 1 cung - Thuận)
        kinh_duong_pos = (loc_ton_index + 1) % 12
        self.cung[kinh_duong_pos]["phu_tinh"].append("Kình Dương")
        
        # An Đà La (Hậu Đà - Sau Lộc Tồn 1 cung - Nghịch)
        da_la_pos = (loc_ton_index - 1) % 12
        self.cung[da_la_pos]["phu_tinh"].append("Đà La")

        # An Vòng Bác Sỹ (Bác Sỹ tại cung Lộc Tồn)
        # Chiều: Dương Nam/Âm Nữ -> Thuận. Âm Nam/Dương Nữ -> Nghịch.
        # Check Âm Dương của Can Năm sinh? Không, Âm Dương của Tuổi (Can + Chi).
        # TuViLogic.init đã tính am_duong_nam_nu chưa? Chưa explicit.
        # Convention: input gender (1 Nam, 0 Nữ). 
        # Cần xác định Can Chi năm sinh là Dương hay Âm.
        # Giáp, Bính, Mậu, Canh, Nhâm -> Dương
        # Ất, Đinh, Kỷ, Tân, Quý -> Âm
        can_index = self.can_nam # 0=Giáp (Dương), 1=Ất (Âm)...
        is_yang_year = (can_index % 2 == 0)
        
        # Nam (1): Dương (is_yang) -> Dương Nam. Âm -> Âm Nam.
        # Nữ (0): Dương -> Dương Nữ (Nghịch). Âm -> Âm Nữ (Thuận). -- Wait convention.
        # Dương Nam / Âm Nữ: Thuận.
        # Âm Nam / Dương Nữ: Nghịch. 
        
        is_thuan = False
        if self.gender == 1: # Nam
            if is_yang_year: is_thuan = True # Dương Nam -> Thuận
            else: is_thuan = False # Âm Nam -> Nghịch
        else: # Nữ
            if not is_yang_year: is_thuan = True # Âm Nữ -> Thuận
            else: is_thuan = False # Dương Nữ -> Nghịch
            
        for i, star in enumerate(VONG_BAC_SY):
            if is_thuan:
                pos = (loc_ton_index + i) % 12
            else:
                pos = (loc_ton_index - i) % 12
            self.cung[pos]["phu_tinh"].append(star)

        # --- 3. Vòng Tràng Sinh (Theo Cục) ---
        # Khởi Tràng Sinh tại TRANG_SINH_START[cuc_number]
        # Bắt cục:
        # cuc_number lấy từ _an_cuc return. Nhưng số Cục đã truyền vào _an_chinh_tinh, chưa lưu property.
        # Recalculate or use saved? Better save property in step 2.
        # Hotfix: Recalculate cuc_number from saved cuc name/number logic is tricky. 
        # Re-call _an_cuc? No, _an_cuc uses menh_index.
        # Let's verify if we can access cuc_number.
        # In an_sao(), we have `cuc_name, cuc_number = self._an_cuc(menh_index)`.
        # Pass cuc_number to _an_phu_tinh.
        
        # Update method signature later. For now, hack re-calc simple or pass as arg.
        # Plan: I will modify `an_sao` to pass `cuc_number`. For now, use `self.cuc_number` if I set it, 
        # or re-call `_an_cuc`. But `_an_cuc` needs `menh_index`.
        # Best: Modify `an_sao` to save `self.cuc_number`. 
        pass 
        # (Wait for signature update in `an_sao`)

    def _an_phu_tinh_full(self, cuc_number):
        # Implementation moved here to accept cuc_number
        from core.constants import (
            VONG_THAI_TUE, VONG_BAC_SY, VONG_TRANG_SINH, TRANG_SINH_START,
            KHOI_VIET_POS, LOC_TON_MAP, DIA_CHI
        )
        
        # --- 0. Setup Params ---
        can_nam_idx = self.can_nam
        chi_nam_idx = self.chi_nam
        hour_idx = self.chi_gio
        month = self.lunar_month # 1-12
        day = self.lunar_day
        
        # Nam (1): Can Dương -> Dương Nam (Thuận). Can Âm -> Âm Nam (Nghịch).
        # Nữ (0): Can Dương -> Dương Nữ (Nghịch). Can Âm -> Âm Nữ (Thuận).
        is_yang_year = (can_nam_idx % 2 == 0)
        if self.gender == 1:
            is_thuan = is_yang_year
        else:
            is_thuan = not is_yang_year
            
        # --- 1. Vòng Thái Tuế (Luôn Thuận từ Chi Năm) ---
        for i, star in enumerate(VONG_THAI_TUE):
            pos = (chi_nam_idx + i) % 12
            self.cung[pos]["phu_tinh"].append(star)
            
        # --- 2. Vòng Lộc Tồn ---
        can_nam_str = THIEN_CAN[can_nam_idx]
        loc_ton_chi = LOC_TON_MAP.get(can_nam_str, "Dần")
        loc_ton_idx = DIA_CHI.index(loc_ton_chi)
        
        self.cung[loc_ton_idx]["phu_tinh"].append("Lộc Tồn")
        self.cung[(loc_ton_idx + 1)%12]["phu_tinh"].append("Kình Dương") # Thuận 1
        self.cung[(loc_ton_idx - 1)%12]["phu_tinh"].append("Đà La")     # Nghịch 1
        
        for i, star in enumerate(VONG_BAC_SY):
            # Bác Sỹ đồng cung Lộc Tồn
            if has_bac_sy := True: 
                # Skip Bác Sỹ text if wanted, but standard shows both.
                pass
            
            if is_thuan: pos = (loc_ton_idx + i) % 12
            else: pos = (loc_ton_idx - i) % 12
            
            # Avoid duplicate Lộc Tồn (Bác Sỹ is separate star)
            self.cung[pos]["phu_tinh"].append(star)
            
        # --- 3. Vòng Tràng Sinh (Theo Cục) ---
        ts_start = TRANG_SINH_START.get(cuc_number, 2) # Default Dần?
        for i, star in enumerate(VONG_TRANG_SINH):
            if is_thuan: pos = (ts_start + i) % 12
            else: pos = (ts_start - i) % 12
            self.cung[pos]["phu_tinh"].append(star)
            
        # --- 4. Sao Lẻ Quan Trọng ---
        
        # Tả Phù (Thìn thuận đến tháng), Hữu Bật (Tuất nghịch đến tháng)
        # Tháng 1 tại cung khởi. -> pos = start + (month - 1) * dir
        ta_phu_pos = (4 + (month - 1)) % 12 # Thìn = 4
        huu_bat_pos = (10 - (month - 1)) % 12 # Tuất = 10
        self.cung[ta_phu_pos]["phu_tinh"].append("Tả Phù")
        self.cung[huu_bat_pos]["phu_tinh"].append("Hữu Bật")
        
        # Văn Xương (Tuất nghịch đến giờ), Văn Khúc (Thìn thuận đến giờ)
        # Giờ Tý (idx 0) tại cung khởi.
        van_xuong_pos = (10 - hour_idx) % 12
        van_khuc_pos = (4 + hour_idx) % 12
        self.cung[van_xuong_pos]["phu_tinh"].append("Văn Xương")
        self.cung[van_khuc_pos]["phu_tinh"].append("Văn Khúc")
        
        # Thiên Khôi, Thiên Việt (Theo Can Năm)
        if can_nam_str in KHOI_VIET_POS:
            k_pos, v_pos = KHOI_VIET_POS[can_nam_str]
            self.cung[k_pos]["phu_tinh"].append("Thiên Khôi")
            self.cung[v_pos]["phu_tinh"].append("Thiên Việt")
            
        # Thiên Mã (Theo Chi Năm - Tam Hợp Cục)
        # Dần Ngọ Tuất -> Thân (Mã tại đối cung của Chi đầu tam hợp?) -> Mã tại Thân.
        # Thân Tý Thìn -> Dần.
        # Tỵ Dậu Sửu -> Hợi.
        # Hợi Mão Mùi -> Tỵ.
        # Mapping: 
        tam_hop_ma = {
            2: 8, 6: 8, 10: 8, # Dần Ngọ Tuất -> Thân (8)
            8: 2, 0: 2, 4: 2,  # Thân Tý Thìn -> Dần (2)
            5: 11, 9: 11, 1: 11, # Tỵ Dậu Sửu -> Hợi (11)
            11: 5, 3: 5, 7: 5   # Hợi Mão Mùi -> Tỵ (5)
        }
        ma_pos = tam_hop_ma.get(chi_nam_idx, 2)
        self.cung[ma_pos]["phu_tinh"].append("Thiên Mã")
        
        # Thiên Khốc, Thiên Hư (Ngọ nghịch đến năm)
        # Ngọ (6). Tý (0 bước). 
        # Khốc: Ngọ nghịch. (6 - chi_nam)
        # Hư: Ngọ thuận. (6 + chi_nam)
        khoc_pos = (6 - chi_nam_idx) % 12
        hu_pos = (6 + chi_nam_idx) % 12
        self.cung[khoc_pos]["phu_tinh"].append("Thiên Khốc")
        self.cung[hu_pos]["phu_tinh"].append("Thiên Hư")
        
        # Địa Không, Địa Kiếp (Hợi thuận/nghịch giờ)
        # Hợi (11). Giờ Tý (0) tại Hợi.
        # Kiếp: Thuận. Không: Nghịch.
        dia_kiep_pos = (11 + hour_idx) % 12
        dia_khong_pos = (11 - hour_idx) % 12
        self.cung[dia_kiep_pos]["phu_tinh"].append("Địa Kiếp")
        self.cung[dia_khong_pos]["phu_tinh"].append("Địa Không")

        # Hỏa Tinh, Linh Tinh (Phức tạp - Tạm bỏ qua hoặc an theo Giờ)

