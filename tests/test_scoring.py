import unittest
from core.tuvi import TuViLogic
from core.constants import STAR_SCORES

class TestScoringLogic(unittest.TestCase):
    def test_scores_structure(self):
        # Setup data
        tv = TuViLogic(15, 1, 2024, 12, 1, "Test User")
        result = tv.an_sao()
        
        # Check scores existence
        self.assertIn("scores", result)
        self.assertEqual(len(result["scores"]), 12)
        
    def test_score_calculation(self):
        # Mock logic or verify logic for a specific case
        # Case: Tu Vi (10) + Thien Phu (10) in one house (impossible usually, but check sums)
        # Let's check if scores are not all 5 (Base score)
        
        tv = TuViLogic(10, 2, 2024, 10, 1, "Test Scoring")
        result = tv.an_sao()
        scores = result["scores"]
        
        # Ensure variations exist (not all neutral)
        self.assertTrue(any(s != 5 for s in scores), "Scores should vary based on stars")
        
        # Debug print for manual verification if needed
        # for i, s in enumerate(scores):
        #     print(f"Cung {i}: {s}")

if __name__ == '__main__':
    unittest.main()
