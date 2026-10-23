import unittest

from code_sample.location import NormalizedLocation, normalize_location


class LocationNormalizationTests(unittest.TestCase):
    def test_german_city_variants(self) -> None:
        cases = {
            "Bremen": "Bremen",
            "München": "Munich",
            "Muenchen, DE": "Munich",
            "Köln": "Cologne",
            "Hanover": "Hannover",
        }

        for raw, city in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(
                    normalize_location(raw),
                    NormalizedLocation("Germany", city, False, "high"),
                )

    def test_remote_germany_is_explicit(self) -> None:
        for raw in ("Remote - Germany", "Deutschlandweit", "Homeoffice Germany"):
            with self.subTest(raw=raw):
                result = normalize_location(raw)
                self.assertEqual(result.country, "Germany")
                self.assertTrue(result.is_remote)
                self.assertEqual(result.confidence, "high")

    def test_ambiguous_remote_location_stays_unknown(self) -> None:
        result = normalize_location("EMEA Remote")

        self.assertIsNone(result.country)
        self.assertTrue(result.is_remote)
        self.assertFalse(result.is_clearly_outside_germany)

    def test_non_german_dach_location_is_not_misclassified(self) -> None:
        for raw, country in (
            ("Wien, Österreich", "Austria"),
            ("Zürich, Switzerland", "Switzerland"),
        ):
            with self.subTest(raw=raw):
                result = normalize_location(raw)
                self.assertEqual(result.country, country)
                self.assertTrue(result.is_clearly_outside_germany)

    def test_short_country_code_does_not_match_inside_a_country_name(self) -> None:
        result = normalize_location("Kyiv, Ukraine")

        self.assertIsNone(result.country)
        self.assertFalse(result.is_clearly_outside_germany)


if __name__ == "__main__":
    unittest.main()
