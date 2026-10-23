from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def load_json(relative_path: str) -> dict:
    path = ROOT / relative_path
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def verify_json_artifacts() -> None:
    json_paths = sorted(ARTIFACTS.rglob("*.json"))
    assert len(json_paths) == 6, f"expected 6 JSON artifacts, found {len(json_paths)}"
    for path in json_paths:
        with path.open(encoding="utf-8") as handle:
            json.load(handle)


def verify_ingestion() -> None:
    snapshot = load_json("artifacts/ingestion/snapshot.json")
    assert snapshot["jobs"] == 1943
    assert snapshot["companies"] == 527
    assert snapshot["configured_sources"] == 49
    assert len(snapshot["adapter_types"]) == 8
    assert len(set(snapshot["adapter_types"])) == 8


def verify_migration() -> None:
    migration = load_json("artifacts/migration/verification.json")
    computed_total = sum(migration["rows_by_table"].values())
    assert computed_total == migration["stated_total_rows"], (
        f"migration total mismatch: {computed_total} != "
        f"{migration['stated_total_rows']}"
    )
    assert migration["checks"]["per_table_row_count_parity"] is True
    assert migration["checks"]["row_level_security_isolation"] == "pass"


def verify_evaluation() -> None:
    scorecard = load_json("artifacts/evaluation/pack-ready-scorecard.json")
    harness = scorecard["harness"]
    readiness = scorecard["readiness_analysis"]
    scores = scorecard["pack_ready_average_scores_out_of_5"]

    assert harness["synthetic_profiles"] == 4
    assert len(harness["role_families"]) == 5
    assert set(harness["fit_strengths"]) == {"strong", "stretch", "weak"}
    assert readiness["pack_ready_cells"] + readiness["visible_not_pack_ready_cells"] == readiness[
        "visible_cells_reviewed"
    ]
    assert readiness["cells_passing_all_material_bars"] <= readiness["pack_ready_cells"]
    expected_rate = round(
        readiness["cells_passing_all_material_bars"] / readiness["pack_ready_cells"], 4
    )
    assert expected_rate == readiness["pass_rate_on_pack_ready_cells"]
    assert all(0 <= score <= 5 for score in scores.values())

    sentinel = load_json("artifacts/evaluation/regression-sentinel.json")
    assert sentinel["fixture_pairs"] * len(sentinel["material_types"]) == sentinel[
        "files_compared"
    ]
    assert sentinel["result"] == "pass"


def verify_security() -> None:
    review = load_json("artifacts/security/security-review.json")
    severities = {finding["severity"] for finding in review["fixed_findings"]}
    assert severities == {"critical", "high", "medium"}
    assert all(result == "pass" for result in review["verification"].values())


def verify_contract() -> None:
    schema = load_json("artifacts/contracts/public-fit-payload.schema.json")
    required = {"tier", "explanation", "matched", "gap", "gaps", "language"}
    assert set(schema["required"]) == required
    assert set(schema["properties"]) == required
    assert "score" not in schema["properties"]
    assert "weights" not in schema["properties"]


def verify_markdown() -> None:
    markdown_paths = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
    for path in markdown_paths:
        text = path.read_text(encoding="utf-8")
        assert text.count(chr(96) * 3) % 2 == 0, f"unbalanced code fence in {path}"
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative_target = target.split("#", 1)[0]
            if not relative_target:
                continue
            resolved = (path.parent / relative_target).resolve()
            assert resolved.exists(), f"broken link in {path}: {target}"


def main() -> None:
    verify_json_artifacts()
    verify_ingestion()
    verify_migration()
    verify_evaluation()
    verify_security()
    verify_contract()
    verify_markdown()
    print("Public evidence checks passed.")


if __name__ == "__main__":
    main()
