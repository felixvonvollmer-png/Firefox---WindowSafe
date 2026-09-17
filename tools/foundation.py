"""Offline WindowSafe foundation checks; no browser or provider access."""

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SHA = "80203ae9f554aa4dba951d316a685bd20cbe57ef28a2912fd49608cdaf9cb6a8"
HANDOFF_SHA = "15701c717061773d9017cf3c884a7eb0cebcb0d66b67a93dc13e41acb7d98774"
BLOBS = {
    "foundation-1.md": "3b139a7dfd70da3ae6c83bbdfa703cb98ef94193",
    "foundation-2.md": "ff49e56aba09881e9e4a22dc8225949fbc4b54f6",
}
CONTRACT_PATH = "reviews/review-contract.json"
RESULT_FIELDS = {
    "schema_version", "review_id", "review_type", "reviewer", "provenance",
    "subject", "verdict", "findings", "reviewed_evidence", "result_reference",
}
SEMANTIC_MAPPING = {
    "REVIEW_ID": "review_id", "REVIEW_TYPE": "review_type",
    "REVIEWER_OR_REVIEW_AUTHORITY": "reviewer", "RESULT_PROVENANCE": "provenance",
    "SUBJECT_ID_OR_EQUIVALENT_STABLE_SUBJECT_REFERENCE": "subject.id",
    "SUBJECT_END_SHA_OR_EQUIVALENT_IMMUTABLE_END_STATE": "subject.end_sha",
    "VERDICT": "verdict", "FINDINGS": "findings",
    "REVIEWED_EVIDENCE_REFERENCE": "reviewed_evidence",
    "REVIEW_RESULT_REFERENCE": "result_reference",
}
AUTHORITIES = {
    "PROJECT_FOUNDATION_REVIEW": "INDEPENDENT_PROJECT_LLM",
    "EPIC_PREPARATION_REVIEW": "INDEPENDENT_EPIC_PREPARATION_REVIEWER",
    "FEATURE_ACCEPTANCE_REVIEW": "INDEPENDENT_ACCEPTANCE_REVIEWER",
}
ID_PATTERN = r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}"
SHA_PATTERN = r"[0-9a-f]{40}"


class Invalid(ValueError):
    """A closed gate with a safe categorical reason."""


def require(condition, reason):
    if not condition:
        raise Invalid(reason)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def reject_constant(_value):
    raise Invalid("non-finite JSON value")


def parse(data):
    return json.loads(data, object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], stderr=subprocess.PIPE)


def safe_path(value):
    require(isinstance(value, str) and value and "\\" not in value, "invalid path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts, "unsafe path")
    require(str(path) == value and ":" not in value, "noncanonical path")
    return value


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "empty or nontext field")


def fields(value, expected):
    require(isinstance(value, dict) and set(value) == set(expected), "object fields mismatch")


def identifier(value):
    require(isinstance(value, str) and re.fullmatch(ID_PATTERN, value), "invalid ID")


def commit(ref):
    value = git("rev-parse", "--verify", ref + "^{commit}").decode().strip()
    require(re.fullmatch(SHA_PATTERN, value), "invalid commit")
    return value


def at(sha, path):
    require(re.fullmatch(SHA_PATTERN, sha), "full commit SHA required")
    return git("show", sha + ":" + safe_path(path))


def validate_contract(c):
    fields(c, {
        "contract_version", "format", "result_channel", "required_fields", "review_types",
        "verdicts", "severities", "finding_statuses", "reviewer_fields", "provenance_fields",
        "subject_fields", "evidence_fields", "finding_fields", "authorities", "independence",
        "transport", "rules", "semantic_minimum_mapping",
    })
    require(type(c["contract_version"]) is int and c["contract_version"] == 1, "contract version")
    require(c["format"] == "WINDOWSAFE_REVIEW_CONTRACT_V1", "contract format")
    require(c["result_channel"] == "reviews/results/<REVIEW_ID>.json", "result channel")
    require(c["semantic_minimum_mapping"] == SEMANTIC_MAPPING, "semantic minimum mismatch")
    require(c["authorities"] == AUTHORITIES, "review authorities mismatch")
    expected = {
        "required_fields": RESULT_FIELDS,
        "review_types": set(AUTHORITIES),
        "verdicts": {"PASS", "CORRECTION_REQUIRED", "BLOCKED"},
        "severities": {"CRITICAL", "BLOCKING", "MAJOR", "MINOR", "NIT_OR_SUGGESTION"},
        "finding_statuses": {"OPEN", "RESOLVED"},
        "reviewer_fields": {"authority", "identity", "run_reference", "independence"},
        "provenance_fields": {"source_reference", "transport"},
        "subject_fields": {"id", "path", "end_sha"},
        "evidence_fields": {"path", "sha256"},
        "finding_fields": {"id", "severity", "status", "description", "disposition"},
        "transport": {"DIRECT_CANONICAL_WRITE", "EXACT_AUTHORIZED_TRANSFER"},
        "rules": {
            "ALL_FIELDS_REQUIRED_NO_ADDITIONAL_FIELDS", "NONEMPTY_STRINGS",
            "EXACT_SUBJECT_COMMIT_AND_PATH", "EVIDENCE_BYTES_AT_SUBJECT_COMMIT",
            "REVIEWER_DIFFERS_FROM_SUBJECT_IMPLEMENTER", "ROLE_MATCHES_REVIEW_TYPE",
            "RESULT_FILENAME_MATCHES_ID", "PASS_HAS_NO_OPEN_CRITICAL_BLOCKING_MAJOR",
            "MINOR_OPEN_HAS_NONBLOCKING_DISPOSITION", "APPEND_ONLY_HISTORY_NO_COUNT_LIMIT",
            "SCHEMA_PREFLIGHT_EXACT_CONTRACT_EQUALITY", "PROVENANCE_REQUIRES_EXTERNAL_AUTHENTICATION",
        },
    }
    for key, values in expected.items():
        require(isinstance(c[key], list) and all(isinstance(v, str) for v in c[key]), "contract list")
        require(len(c[key]) == len(values) and set(c[key]) == values, "contract field/rule drift")
    require(c["independence"] == "FRESH_OR_SUFFICIENTLY_ISOLATED", "independence contract")


def schema_preflight(canonical, external):
    validate_contract(canonical)
    validate_contract(external)
    require(canonical == external, "external output schema mismatch")


def request(sha, path="foundation/subject.json"):
    sha = commit(sha)
    c = parse(at(sha, CONTRACT_PATH))
    validate_contract(c)
    s = parse(at(sha, path))
    identifier(s["subject_id"])
    require(s["review_type"] in AUTHORITIES, "subject review type")
    kind = s["review_type"]
    expected = {
        "PROJECT_FOUNDATION_REVIEW": "foundation/subject.json",
        "EPIC_PREPARATION_REVIEW": "epics/" + s["subject_id"] + "/subject.json",
        "FEATURE_ACCEPTANCE_REVIEW": "features/" + s["subject_id"] + "/subject.json",
    }[kind]
    require(path == expected, "subject locator mismatch")
    text(s["implementer"])
    require(isinstance(s["evidence_paths"], list) and s["evidence_paths"], "missing subject evidence")
    require(len(s["evidence_paths"]) == len(set(s["evidence_paths"])), "duplicate evidence")
    evidence = [{"path": safe_path(p), "sha256": sha256(at(sha, p))} for p in s["evidence_paths"]]
    return {
        "review_type": kind,
        "subject": {"id": s["subject_id"], "path": path, "end_sha": sha},
        "implementer": s["implementer"], "required_authority": c["authorities"][kind],
        "reviewed_evidence": evidence,
        "contract_sha256": sha256(at(sha, CONTRACT_PATH)),
    }


def validate_result(result, req, c, filename):
    validate_contract(c)
    fields(result, c["required_fields"])
    require(type(result["schema_version"]) is int and result["schema_version"] == 1, "schema version")
    identifier(result["review_id"])
    require(filename == result["review_id"] + ".json", "ID/filename mismatch")
    require(result["result_reference"] == "reviews/results/" + filename, "result locator mismatch")
    require(result["review_type"] == req["review_type"], "review type mismatch")
    fields(result["subject"], c["subject_fields"])
    require(result["subject"] == req["subject"], "subject mismatch")
    r = result["reviewer"]
    fields(r, c["reviewer_fields"])
    for value in r.values():
        text(value)
    require(r["authority"] == req["required_authority"], "review authority mismatch")
    require(r["identity"].casefold() != req["implementer"].casefold(), "self verdict prohibited")
    require(r["independence"] == c["independence"], "independent context required")
    fields(result["provenance"], c["provenance_fields"])
    text(result["provenance"]["source_reference"])
    require(result["provenance"]["transport"] in c["transport"], "transport mode")
    evidence = result["reviewed_evidence"]
    require(isinstance(evidence, list) and evidence, "missing evidence")
    for e in evidence:
        fields(e, c["evidence_fields"])
        safe_path(e["path"])
        require(isinstance(e["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", e["sha256"]), "evidence digest")
    require(sorted(evidence, key=lambda e: e["path"]) == sorted(req["reviewed_evidence"], key=lambda e: e["path"]), "evidence binding mismatch")
    require(result["verdict"] in c["verdicts"], "invalid verdict")
    require(isinstance(result["findings"], list), "findings must be a list")
    seen = set()
    for finding in result["findings"]:
        fields(finding, c["finding_fields"])
        identifier(finding["id"])
        require(finding["id"] not in seen, "duplicate finding ID")
        seen.add(finding["id"])
        require(finding["severity"] in c["severities"], "finding severity")
        require(finding["status"] in c["finding_statuses"], "finding status")
        text(finding["description"])
        text(finding["disposition"])
        if result["verdict"] == "PASS":
            require(not (finding["status"] == "OPEN" and finding["severity"] in {"CRITICAL", "BLOCKING", "MAJOR"}), "PASS with blocking finding")


def validate_result_file(path):
    result = parse(path.read_bytes())
    sha = result["subject"]["end_sha"]
    require(isinstance(sha, str) and re.fullmatch(SHA_PATTERN, sha), "immutable SHA required")
    req = request(sha, result["subject"]["path"])
    validate_result(result, req, parse(at(sha, CONTRACT_PATH)), path.name)


def input_integrity(root):
    base = root / "foundation/inputs"
    manifest = (base / "SHA256SUMS.json").read_bytes()
    require(sha256(manifest) == MANIFEST_SHA, "input manifest hash mismatch")
    entries = parse(manifest)["FILES"]
    expected = {"SHA256SUMS.json"}
    for entry in entries:
        name = safe_path(entry["path"])
        require(name not in expected, "duplicate manifest path")
        expected.add(name)
        data = (base / name).read_bytes()
        require(len(data) == entry["bytes"] and sha256(data) == entry["sha256"], "input integrity mismatch")
    actual = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
    require(expected == actual, "input inventory mismatch")
    handoff = base / "WindowSafe_Project_Foundation_Agent_Start_Handoff_WS-PFBOOT-20260917-01.md"
    require(sha256(handoff.read_bytes()) == HANDOFF_SHA, "handoff mismatch")
    for name, sha in BLOBS.items():
        data = (root / "foundation/sources" / name).read_bytes()
        identity = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(identity == sha, "foundation blob mismatch")


def files(root):
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(p in {".git", "build", "__pycache__"} for p in relative.parts):
            continue
        require(not path.is_symlink(), "symlink prohibited")
        if path.is_file():
            yield path


def scope(path):
    allowed_root = {"README.md", "AGENTS.md", ".gitignore", ".gitattributes"}
    allowed = path in allowed_root or path == ".github/workflows/foundation.yml"
    allowed |= bool(re.fullmatch(r"foundation/(inputs/.+|sources/foundation-[12]\.md|[a-z-]+\.(md|json)|evidence/[a-z-]+\.(md|json))", path))
    allowed |= bool(re.fullmatch(r"(tools|tests)/[a-z_]+\.py", path))
    allowed |= path in {"epics/README.md", "reviews/README.md", CONTRACT_PATH}
    allowed |= bool(re.fullmatch(r"reviews/results/" + ID_PATTERN + r"\.json", path))
    require(allowed, "outside foundation-only path scope")
    require(PurePosixPath(path).name != "manifest.json", "extension manifest prohibited")


def check(root=ROOT):
    require(sys.version_info[:3] == (3, 14, 4), "Python 3.14.4 required")
    input_integrity(root)
    validate_contract(parse((root / CONTRACT_PATH).read_bytes()))
    subject = parse((root / "foundation/subject.json").read_bytes())
    require(subject["product_features_started"] is False and subject["epic_started"] is False, "product start prohibited")
    require(subject["status"] == "PROJECT_FOUNDATION_READY_FOR_REVIEW", "foundation lifecycle drift")
    require(subject["independent_review_status"] == "PENDING", "self acceptance prohibited")
    require(subject["platform_qualification"] == subject["performance_method_binding"] == "REQUIRED_BEFORE_AFFECTED_PRODUCT_IMPLEMENTATION", "preimplementation gate drift")
    require(subject["runtime_evidence"] == "NOT_EXECUTED", "runtime claim drift")
    for path in files(root):
        rel = path.relative_to(root).as_posix()
        scope(rel)
        data = path.read_bytes()
        content = data.decode("utf-8")
        if path.suffix == ".json":
            parse(data)
        if rel.startswith(("foundation/inputs/", "foundation/sources/")):
            continue  # Original bytes, including original whitespace, are immutable.
        require(content.endswith("\n") and "\r" not in content, "text newline format")
        require(all(line == line.rstrip() for line in content.splitlines()), "trailing whitespace")
        if path.suffix == ".py":
            ast.parse(content)
        if path.suffix == ".md":
            for link in re.findall(r"\]\(([^)]+)\)", content):
                if "://" not in link and not link.startswith("#"):
                    target = link.split("#", 1)[0]
                    require((path.parent / target).is_file(), "missing local document link")
        if rel.startswith("reviews/results/"):
            validate_result_file(path)
    workflow = (root / ".github/workflows/foundation.yml").read_text()
    require("contents: read" in workflow and "persist-credentials: false" in workflow, "CI privilege drift")
    require(re.findall(r"(?m)^\s*permissions:.*$", workflow) == ["permissions:"], "additional CI permissions")
    permissions = re.search(r"(?m)^permissions:\n((?:  [^\n]+\n)+)", workflow)
    require(permissions is not None and permissions.group(1) == "  contents: read\n", "CI permission scope")
    require("pull_request_target" not in workflow and "secrets." not in workflow, "CI trust drift")
    require("python-version: '3.14.4'" in workflow, "CI Python pin drift")
    actions = re.findall(r"uses: ([^\s]+)", workflow)
    require(actions == ["actions/checkout@11d5960a326750d5838078e36cf38b85af677262", "actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065"], "CI action pin drift")
    for command in ["foundation.py check", "unittest discover", "foundation.py build --verify-repeat", "foundation.py history --event-base"]:
        require(command in workflow, "missing CI gate")
    if root == ROOT and (root / ".git").exists():
        # Ignored build/cache directories cannot hide tracked out-of-scope files.
        for name in git("ls-files", "--cached", "-z").split(b"\0"):
            if name:
                scope(name.decode())


def build_bytes(root):
    inventory = [{"path": p.relative_to(root).as_posix(), "sha256": sha256(p.read_bytes()), "bytes": p.stat().st_size} for p in files(root)]
    return (json.dumps({"artifact": "FOUNDATION_INVENTORY_NOT_ADDON", "files": inventory}, indent=2) + "\n").encode()


def protected(path):
    return path.startswith(("foundation/inputs/", "foundation/sources/", "reviews/results/"))


def check_history_maps(before, after):
    for path, value in before.items():
        if protected(path):
            require(path in after and after[path] == value, "append-only history violated")


def history(base):
    head = commit("HEAD")
    if not base or base == "0" * 40:
        require(git("rev-list", "--count", head).strip() == b"1", "missing noninitial history baseline")
        return
    base = commit(base)
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", base, head], check=True, capture_output=True)
    before = {}
    for entry in git("ls-tree", "-rz", "--full-tree", base).split(b"\0"):
        if not entry:
            continue
        _metadata, name = entry.split(b"\t", 1)
        path = name.decode()
        if protected(path):
            before[path] = at(base, path)
    after = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in files(ROOT)}
    check_history_maps(before, after)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "build", "request", "schema-preflight", "validate-result", "history"])
    parser.add_argument("--sha", default="HEAD")
    parser.add_argument("--subject", default="foundation/subject.json")
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--base")
    parser.add_argument("--event-base", action="store_true")
    parser.add_argument("--verify-repeat", action="store_true")
    args = parser.parse_args()
    if args.command == "check":
        check()
    elif args.command == "build":
        check()
        result = build_bytes(ROOT)
        if args.verify_repeat:
            require(result == build_bytes(ROOT), "nondeterministic build")
        require(not (ROOT / "build").is_symlink(), "build symlink prohibited")
        (ROOT / "build").mkdir(exist_ok=True)
        (ROOT / "build/foundation-inventory.json").write_bytes(result)
        print("FOUNDATION_INVENTORY_SHA256", sha256(result))
    elif args.command == "request":
        print(json.dumps(request(args.sha, args.subject), indent=2))
        return
    elif args.command == "schema-preflight":
        require(args.schema is not None, "external schema required")
        schema_preflight(parse(at(commit(args.sha), CONTRACT_PATH)), parse(args.schema.read_bytes()))
    elif args.command == "validate-result":
        require(args.file is not None, "result file required")
        validate_result_file(args.file)
    elif args.command == "history":
        base = os.environ.get("FOUNDATION_EVENT_BASE") if args.event_base else args.base
        require(args.event_base or args.base is not None, "explicit history baseline required")
        history(base)
    print(args.command.upper() + " OK (mechanical evidence only)")


if __name__ == "__main__":
    try:
        main()
    except (Invalid, KeyError, TypeError, ValueError, OSError, subprocess.SubprocessError):
        print("FOUNDATION_GATE_FAILED: invalid input, binding, environment or history", file=sys.stderr)
        sys.exit(1)
