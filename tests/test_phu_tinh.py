import unittest
from core.tuvi import TuViLogic
from core.constants import DIA_CHI

class TestPhuTinhLogic(unittest.TestCase):
    def setUp(self):
        # Case: 05/03/1992 (Duong) -> 02/02/1992 (Am) - Nhâm Thân
        # Gio: 9:06 (Tỵ)
        # Gender: Nam (1)
        # Expected:
        # - Mệnh: Tuất
        # - Cục: Kim Tứ Cục
        self.tv = TuViLogic(5, 3, 1992, 9, 1, "Nguyen Duy Truong")
        self.data = self.tv.an_sao()
        self.cung = self.data["cung"]

    def find_star(self, star_name):
        """Helper to find which cung (index) contains the star"""
        for i in range(12):
            if star_name in self.cung[i]["phu_tinh"]:
                return i, self.cung[i]["name"]
        return -1, None

    def test_vong_thai_tue(self):
        # Năm Thân -> Thái Tuế an tại Thân (8)
        # Các sao: Thái Tuế, Thiếu Dương, Tang Môn...
        idx, name = self.find_star("Thái Tuế")
        self.assertEqual(name, "Thân", "Thái Tuế phải an tại cung Chi năm sinh (Thân)")
        
        idx, name = self.find_star("Tang Môn")
        # Tang Môn cách Thái Tuế 2 cung thuận -> Thân(8) + 2 = Tuất(10)
        self.assertEqual(name, "Tuất", "Tang Môn phải cách Thái Tuế 2 cung")

    def test_vong_loc_ton(self):
        # Can Nhâm -> Lộc Tồn tại Hợi
        idx, name = self.find_star("Lộc Tồn")
        self.assertEqual(name, "Hợi", "Can Nhâm -> Lộc Tồn tại Hợi")
        
        # Kình Dương: Thuận 1 -> Tý
        idx, name = self.find_star("Kình Dương")
        self.assertEqual(name, "Tý", "Kình Dương phải ở trước Lộc Tồn")
        
        # Đà La: Nghịch 1 -> Tuất
        idx, name = self.find_star("Đà La")
        self.assertEqual(name, "Tuất", "Đà La phải ở sau Lộc Tồn")

    def test_vong_trang_sinh(self):
        # Cục: Kim Tứ Cục (4)
        # Kim -> Tràng Sinh tại Tỵ (5)
        # Nam (1), Dương Năm (Nhâm - Dương) -> Thuận
        idx, name = self.find_star("Tràng Sinh")
        self.assertEqual(name, "Tỵ", "Kim Tứ Cục -> Tràng Sinh tại Tỵ")
        
        idx, name = self.find_star("Đế Vượng")
        # Tràng Sinh (1) -> Mộc Dục (2) -> Quan Đới (3) -> Lâm Quan (4) -> Đế Vượng (5)
        # Tỵ -> Ngọ -> Mùi -> Thân -> Dậu
        self.assertEqual(name, "Dậu", "Đế Vượng phải tại Dậu")

    def test_khoi_viet(self):
        # Can Nhâm -> Khôi tại Tỵ, Việt tại Mão (Theo KHOI_VIET_POS trong Constants)
        # Check Constants: "Nhâm": (5, 3) -> Tỵ, Mão
        idx, name = self.find_star("Thiên Khôi")
        self.assertEqual(name, "Tỵ", "Can Nhâm -> Thiên Khôi tại Tỵ")
        
        idx, name = self.find_star("Thiên Việt")
        self.assertEqual(name, "Mão", "Can Nhâm -> Thiên Việt tại Mão")

    def test_ta_huu(self):
        # Tháng 2
        # Tả Phù: Thìn (4) + (2-1) = Tỵ (5)
        # Hữu Bật: Tuất (10) - (2-1) = Dậu (9)
        idx, name = self.find_star("Tả Phù")
        self.assertEqual(name, "Tỵ", "Tháng 2 -> Tả Phù tại Tỵ")
        
        idx, name = self.find_star("Hữu Bật")
        self.assertEqual(name, "Dậu", "Tháng 2 -> Hữu Bật tại Dậu")

if __name__ == '__main__':
    unittest.main()
