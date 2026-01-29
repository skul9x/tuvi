import unittest
from core.tuvi import TuViLogic
from core.lunar import LunarConverter

class TestTuViLogic(unittest.TestCase):
    def test_lunar_conversion(self):
        # 10/2/2024 Solar -> 1/1/2024 Lunar (Giáp Thìn)
        d, m, y, leap = LunarConverter.convert_solar_to_lunar(10, 2, 2024)
        self.assertEqual(d, 1)
        self.assertEqual(m, 1)
        self.assertEqual(y, 2024)
        
    def test_an_sao_basic(self):
        # Test case: Sinh 15/1/2024 Dương. Giờ Ngọ (12h). Nam.
        # Âm: 5/12/2023 (Quý Mão). (Tháng 12 thiếu).
        # Check online (tuvivietnam.vn or others) to verify expected stars.
        
        # Để đơn giản, test logic chạy không crash và ra kết quả có cấu trúc đúng.
        tv = TuViLogic(15, 1, 2024, 12, 1, "Test User")
        result = tv.an_sao()
        
        # Check info
        self.assertIn("Quý Mão", result["info"]["can_chi"])
        
        # Check 14 chinh tinh duoc an
        count_chinh_tinh = 0
        all_stars = []
        for i in range(12):
            stars = result["cung"][i]["chinh_tinh"]
            count_chinh_tinh += len(stars)
            all_stars.extend(stars)
            
        self.assertEqual(count_chinh_tinh, 14) 
        self.assertIn("Tử Vi", all_stars)
        self.assertIn("Phá Quân", all_stars)

if __name__ == '__main__':
    unittest.main()
