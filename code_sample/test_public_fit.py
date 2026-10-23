import unittest
from dataclasses import replace

from code_sample.public_fit import InternalFitAssessment, to_public_payload


class PublicFitPayloadTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assessment = InternalFitAssessment(
            tier="reachable_reach",
            explanation="A close match with one explicit infrastructure gap.",
            matched=("Python", "PostgreSQL", "Python"),
            gaps=("Kubernetes", "Terraform", "Kubernetes"),
            language="English",
            similarity=0.82,
            ranking_weight=0.94,
            seniority_label="stretch",
        )

    def test_public_payload_matches_the_documented_contract(self) -> None:
        payload = to_public_payload(self.assessment).as_dict()

        self.assertEqual(
            set(payload),
            {"tier", "explanation", "matched", "gap", "gaps", "language"},
        )
        self.assertEqual(payload["matched"], ["Python", "PostgreSQL"])
        self.assertEqual(payload["gap"], "Kubernetes")
        self.assertEqual(payload["gaps"], ["Kubernetes", "Terraform"])

    def test_internal_ranking_fields_do_not_cross_the_boundary(self) -> None:
        serialized = repr(to_public_payload(self.assessment).as_dict())

        self.assertNotIn("0.82", serialized)
        self.assertNotIn("0.94", serialized)
        self.assertNotIn("stretch", serialized)

    def test_empty_explanation_is_rejected(self) -> None:
        assessment = replace(self.assessment, explanation="  ")

        with self.assertRaisesRegex(ValueError, "needs an explanation"):
            to_public_payload(assessment)


if __name__ == "__main__":
    unittest.main()
