import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import growth_scorecard as gs


def all_factors(rating):
    return {k: rating for k in gs.WEIGHTS}


class TestWeights(unittest.TestCase):
    def test_weights_sum_to_100(self):
        self.assertEqual(sum(gs.WEIGHTS.values()), 100)

    def test_quality_entry_split(self):
        self.assertEqual(sum(gs.QUALITY_WEIGHTS.values()), 80)
        self.assertEqual(sum(gs.ENTRY_WEIGHTS.values()), 20)


class TestScoring(unittest.TestCase):
    def test_perfect_score(self):
        r = gs.score({"factors": all_factors(5)})
        self.assertEqual(r["final_score"], 100.0)
        self.assertEqual(r["quality_score"], 100.0)
        self.assertEqual(r["entry_score"], 100.0)
        self.assertEqual(r["verdict"], "强信心值得投资")
        self.assertFalse(r["capped_by_red_line"])

    def test_zero_score(self):
        r = gs.score({"factors": all_factors(0)})
        self.assertEqual(r["final_score"], 0.0)
        self.assertEqual(r["verdict"], "暂不值得 / 回避")

    def test_penalty_reduces_score(self):
        r = gs.score({"factors": all_factors(5),
                      "penalties": {"dilution_financing": 5}})
        # raw 100 - (5 * 2.0) = 90
        self.assertEqual(r["final_score"], 90.0)
        self.assertEqual(r["verdict"], "强信心值得投资")

    def test_dual_axis_good_company_expensive(self):
        # quality factors maxed, entry factors zero -> great biz, bad price
        factors = {k: (5 if k in gs.QUALITY_WEIGHTS else 0) for k in gs.WEIGHTS}
        r = gs.score({"factors": factors})
        self.assertEqual(r["quality_score"], 100.0)
        self.assertEqual(r["entry_score"], 0.0)
        self.assertEqual(r["final_score"], 80.0)  # raw quality points = 80
        self.assertEqual(r["verdict"], "值得投资")

    def test_red_line_caps_high_score(self):
        r = gs.score({"factors": all_factors(5),
                      "red_lines": {"accounting_fraud_suspicion": True}})
        self.assertTrue(r["capped_by_red_line"])
        self.assertEqual(r["verdict"], gs.CAPPED_VERDICT)
        self.assertIn("accounting_fraud_suspicion", r["triggered_red_lines"])

    def test_invalid_rating_raises(self):
        with self.assertRaises(ValueError):
            gs.score({"factors": {"revenue_growth_durability": 6}})


if __name__ == "__main__":
    unittest.main(verbosity=2)
