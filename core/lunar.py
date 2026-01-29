from lunardate import LunarDate
from core.constants import THIEN_CAN, DIA_CHI

class LunarConverter:
    @staticmethod
    def convert_solar_to_lunar(day, month, year):
        """Convert Solar date to Lunar date (day, month, year, leap)."""
        try:
            lunar_date = LunarDate.fromSolarDate(year, month, day)
            return lunar_date.day, lunar_date.month, lunar_date.year, lunar_date.isLeapMonth
        except Exception as e:
            # lunardate library limits (usually < 1900)
            if year < 1900:
                raise ValueError(f"Năm sinh {year} quá xa xưa, thư viện chưa hỗ trợ (Sau 1900).")
            raise ValueError(f"Ngày sinh không hợp lệ: {day}/{month}/{year}")

    @staticmethod
    def get_can_chi_nam(year: int) -> str:
        can = THIEN_CAN[(year - 4) % 10]
        chi = DIA_CHI[(year - 4) % 12]
        return f"{can} {chi}"
    
    @staticmethod
    def get_chi_nam_index(year: int) -> int:
        return (year - 4) % 12

    @staticmethod
    def get_can_nam_index(year: int) -> int:
        return (year - 4) % 10

    @staticmethod
    def get_can_chi_thang(lunar_month: int, year_can_index: int) -> str:
        # Công thức tính Can tháng:
        # Giáp, Kỷ -> Bính Dần (Tháng 1 là Bính)
        # Ất, Canh -> Mậu Dần
        # Bính, Tân -> Canh Dần
        # Đinh, Nhâm -> Nhâm Dần
        # Mậu, Quý -> Giáp Dần
        start_cans = {
            0: 2, # Giáp -> Bính
            1: 4, # Ất -> Mậu
            2: 6, # Bính -> Canh
            3: 8, # Đinh -> Nhâm
            4: 0, # Mậu -> Giáp
            5: 2, # Kỷ -> Bính
            6: 4, # Canh -> Mậu
            7: 6, # Tân -> Canh
            8: 8, # Nhâm -> Nhâm
            9: 0  # Quý -> Giáp
        }
        
        start_can = start_cans[year_can_index]
        current_can_index = (start_can + (lunar_month - 1)) % 10
        current_chi_index = (2 + (lunar_month - 1)) % 12 # Tháng 1 luôn là Dần (index 2)
        
        return f"{THIEN_CAN[current_can_index]} {DIA_CHI[current_chi_index]}"

    @staticmethod
    def get_chi_gio(hour: int) -> str:
        # 23-1: Tý, 1-3: Sửu...
        if hour >= 23 or hour < 1:
            return "Tý"
        elif 1 <= hour < 3:
            return "Sửu"
        elif 3 <= hour < 5:
            return "Dần"
        elif 5 <= hour < 7:
            return "Mão"
        elif 7 <= hour < 9:
            return "Thìn"
        elif 9 <= hour < 11:
            return "Tỵ"
        elif 11 <= hour < 13:
            return "Ngọ"
        elif 13 <= hour < 15:
            return "Mùi"
        elif 15 <= hour < 17:
            return "Thân"
        elif 17 <= hour < 19:
            return "Dậu"
        elif 19 <= hour < 21:
            return "Tuất"
        else: # 21-23
            return "Hợi"
            
    @staticmethod
    def get_chi_gio_index(hour: int) -> int:
        # Tý = 0, Sửu = 1...
        if hour >= 23 or hour < 1: return 0
        if 1 <= hour < 3: return 1
        if 3 <= hour < 5: return 2
        if 5 <= hour < 7: return 3
        if 7 <= hour < 9: return 4
        if 9 <= hour < 11: return 5
        if 11 <= hour < 13: return 6
        if 13 <= hour < 15: return 7
        if 15 <= hour < 17: return 8
        if 17 <= hour < 19: return 9
        if 19 <= hour < 21: return 10
        return 11
