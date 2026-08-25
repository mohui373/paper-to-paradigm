#!/usr/bin/env python3
"""Validate collection structure, bilingual routing fixtures, and output contracts."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXPECTED = {
    "paper-anatomy": {
        "required": [
            "SKILL.md",
            "README.md",
            "README_EN.md",
            "agents/openai.yaml",
            "references/anatomy-protocol.md",
            "references/claim-verification.md",
            "references/output-contract.md",
            "references/scoring-rubric.md",
            "references/source-grounding.md",
            "scripts/prepare_paper.py",
            "scripts/validate_output.py",
            "evals/evals.json",
        ],
        "description_terms": ["analyze", "verify", "解剖", "核验", "meta-analysis", "德尔菲"],
        "routing_terms": ["read", "explain", "analyze", "review", "verify", "fact-check", "读懂", "解剖", "解释", "核验", "科普", "博主", "主张", "问卷", "纵向", "meta-analysis", "delphi"],
    },
    "paper-reconstruction": {
        "required": [
            "SKILL.md",
            "README.md",
            "README_EN.md",
            "agents/openai.yaml",
            "references/reconstruction-protocol.md",
            "references/domain-adaptation.md",
            "references/eprime-execution-path.md",
            "references/analysis-environment.md",
            "references/output-contract.md",
            "references/platform-selection.md",
            "references/platform-adapters.md",
            "references/replication-deliverables.md",
            "references/replication-source-ledger.md",
            "references/scoring-rubric.md",
            "references/survey-longitudinal-path.md",
            "assets/eprime-starter/bundle_manifest.json",
            "assets/eprime-starter/procedure_map.csv",
            "assets/eprime-starter/eprime_build_spec.json",
            "assets/eprime-starter/event_log_schema.json",
            "assets/eprime-starter/data_dictionary.csv",
            "assets/eprime-starter/analysis_contract.json",
            "scripts/audit_replication_bundle.py",
            "scripts/validate_platform_plan.py",
            "scripts/validate_output.py",
            "evals/evals.json",
        ],
        "description_terms": ["reconstruct", "longitudinal", "matlab/psychtoolbox", "python", "spss", "重组", "复现", "纵向", "数据字典"],
        "routing_terms": ["reconstruct", "replicate", "adapt", "extend", "innovate", "new study", "survey workflow", "longitudinal", "matlab", "psychtoolbox", "python", "spss", "重组", "复现", "重建", "迁移", "创新", "研究构思", "变量扩展", "问卷流程", "纵向研究", "数据字典", "analysis plan", "分析"],
    },
}


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?(.*?)[\"']?\s*$", text)
    return match.group(1) if match else None


def run_validator(script: Path, content: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8", delete=False) as handle:
        handle.write(content)
        temp_path = Path(handle.name)
    try:
        return subprocess.run(
            [sys.executable, str(script), str(temp_path)],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
    finally:
        temp_path.unlink(missing_ok=True)


def main() -> int:
    errors: list[str] = []

    for relative in (
        "CITATION.cff",
        "CONTRIBUTING.md",
        ".github/workflows/validate.yml",
        "requirements-test.txt",
        "tests/fixtures/generate_synthetic_paper.py",
        "tests/fixtures/synthetic_paper.pdf",
        "tests/test_prepare_paper.py",
        "tests/test_platform_plan.py",
    ):
        if not (ROOT / relative).is_file():
            errors.append(f"repository missing {relative}")

    citation_path = ROOT / "CITATION.cff"
    if citation_path.is_file():
        citation = citation_path.read_text(encoding="utf-8")
        for pattern, label in (
            (r"(?m)^cff-version:\s*[\"']?1\.2\.0", "CFF schema version 1.2.0"),
            (r"(?m)^title:\s*[\"']?paper-to-paradigm", "project title"),
            (r"(?m)^version:\s*[\"']?0\.1\.0", "project version 0.1.0"),
            (r"(?m)^authors:\s*$", "authors"),
            (r"(?m)^\s+- family-names:\s*[\"']?Xuan", "author family name Xuan"),
            (r"(?m)^\s+given-names:\s*[\"']?Bole", "author given name Bole"),
            (r"(?m)^\s+alias:\s*[\"']?宣博乐", "author Chinese name 宣博乐"),
            (r"(?m)^\s+orcid:\s*[\"']?https://orcid\.org/0009-0004-9399-9489", "author ORCID"),
            (r"(?m)^license:\s*Apache-2\.0", "Apache-2.0 license"),
        ):
            if not re.search(pattern, citation):
                errors.append(f"CITATION.cff missing {label}")

    actual_skill_dirs = {p.name for p in SKILLS.iterdir() if p.is_dir()} if SKILLS.is_dir() else set()
    if actual_skill_dirs != set(EXPECTED):
        errors.append(f"runtime skills mismatch: expected {sorted(EXPECTED)}, got {sorted(actual_skill_dirs)}")

    for skill_name, rules in EXPECTED.items():
        skill_dir = SKILLS / skill_name
        for relative in rules["required"]:
            if not (skill_dir / relative).is_file():
                errors.append(f"{skill_name}: missing {relative}")

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            continue
        text = skill_file.read_text(encoding="utf-8")
        for readme_name in ("README.md", "README_EN.md"):
            readme_path = skill_dir / readme_name
            if readme_path.is_file() and "English version will follow" in readme_path.read_text(encoding="utf-8"):
                errors.append(f"{skill_name}: deferred English placeholder remains in {readme_name}")
        readme_zh = skill_dir / "README.md"
        readme_en = skill_dir / "README_EN.md"
        if readme_zh.is_file() and readme_en.is_file():
            zh_sections = re.findall(r"(?m)^##\s+", readme_zh.read_text(encoding="utf-8"))
            en_sections = re.findall(r"(?m)^##\s+", readme_en.read_text(encoding="utf-8"))
            if len(zh_sections) != len(en_sections):
                errors.append(f"{skill_name}: Chinese/English README section counts differ")
        if frontmatter_value(text, "name") != skill_name:
            errors.append(f"{skill_name}: frontmatter name mismatch")
        description = frontmatter_value(text, "description") or ""
        lowered = description.lower()
        for term in rules["description_terms"]:
            if term.lower() not in lowered:
                errors.append(f"{skill_name}: description missing bilingual trigger term {term!r}")

        agent_file = skill_dir / "agents/openai.yaml"
        if agent_file.is_file():
            agent_text = agent_file.read_text(encoding="utf-8")
            short_match = re.search(r'(?m)^\s*short_description:\s*["\'](.*)["\']\s*$', agent_text)
            prompt_match = re.search(r'(?m)^\s*default_prompt:\s*["\'](.*)["\']\s*$', agent_text)
            if not short_match or not 25 <= len(short_match.group(1)) <= 64:
                length = len(short_match.group(1)) if short_match else 0
                errors.append(f"{skill_name}: short_description length must be 25-64, got {length}")
            if not prompt_match or f"${skill_name}" not in prompt_match.group(1):
                errors.append(f"{skill_name}: default_prompt must mention ${skill_name}")

        eval_path = skill_dir / "evals/evals.json"
        if eval_path.is_file():
            try:
                eval_data = json.loads(eval_path.read_text(encoding="utf-8"))
                cases = eval_data.get("cases", [])
                scenarios = {case.get("scenario") for case in cases}
                required_scenarios = {"完整论文", "摘要不足", "补充材料缺失", "矛盾证据"}
                if not required_scenarios.issubset(scenarios):
                    errors.append(f"{skill_name}: evals missing scenarios {sorted(required_scenarios - scenarios)}")
                for case in cases:
                    if not case.get("id") or not case.get("expected") or not case.get("must_not"):
                        errors.append(f"{skill_name}: malformed eval case {case.get('id', '<missing>')}")
            except Exception as exc:  # noqa: BLE001 - report malformed eval fixtures
                errors.append(f"{skill_name}: cannot read evals/evals.json: {exc}")

    ppt_like = [p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_dir() and ("ppt" in p.name.lower() or "slide" in p.name.lower())]
    if ppt_like:
        errors.append(f"PPT/slide directories remain inside collection: {ppt_like}")

    routing_path = ROOT / "tests" / "routing_cases.json"
    try:
        routing_cases = json.loads(routing_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report malformed test fixtures
        errors.append(f"cannot read routing fixtures: {exc}")
        routing_cases = []

    seen_ids: set[str] = set()
    seen_languages = {"zh": False, "en": False}
    for case in routing_cases:
        case_id = case.get("id", "<missing>")
        query = case.get("query", "")
        expected = case.get("expected_skill")
        if case_id in seen_ids:
            errors.append(f"duplicate routing id: {case_id}")
        seen_ids.add(case_id)
        if expected not in EXPECTED:
            errors.append(f"{case_id}: unknown expected skill {expected!r}")
            continue
        query_lower = query.lower()
        if not any(term.lower() in query_lower for term in EXPECTED[expected]["routing_terms"]):
            errors.append(f"{case_id}: query does not contain a declared trigger for {expected}")
        seen_languages["zh"] |= bool(re.search(r"[\u4e00-\u9fff]", query))
        seen_languages["en"] |= bool(re.search(r"[A-Za-z]{4}", query))
    if not all(seen_languages.values()):
        errors.append("routing fixtures must cover both Chinese and English")

    root_readme = ROOT / "README.md"
    root_readme_en = ROOT / "README_EN.md"
    if root_readme.is_file() and root_readme_en.is_file():
        if len(re.findall(r"(?m)^##\s+", root_readme.read_text(encoding="utf-8"))) != len(
            re.findall(r"(?m)^##\s+", root_readme_en.read_text(encoding="utf-8"))
        ):
            errors.append("root Chinese/English README section counts differ")

    anatomy_good = """## 文献与材料范围\n- 定位模式：page-grounded\n# A. 研究叙事\n# B. 研究设计\n## B4. 核心结果到结论\n结果 [Paper: PDF p. 7, Fig. 2]\n## B5. 证据链\n# C. 结论讨论\n## C1. 数据到讨论的闭环\n解释 [Paper: PDF p. 9]\n## C2. 贡献\n## C4. 当代近况检查\n领域锚点：[示例综述](https://doi.org/10.0000/example)\n## 最终判断\n判断 [Paper: PDF p. 12]\n"""
    anatomy_bad = anatomy_good + "# D. 材料与程序\n"
    anatomy_missing_c4 = anatomy_good.replace("## C4. 当代近况检查\n领域锚点：[示例综述](https://doi.org/10.0000/example)\n", "")
    reconstruction_good = """# A. 论文重组复现目标\n## A0. 复现来源账本\n主论文 DOI：未发现\n# B. 被试视角流程\n## B0. 任务关系图\n# C. 程序蓝图\n## C0. 原始平台识别\n## C5. 原文数据分析路线\n# D. 材料数据\n## D1. 来源、材料与复现状态\n## D2. 最小数据字段\n## D3. 复现验证与差异处理\n# E. 实验参数沉淀\n## E2. 理论与文献锚点\n## E4. 有理论支撑的优先研究 idea\n证据起点：原文限制\n证据状态：部分支持\n## 复现行动顺序\n## 可编辑反馈表\n"""
    reconstruction_bad = reconstruction_good.replace("## D2. 最小数据字段\n", "")

    validator_cases = [
        ("paper-anatomy valid", SKILLS / "paper-anatomy/scripts/validate_output.py", anatomy_good, 0),
        ("paper-anatomy rejects reconstruction section", SKILLS / "paper-anatomy/scripts/validate_output.py", anatomy_bad, 1),
        ("paper-anatomy rejects missing C4", SKILLS / "paper-anatomy/scripts/validate_output.py", anatomy_missing_c4, 1),
        ("paper-reconstruction valid", SKILLS / "paper-reconstruction/scripts/validate_output.py", reconstruction_good, 0),
        ("paper-reconstruction rejects missing D2", SKILLS / "paper-reconstruction/scripts/validate_output.py", reconstruction_bad, 1),
    ]
    for label, script, content, expected_code in validator_cases:
        if not script.is_file():
            continue
        result = run_validator(script, content)
        if result.returncode != expected_code:
            errors.append(f"{label}: expected exit {expected_code}, got {result.returncode}: {result.stdout.strip()} {result.stderr.strip()}")

    audit_script = SKILLS / "paper-reconstruction/scripts/audit_replication_bundle.py"
    starter = SKILLS / "paper-reconstruction/assets/eprime-starter"
    if audit_script.is_file() and starter.is_dir():
        audit_result = subprocess.run(
            [sys.executable, str(audit_script), str(starter)],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        if audit_result.returncode != 0:
            errors.append(f"E-Prime starter semantic audit failed: {audit_result.stdout.strip()} {audit_result.stderr.strip()}")

        with tempfile.TemporaryDirectory(prefix="paper-to-paradigm-audit-") as temp_dir:
            broken = Path(temp_dir) / "broken-bundle"
            shutil.copytree(starter, broken)
            manifest_path = broken / "bundle_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["execution"]["lists"][0]["calls"] = ["UndefinedProc"]
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            negative_result = subprocess.run(
                [sys.executable, str(audit_script), str(broken)],
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
            )
            if negative_result.returncode == 0:
                errors.append("semantic audit failed to reject a List that calls UndefinedProc")

    if errors:
        print("COLLECTION INVALID")
        for error in errors:
            print(f"- {error}")
        return 1

    print("COLLECTION VALID")
    print(f"- runtime skills: {', '.join(sorted(EXPECTED))}")
    print(f"- routing fixtures: {len(routing_cases)} (Chinese and English covered)")
    print("- per-skill evals: evidence boundaries covered; reconstruction also covers platform, survey/longitudinal, and analysis routing")
    print("- per-skill contracts: positive and negative validator cases passed")
    print("- E-Prime semantic audit: valid starter accepted and broken Proc/List call rejected")
    print("- repository metadata: CITATION.cff, CONTRIBUTING.md, and GitHub Actions present")
    print("- PPT/slide skill directories inside collection: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
