import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_docs_test_toml_versions_match_active_versions():
    """Verify that .docs-test.toml [versioning].versions matches versions.json.

    The Playwright testing harness in solo-io/docs-theme-extras relies on
    .docs-test.toml to determine which version trees to scan. If an active
    version is missing from .docs-test.toml, its documentation is silently
    skipped by CI framework testing.
    """
    versions_json_path = REPO_ROOT / "versions.json"
    assert versions_json_path.exists(), "versions.json does not exist"
    active_versions = json.loads(versions_json_path.read_text(encoding="utf-8"))
    expected_link_versions = [v["linkVersion"] for v in active_versions]

    docs_test_path = REPO_ROOT / ".docs-test.toml"
    assert docs_test_path.exists(), ".docs-test.toml does not exist"
    content = docs_test_path.read_text(encoding="utf-8")

    match = re.search(r"\[versioning\][\s\S]*?versions\s*=\s*\[(.*?)\]", content)
    assert match, "Could not find [versioning].versions in .docs-test.toml"

    actual_versions = [
        s.strip().strip('"\'')
        for s in match.group(1).split(",")
        if s.strip()
    ]

    assert actual_versions == expected_link_versions, (
        f".docs-test.toml [versioning].versions does not match active versions in versions.json.\n"
        f"Configured: {actual_versions}\n"
        f"Expected:   {expected_link_versions}\n"
        f"Missing:    {[v for v in expected_link_versions if v not in actual_versions]}\n"
        f"Obsolete:   {[v for v in actual_versions if v not in expected_link_versions]}"
    )
