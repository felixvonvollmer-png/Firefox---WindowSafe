"""Offline WindowSafe foundation checks; no browser or provider access."""

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
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
NONBLOCKING_PREFIX = "EXPLICIT_NONBLOCKING_FOLLOW_UP: "
MINOR_DISPOSITION_CONTRACT = {
    "prefix": NONBLOCKING_PREFIX,
    "rationale": "NONEMPTY_TEXT_WITHOUT_ADDITIONAL_DISPOSITION_MARKERS",
    "applies_to": "ALL_OPEN_MINOR_FINDINGS_REGARDLESS_OF_VERDICT",
    "legacy_v1": "ENFORCE_EXPLICIT_NONBLOCKING_SEMANTICS_WITH_SAME_MARKER_NO_ID_EXEMPTIONS",
    "limitation": "MARKER_IS_NOT_PROOF_OF_AUTHENTICITY_OR_SEMANTIC_NONBLOCKING",
}
LEGACY_POSITIVE = "nonblocking follow-up with next-review trigger"
LEGACY_DISPOSITION_CONTRACT = {
    "recognized_v1_text": LEGACY_POSITIVE,
    "explicit_marker_also_supported": NONBLOCKING_PREFIX,
    "otherwise": "V1_SEMANTIC_DISPOSITION_REQUIRED_NOT_V2_SYNTAX_ERROR",
    "sidecar": "reviews/dispositions/<REVIEW_ID>.json",
    "binding_fields": ["result_sha256", "subject", "reviewed_evidence", "original_provenance"],
    "required_fields": ["result_sha256", "subject", "reviewed_evidence", "original_provenance", "reviewer", "provenance", "decisions"],
    "decision_fields": ["finding_id", "original_disposition_sha256", "decision", "rationale", "follow_up", "trigger"],
    "decision": "NONBLOCKING_FOLLOW_UP",
    "authority": "SAME_ROLE_AND_INDEPENDENCE_REQUIREMENTS_AS_BOUND_REVIEW",
    "limits": "V1_ONLY_NO_EMPTY_OR_EXPLICIT_BLOCKING_OVERRIDE_EXTERNAL_AUTHENTICATION_REQUIRED",
}
CURRENT_MINOR_CONTRACT = dict(MINOR_DISPOSITION_CONTRACT,
    legacy_v1="HISTORICAL_SEMANTICS_WITH_BOUND_SEPARATE_DISPOSITION_WHEN_UNCLEAR")
FOLLOWUP_AUTH = "foundation/evidence/followup-authorization.json"
# Original user authorization, independent of editable subject/baseline claims.
# New preparations require their own externally authorized trust anchor.
PREPARATION_AUTHORIZATIONS = {
    "epics/WS-E01/evidence/preparation-authorization.json":
        "72fbabec02b37e199cb5043cd2accdfd3925e3ab0c09e58f62f032e7ae3e9b0d",
}
# Separately approved integration originals; a PASS alone cannot open this gate.
INTEGRATION_AUTHORIZATIONS = {
    "epics/WS-E01/evidence/integration-authorization.json":
        "ae698e67364c3a887a867d976aaf254deb0811915b4f309a8e4e47e774f79c6b",
}
INTEGRATION_SUPPORT_PATHS = {
    "README.md", "AGENTS.md", "reviews/README.md", "epics/README.md",
    "foundation/context.md", "foundation/engineering.md",
    "tools/foundation.py", "tests/test_foundation.py",
}
SELF_REVIEW_COMPLETE = "COMPLETE__NO_OPEN_CRITICAL_BLOCKING_MAJOR_SELF_FINDINGS"
FOLLOWUP_INPUTS = {
    FOLLOWUP_AUTH: "f3f0c51070e51974bfc6979e5db4ead2cdfa131315c0654ebad8773e467320ed",
    "foundation/evidence/followup-handoff.md": "17461e12b7a8ff3fcd8fcf5924e506147a471c44a28e626df184dbc91120bb61",
    "foundation/evidence/followup-draft.md": "77f91ef8333959c6e69c2af510600101fc3fcd241fd5b5be49eee475967582f7",
    "foundation/evidence/followup-environment-authorization.md": "263a209c0a8233e72fec5020fe5cdb2716f9a4d07c2b3c3b862d104e62a5428d",
    "foundation/evidence/followup-environment-draft.md": "40d65217da93528afddd5f469884bc4571dfc548c36af445ab92dd3066bebbf4",
    "foundation/evidence/followup-return.json": "55036d0f3845321f7b66dc8b4cac0f45e57222d6f32816420035c4dbcfcf12ed",
    "foundation/evidence/followup-baseline.json": "ca79ad0e6433281341215e98eaff763397d7886966238e743440a8c5d2186d4c",
    "foundation/evidence/followup-manifest.json": "85e15f981b0b1c134234759ddd072d63c7521351c14b84c23138081e6b56950b",
    "foundation/evidence/followup-return-manifest.json": "486f0fc704a75b52ed5fa8761ef8c271f5d9cfa6181174dd638a08fc48b8a4fe",
}
CORRECTION_INPUTS = {
    "foundation/evidence/harness-authorization.json": "25f0ee35f9cafe89230f47e218d31a43c2aecb57f4f67446008c4a8c4eb3e0ab",
    "foundation/evidence/harness-handoff.md": "f7957cf9e9643616c78b49d8ffa5912e6d49a9bc155fae95a41192d4c90e0e46",
    "foundation/evidence/harness-draft.md": "83fee934ec31863b808af771481fcda6d65954b74e62628c1b73e8e24d61bffe",
    "foundation/evidence/harness-residual.json": "694ac89f40e9246ee8eb4c79b4a5f5712e0079270258fdc90529abe95d223a18",
    "foundation/evidence/harness-return.json": "c9af93124931e13442e38b40ee476f0a738b8f16b6f0a67f10dfa94a2aaf0e12",
}


class Invalid(ValueError):
    """A closed gate with a safe categorical reason."""


class SemanticDispositionRequired(Invalid):
    """Unclear V1 semantics require separate, bound independent evidence."""


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
    require(isinstance(c, dict), "contract object required")
    version = c.get("contract_version")
    require(type(version) is int and version in {1, 2, 3}, "contract version")
    expected_fields = {
        "contract_version", "format", "result_channel", "required_fields", "review_types",
        "verdicts", "severities", "finding_statuses", "reviewer_fields", "provenance_fields",
        "subject_fields", "evidence_fields", "finding_fields", "authorities", "independence",
        "transport", "rules", "semantic_minimum_mapping",
    }
    if version >= 2:
        expected_fields.add("minor_open_disposition")
    if version == 3:
        expected_fields.add("legacy_v1_disposition")
    fields(c, expected_fields)
    require(c["format"] == "WINDOWSAFE_REVIEW_CONTRACT_V" + str(version), "contract format")
    if version == 2:
        require(c["minor_open_disposition"] == MINOR_DISPOSITION_CONTRACT, "minor disposition contract drift")
    if version == 3:
        require(c["minor_open_disposition"] == CURRENT_MINOR_CONTRACT, "minor disposition contract drift")
        require(c["legacy_v1_disposition"] == LEGACY_DISPOSITION_CONTRACT, "legacy semantics contract drift")
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
    if kind == "EPIC_PREPARATION_REVIEW":
        epic_preparation(path, lambda name: at(sha, name), sha)
        binding = parse(at(sha, path.replace("subject.json", "binding.json")))
        if binding["status"] == "READY_FOR_AGENT":
            # A current accepted locator still requests the original reviewed bytes.
            return request(binding["epic_preparation_subject_immutable_reference"]["end_sha"], path)
    evidence = [{"path": safe_path(p), "sha256": sha256(at(sha, p))} for p in s["evidence_paths"]]
    return {
        "schema_version": c["contract_version"],
        "review_type": kind,
        "subject": {"id": s["subject_id"], "path": path, "end_sha": sha},
        "implementer": s["implementer"], "required_authority": c["authorities"][kind],
        "reviewed_evidence": evidence,
        "contract_sha256": sha256(at(sha, CONTRACT_PATH)),
    }


def validate_result(result, req, c, filename, semantic=None, raw_sha=None):
    validate_contract(c)
    fields(result, c["required_fields"])
    require(type(result["schema_version"]) is int and result["schema_version"] == c["contract_version"], "schema version")
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
    unclear = []
    for finding in result["findings"]:
        fields(finding, c["finding_fields"])
        identifier(finding["id"])
        require(finding["id"] not in seen, "duplicate finding ID")
        seen.add(finding["id"])
        require(finding["severity"] in c["severities"], "finding severity")
        require(finding["status"] in c["finding_statuses"], "finding status")
        text(finding["description"])
        text(finding["disposition"])
        if finding["status"] == "OPEN" and finding["severity"] == "MINOR":
            disposition = finding["disposition"]
            if c["contract_version"] == 1 and disposition == LEGACY_POSITIVE:
                pass  # Historical positive semantics; no review ID or SHA exemption.
            elif disposition.startswith(NONBLOCKING_PREFIX):
                rationale = disposition[len(NONBLOCKING_PREFIX):]
                text(rationale)
                require(not re.search(r"\b(?:EXPLICIT_[A-Z_]+|BLOCKING|NONBLOCKING)\s*:", rationale, re.IGNORECASE), "ambiguous disposition markers")
            elif c["contract_version"] == 1:
                require(not re.search(r"\b(?:EXPLICIT_[A-Z_]+|BLOCKING|NONBLOCKING)\s*:", disposition, re.IGNORECASE), "ambiguous or blocking disposition marker")
                unclear.append(finding)
            else:
                raise Invalid("explicit nonblocking marker required")
        if result["verdict"] == "PASS":
            require(not (finding["status"] == "OPEN" and finding["severity"] in {"CRITICAL", "BLOCKING", "MAJOR"}), "PASS with blocking finding")
    if unclear:
        if semantic is None:
            raise SemanticDispositionRequired("V1_SEMANTIC_DISPOSITION_REQUIRED")
        validate_semantic_disposition(semantic, result, req, unclear, raw_sha)
    else:
        require(semantic is None, "unexpected semantic disposition")


def validate_semantic_disposition(record, result, req, unclear, raw_sha):
    fields(record, LEGACY_DISPOSITION_CONTRACT["required_fields"])
    require(isinstance(raw_sha, str) and re.fullmatch(r"[0-9a-f]{64}", raw_sha), "original bytes required")
    require(record["result_sha256"] == raw_sha, "semantic original result mismatch")
    for key in ("subject", "reviewed_evidence"):
        require(record[key] == result[key], "semantic subject/evidence mismatch")
    require(record["original_provenance"] == result["provenance"], "semantic original provenance mismatch")
    reviewer = record["reviewer"]
    fields(reviewer, {"authority", "identity", "run_reference", "independence"})
    for value in reviewer.values():
        text(value)
    require(reviewer["authority"] == req["required_authority"], "semantic authority mismatch")
    require(reviewer["identity"].casefold() != req["implementer"].casefold(), "semantic self disposition")
    require(reviewer["independence"] == "FRESH_OR_SUFFICIENTLY_ISOLATED", "semantic independence")
    fields(record["provenance"], {"source_reference", "transport"})
    text(record["provenance"]["source_reference"])
    require(record["provenance"]["transport"] in {"DIRECT_CANONICAL_WRITE", "EXACT_AUTHORIZED_TRANSFER"}, "semantic transport")
    decisions = record["decisions"]
    require(isinstance(decisions, list) and len(decisions) == len(unclear), "semantic decisions incomplete")
    expected = {finding["id"]: finding for finding in unclear}
    for decision in decisions:
        fields(decision, LEGACY_DISPOSITION_CONTRACT["decision_fields"])
        finding = expected.pop(decision["finding_id"], None)
        require(finding is not None, "semantic finding mismatch")
        require(decision["original_disposition_sha256"] == sha256(finding["disposition"].encode()), "semantic disposition mismatch")
        require(decision["decision"] == "NONBLOCKING_FOLLOW_UP", "semantic nonblocking decision required")
        for key in ("rationale", "follow_up", "trigger"):
            text(decision[key])


def validate_result_file(path, semantic_path=None):
    data = path.read_bytes()
    result = parse(data)
    sha = result["subject"]["end_sha"]
    require(isinstance(sha, str) and re.fullmatch(SHA_PATTERN, sha), "immutable SHA required")
    req = request(sha, result["subject"]["path"])
    if semantic_path is None and path.parent.resolve() == (ROOT / "reviews/results").resolve():
        candidate = ROOT / "reviews/dispositions" / path.name
        if candidate.exists():
            semantic_path = candidate
    semantic = parse(semantic_path.read_bytes()) if semantic_path else None
    try:
        validate_result(result, req, parse(at(sha, CONTRACT_PATH)), path.name, semantic, sha256(data))
    except SemanticDispositionRequired:
        # A machine-readable unresolved request, not a fabricated disposition or V2 error.
        print(json.dumps({"status": "V1_SEMANTIC_DISPOSITION_REQUIRED", "result_sha256": sha256(data),
                          "subject": result["subject"], "reviewed_evidence": result["reviewed_evidence"],
                          "original_provenance": result["provenance"],
                          "required_authority": req["required_authority"],
                          "original_result_reference": result["result_reference"],
                          "sidecar_contract": LEGACY_DISPOSITION_CONTRACT}, indent=2))
        raise


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
    safe_path(path)
    allowed_root = {"README.md", "AGENTS.md", ".gitignore", ".gitattributes"}
    allowed = path in allowed_root or path == ".github/workflows/foundation.yml"
    allowed |= bool(re.fullmatch(r"foundation/(inputs/.+|sources/foundation-[12]\.md|[a-z-]+\.(md|json)|evidence/[a-z-]+\.(md|json))", path))
    allowed |= bool(re.fullmatch(r"(tools|tests)/[a-z_]+\.py", path))
    allowed |= path in {"epics/README.md", "reviews/README.md", CONTRACT_PATH}
    allowed |= bool(re.fullmatch(r"epics/" + ID_PATTERN
                                + r"/(subject\.json|binding\.json|preparation\.md|evidence/"
                                + ID_PATTERN + r"\.(md|json))", path))
    allowed |= bool(re.fullmatch(r"reviews/results/" + ID_PATTERN + r"\.json", path))
    allowed |= bool(re.fullmatch(r"reviews/dispositions/" + ID_PATTERN + r"\.json", path))
    require(allowed, "outside foundation-only path scope")
    require(PurePosixPath(path).name != "manifest.json", "extension manifest prohibited")


def epic_preparation(path, read, head):
    """Mechanical preparation binding only; never an independent verdict."""
    safe_path(path)
    subject = parse(read(path))
    epic = subject["subject_id"]
    identifier(epic)
    prefix = "epics/" + epic + "/"
    require(path == prefix + "subject.json", "epic subject locator")
    binding = parse(read(prefix + "binding.json"))
    if binding["status"] == "READY_FOR_AGENT":
        reviewed = accepted_epic_binding(path, read, head)
        return epic_preparation(path, lambda name: at(reviewed, name), reviewed)
    require(subject["review_type"] == "EPIC_PREPARATION_REVIEW", "epic review type")
    require(subject["status"] == "EPIC_PREPARATION_READY_FOR_REVIEW", "epic lifecycle")
    text(subject["implementer"])
    identifier(subject["epic_preparation_id"])
    require(subject["ready_for_agent"] is False, "epic execution prohibited")
    require(subject["product_features_started"] is False
            and subject["browser_profile_tests_executed"] is False, "epic runtime claim")
    require(subject["epic_preparation_critical_self_review_status"] == SELF_REVIEW_COMPLETE,
            "epic self-review incomplete")
    require(subject["epic_research_reuse_or_delta_status"] in {"UPDATED", "REUSED_NO_MATERIAL_DELTA"},
            "epic research status")
    require(subject["external_project_context_sync"] == "NOT_APPLICABLE", "external sync not bound")
    require(subject["open_material_user_decisions_required_before_start"] == [], "open epic decisions")
    evidence = subject["evidence_paths"]
    require(isinstance(evidence, list) and evidence, "missing epic evidence")
    for name in evidence:
        safe_path(name)
        scope(name)
        read(name)
    require(len(evidence) == len(set(evidence)), "duplicate epic evidence")
    required = {prefix + name for name in ("preparation.md", "binding.json", "evidence/research.md",
                                          "evidence/self-review.md", "evidence/preparation-authorization.json")}
    require(required <= set(evidence), "incomplete epic evidence")
    binding = parse(read(prefix + "binding.json"))
    require(binding["status"] == "REVIEW_REQUIRED", "epic binding lifecycle")
    require(binding["epic_id"] == binding["epic_preparation_subject_id"] == epic, "epic binding ID")
    for key in ("epic_preparation_id", "current_canonical_baseline_or_main_sha",
                "project_foundation_review_result_reference", "external_project_context_sync",
                "epic_research_reuse_or_delta_status", "epic_preparation_critical_self_review_status"):
        require(binding[key] == subject[key], "epic binding mismatch")
    require(binding["ready_for_agent"] is False
            and binding["epic_preparation_review_result_reference"] is None, "invented epic acceptance")
    require(binding["open_critical_blocking_major_findings"] == "NONE_AT_SELF_REVIEW__INDEPENDENT_REVIEW_PENDING",
            "independent epic review pending")
    require(binding["open_material_user_decisions_required_before_start"] == "NONE", "open binding decisions")
    for key, name in (
        ("approved_product_definition_reference", "WindowSafe_Product_Definition_WS-PD-20260917-01.md"),
        ("project_technical_foundation_reference", "WindowSafe_Technical_Foundation_WS-TFP-20260917-01_r6.md"),
    ):
        require(binding[key] == "foundation/inputs/inputs/" + name
                and binding[key] in evidence, "epic product/foundation binding")
    auth_path = prefix + "evidence/preparation-authorization.json"
    require(binding["execution_authorization_reference"] == auth_path, "epic authorization locator")
    raw = read(auth_path)
    require(sha256(raw) == PREPARATION_AUTHORIZATIONS.get(auth_path), "epic authorization hash")
    auth = parse(raw)
    require(auth["STATUS"] == "AUTHORIZED" and auth["AUTHORITY"] == "USER", "epic authorization")
    require(auth["EPIC_ID"] == epic and auth["EPIC_PREPARATION_ID"] == subject["epic_preparation_id"],
            "epic authorization ID")
    baseline = subject["current_canonical_baseline_or_main_sha"]
    require(isinstance(baseline, str) and re.fullmatch(SHA_PATTERN, baseline)
            and baseline == auth["BASELINE_MAIN_SHA"], "epic authorized baseline")
    require(commit(baseline) == baseline, "epic baseline unavailable")
    ancestor(baseline, head)
    reference = safe_path(subject["project_foundation_review_result_reference"])
    require(reference in evidence and re.fullmatch(r"reviews/results/" + ID_PATTERN + r"\.json", reference),
            "foundation result locator")
    result_raw = read(reference)
    require(result_raw == at(baseline, reference), "foundation result not in bound main")
    result = parse(result_raw)
    require(result["review_type"] == "PROJECT_FOUNDATION_REVIEW" and result["verdict"] == "PASS",
            "foundation PASS required")
    reviewed = result["subject"]["end_sha"]
    req = request(reviewed, result["subject"]["path"])
    semantic = None
    try:
        semantic = parse(read("reviews/dispositions/" + PurePosixPath(reference).name))
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    validate_result(result, req, parse(at(reviewed, CONTRACT_PATH)), PurePosixPath(reference).name,
                    semantic, sha256(result_raw))
    ancestor(reviewed, baseline)
    return baseline, reviewed, reference


def accepted_epic_binding(path, read, head):
    """Consume an authorized PASS; preserve the original preparation and verdict."""
    binding_path = path.replace("subject.json", "binding.json")
    binding = parse(read(binding_path))
    auth_path = safe_path(binding["execution_authorization_reference"])
    raw = read(auth_path)
    require(sha256(raw) == INTEGRATION_AUTHORIZATIONS.get(auth_path), "integration authorization hash")
    auth = parse(raw)
    require(auth["STATUS"] == "AUTHORIZED" and auth["AUTHORITY"] == "USER", "integration authorization")
    reviewed = auth["EXPECTED_BRANCH_HEAD"]
    require(isinstance(reviewed, str) and re.fullmatch(SHA_PATTERN, reviewed), "reviewed epic SHA")
    ancestor(reviewed, head)
    original = parse(at(reviewed, binding_path))
    require(original["status"] == "REVIEW_REQUIRED", "acceptance requires pending original")
    require(read(path) == at(reviewed, path), "immutable epic subject drift")
    baseline = original["current_canonical_baseline_or_main_sha"]
    require(baseline == auth["EXPECTED_MAIN_SHA"], "integration baseline mismatch")
    req = request(reviewed, path)
    reference = "reviews/results/" + auth["REVIEW_ID"] + ".json"
    safe_path(reference)
    result_raw = read(reference)
    exact = auth["EXACT_RESULT_BINDING"]
    require(len(result_raw) == exact["bytes"] and sha256(result_raw) == exact["sha256"],
            "integration original result mismatch")
    result = parse(result_raw)
    validate_result(result, req, parse(at(reviewed, CONTRACT_PATH)), PurePosixPath(reference).name)
    require(result["verdict"] == "PASS" and result["review_type"] == "EPIC_PREPARATION_REVIEW",
            "epic PASS required")
    follow_up = safe_path(binding["nonblocking_follow_up_reference"])
    require(follow_up in INTEGRATION_SUPPORT_PATHS and follow_up.endswith(".md"), "follow-up locator")
    text(read(follow_up).decode())
    expected = dict(original,
        status="READY_FOR_AGENT", ready_for_agent=True,
        epic_preparation_subject_immutable_reference=req["subject"],
        epic_preparation_review_result_reference=reference,
        open_critical_blocking_major_findings="NONE",
        execution_authorization_reference=auth_path,
        open_nonblocking_finding_ids=[item["id"] for item in result["findings"] if item["status"] == "OPEN"],
        nonblocking_follow_up_reference=follow_up,
        execution_scope="PREPARATION_INTEGRATION_ONLY__NO_FEATURE_EXECUTION")
    require(binding == expected and binding["ready_for_agent"] is True, "accepted binding mismatch")
    prefix = path.rsplit("/", 1)[0] + "/"
    for name in parse(at(reviewed, path))["evidence_paths"]:
        if name.startswith(prefix) and name != binding_path:
            require(read(name) == at(reviewed, name), "immutable preparation evidence drift")
    allowed = INTEGRATION_SUPPORT_PATHS | {binding_path, auth_path, reference}
    require(set(git("diff", "--name-only", reviewed, head).decode().splitlines()) <= allowed,
            "post-review integration scope")
    return reviewed


def epic_subject_paths(paths):
    """Each materialized epic must have exactly its canonical subject."""
    paths = set(paths)
    epics = {p.split("/")[1] for p in paths if p.startswith("epics/") and len(p.split("/")) > 2}
    subjects = sorted("epics/" + epic + "/subject.json" for epic in epics)
    require(set(subjects) <= paths, "orphan epic preparation")
    return subjects


def check(root=ROOT):
    require(sys.version_info[:3] == (3, 14, 4), "Python 3.14.4 required")
    input_integrity(root)
    for path, digest in (CORRECTION_INPUTS | FOLLOWUP_INPUTS).items():
        require(sha256((root / path).read_bytes()) == digest, "correction input drift")
    validate_contract(parse((root / CONTRACT_PATH).read_bytes()))
    subject = parse((root / "foundation/subject.json").read_bytes())
    require(subject["product_features_started"] is False and subject["epic_started"] is False, "product start prohibited")
    require(subject["status"] == "PROJECT_FOUNDATION_READY_FOR_REVIEW", "foundation lifecycle drift")
    require(subject["independent_review_status"] == "PENDING", "self acceptance prohibited")
    require(subject["platform_qualification"] == subject["performance_method_binding"] == "REQUIRED_BEFORE_AFFECTED_PRODUCT_IMPLEMENTATION", "preimplementation gate drift")
    require(subject["runtime_evidence"] == "NOT_EXECUTED", "runtime claim drift")
    epic_paths = epic_subject_paths(p.relative_to(root).as_posix() for p in files(root))
    for path in epic_paths:
        epic_preparation(path, lambda name: (root / name).read_bytes(), commit("HEAD"))
    for path in files(root):
        rel = path.relative_to(root).as_posix()
        scope(rel)
        data = path.read_bytes()
        content = data.decode("utf-8")
        if path.suffix == ".json":
            parse(data)
        if rel.startswith(("foundation/inputs/", "foundation/sources/")) or rel in FOLLOWUP_INPUTS:
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
            disposition = root / "reviews/dispositions" / path.name
            validate_result_file(path, disposition if disposition.exists() else None)
        if rel.startswith("reviews/dispositions/"):
            require((root / "reviews/results" / path.name).is_file(), "orphan semantic disposition")
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
    if epic_paths:
        require("ref: ${{ github.event.pull_request.head.sha || github.sha }}" in workflow, "CI exact head required")
        require("foundation.py schema-preflight --sha HEAD --schema reviews/review-contract.json" in workflow,
                "missing current schema preflight")
        for path in epic_paths:
            require("foundation.py request --sha HEAD --subject " + path in workflow, "missing epic CI request")
    if root == ROOT and (root / ".git").exists():
        # Ignored build/cache directories cannot hide tracked out-of-scope files.
        for name in git("ls-files", "--cached", "-z").split(b"\0"):
            if name:
                scope(name.decode())


def build_bytes(root):
    inventory = [{"path": p.relative_to(root).as_posix(), "sha256": sha256(p.read_bytes()), "bytes": p.stat().st_size} for p in files(root)]
    return (json.dumps({"artifact": "FOUNDATION_INVENTORY_NOT_ADDON", "files": inventory}, indent=2) + "\n").encode()


def write_inventory(root, data):
    """No-follow, descriptor-relative writer for qualified POSIX environments.

    Never unlinks/replaces a preexisting link. The output is regenerable, not an
    atomic/durable store. Hostile mutation of opened inode ancestry is outside
    the trusted local workspace model; no Windows/reparse-point claim is made.
    """
    require(os.name == "posix" and os.open in os.supports_dir_fd
            and os.mkdir in os.supports_dir_fd
            and all(hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK")),
            "qualified no-follow writer unavailable")
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    root_fd = os.open(root, directory_flags)
    try:
        try:
            os.mkdir("build", mode=0o700, dir_fd=root_fd)
        except FileExistsError:
            pass  # The following open, not this observation, enforces no-follow.
        directory_fd = os.open("build", directory_flags, dir_fd=root_fd)
        try:
            flags = os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK
            output_fd = os.open("foundation-inventory.json", flags, 0o600, dir_fd=directory_fd)
            try:
                info = os.fstat(output_fd)
                require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "output must be a single-link regular file")
                # No path lookup after validation; do not truncate before fstat.
                os.ftruncate(output_fd, 0)
                remaining = memoryview(data)
                while remaining:
                    written = os.write(output_fd, remaining)
                    require(written > 0, "output write made no progress")
                    remaining = remaining[written:]
            finally:
                os.close(output_fd)
        finally:
            os.close(directory_fd)
    finally:
        os.close(root_fd)


def protected(path):
    return path.startswith(("foundation/inputs/", "foundation/sources/", "foundation/evidence/", "reviews/results/", "reviews/dispositions/")) or bool(re.fullmatch(r"epics/" + ID_PATTERN + r"/.+", path))


def check_history_maps(before, after, transitions=None):
    for path, value in before.items():
        if protected(path):
            if transitions and path in transitions and after.get(path) != value:
                old, new, required = transitions[path]
                require(value == old and after.get(path) == new
                        and all(after.get(p) == data for p, data in required.items()),
                        "unauthorized binding history transition")
                continue
            require(path in after and after[path] == value, "append-only history violated")


def ancestor(base, head):
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", base, head], check=True, capture_output=True)


def history_binding(head):
    # Anchor is the separately user-authorized original, hash-pinned independently
    # of the current subject. Changing the subject cannot select a comparison base.
    try:
        raw = at(head, FOLLOWUP_AUTH)
    except subprocess.SubprocessError as error:
        raise Invalid("missing history authorization") from error
    require(sha256(raw) == FOLLOWUP_INPUTS[FOLLOWUP_AUTH], "history authorization hash mismatch")
    require((ROOT / FOLLOWUP_AUTH).read_bytes() == raw, "worktree authorization drift")
    binding = parse(raw)["repository_binding"]
    cumulative = binding["cumulative_review_and_history_base_sha"]
    run_start = binding["run_start_head_sha"]
    require(binding["expected_main_sha"] == cumulative, "authorization baseline conflict")
    for value, tree in ((cumulative, binding["cumulative_base_tree_sha"]), (run_start, binding["run_start_tree_sha"])):
        require(re.fullmatch(SHA_PATTERN, value) and commit(value) == value, "bound commit unavailable")
        require(git("rev-parse", value + "^{tree}").decode().strip() == tree, "bound tree mismatch")
        require(value != head, "history self comparison")
        ancestor(value, head)
    ancestor(cumulative, run_start)
    subject_raw = at(head, "foundation/subject.json")
    require((ROOT / "foundation/subject.json").read_bytes() == subject_raw, "uncommitted history declaration")
    subject = parse(subject_raw)
    require(subject["start_baseline_sha"] == subject["cumulative_review_and_history_base_sha"] == cumulative,
            "cumulative history declaration mismatch")
    require(subject["run_start_head_sha"] == run_start, "run history declaration mismatch")
    require(subject["execution_authorization_path"] == FOLLOWUP_AUTH
            and subject["execution_authorization_sha256"] == sha256(raw), "subject authorization mismatch")
    return cumulative, run_start


def history_snapshot(base):
    before = {}
    for entry in git("ls-tree", "-rz", "--full-tree", base).split(b"\0"):
        if not entry:
            continue
        _metadata, name = entry.split(b"\t", 1)
        path = name.decode()
        if protected(path):
            before[path] = at(base, path)
    return before


def compare_history(base, transitions=None):
    after = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in files(ROOT)}
    check_history_maps(history_snapshot(base), after, transitions)


def accepted_binding_transitions(head):
    transitions = {}
    paths = git("ls-tree", "-r", "--name-only", head, "--", "epics").decode().splitlines()
    for path in epic_subject_paths(paths):
        binding_path = path.replace("subject.json", "binding.json")
        raw = at(head, binding_path)
        binding = parse(raw)
        if binding["status"] == "READY_FOR_AGENT":
            reviewed = accepted_epic_binding(path, lambda name: at(head, name), head)
            required = {name: at(head, name) for name in (
                path, binding["execution_authorization_reference"],
                binding["epic_preparation_review_result_reference"])}
            transitions[binding_path] = (at(reviewed, binding_path), raw, required)
    return transitions


def preparation_integration(head, cumulative):
    """Recognize only the explicitly authorized Foundation/Epic normal merges.

    The old cumulative/run anchors and every pre-merge commit remain checked.
    No subject-supplied SHA may exempt arbitrary merges or shorten history.
    """
    paths = git("ls-tree", "-r", "--name-only", head, "--", "epics").decode().splitlines()
    integrations = set()
    for path in epic_subject_paths(paths):
        baseline, reviewed, reference = epic_preparation(path, lambda name: at(head, name), head)
        for name in (path, path.replace("subject.json", "binding.json"),
                     path.replace("subject.json", "evidence/preparation-authorization.json")):
            require((ROOT / name).read_bytes() == at(head, name), "uncommitted preparation binding")
        require(baseline != head, "preparation requires post-baseline commit")
        parents = git("rev-list", "--parents", "-n", "1", baseline).decode().split()[1:]
        require(len(parents) == 2 and parents[0] == cumulative, "authorized normal integration required")
        ancestor(reviewed, parents[1])
        require(git("rev-parse", baseline + "^{tree}") == git("rev-parse", parents[1] + "^{tree}"),
                "integration tree drift")
        require(git("diff", "--name-status", reviewed, parents[1]).decode().splitlines() == ["A\t" + reference],
                "foundation transfer-only delta required")
        integrations.add(baseline)
        binding = parse(at(head, path.replace("subject.json", "binding.json")))
        if binding["status"] == "READY_FOR_AGENT":
            epic_reviewed = binding["epic_preparation_subject_immutable_reference"]["end_sha"]
            for merge in git("rev-list", "--min-parents=2", epic_reviewed + ".." + head).decode().splitlines():
                parents = git("rev-list", "--parents", "-n", "1", merge).decode().split()[1:]
                require(len(parents) == 2 and parents[0] == baseline, "authorized epic normal merge required")
                ancestor(epic_reviewed, parents[1])
                require(at(parents[1], path.replace("subject.json", "binding.json"))
                        == at(head, path.replace("subject.json", "binding.json")), "merge acceptance mismatch")
                require(git("rev-parse", merge + "^{tree}") == git("rev-parse", parents[1] + "^{tree}"),
                        "epic integration tree drift")
                integrations.add(merge)
    baselines = {parse(at(head, path))["current_canonical_baseline_or_main_sha"]
                 for path in epic_subject_paths(paths)}
    require(len(baselines) <= 1, "conflicting preparation baselines")
    return integrations


def history(base):
    head = commit("HEAD")
    no_base = not base or base == "0" * 40
    # Structural root check, not a fixed count of historical reviews or commits.
    is_root = len(git("rev-list", "--parents", "-n", "1", head).split()) == 1
    if is_root:
        require(no_base, "root must have no history base")
        return
    cumulative, run_start = history_binding(head)
    integrations = preparation_integration(head, cumulative)
    transitions = accepted_binding_transitions(head)
    bases = {cumulative, run_start}
    if not no_base:
        require(re.fullmatch(SHA_PATTERN, base), "full event base required")
        base = commit(base)
        require(base != head, "history self comparison")
        ancestor(base, head)
        if base not in bases:
            ancestor(run_start, base)  # No arbitrary ancestor between cumulative and run start.
        bases.add(base)
    else:
        require(base == "0" * 40, "missing event binding")
    for comparison in sorted(bases):
        compare_history(comparison, transitions)
    # Also protect results introduced within the unaccepted delta, including
    # changes later reverted. Endpoint comparisons alone would hide those edits.
    previous = history_snapshot(cumulative)
    for revision in git("rev-list", "--reverse", cumulative + ".." + head).decode().splitlines():
        require(revision in integrations or len(git("rev-list", "--parents", "-n", "1", revision).split()) == 2,
                "unaccepted history must be linear")
        current = history_snapshot(revision)
        check_history_maps(previous, current, transitions)
        previous = current
    check_history_maps(previous, {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in files(ROOT)}, transitions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "build", "request", "schema-preflight", "validate-result", "history"])
    parser.add_argument("--sha", default="HEAD")
    parser.add_argument("--subject", default="foundation/subject.json")
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--semantic-disposition", type=Path)
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
        write_inventory(ROOT, result)
        print("FOUNDATION_INVENTORY_SHA256", sha256(result))
    elif args.command == "request":
        print(json.dumps(request(args.sha, args.subject), indent=2))
        return
    elif args.command == "schema-preflight":
        require(args.schema is not None, "external schema required")
        schema_preflight(parse(at(commit(args.sha), CONTRACT_PATH)), parse(args.schema.read_bytes()))
    elif args.command == "validate-result":
        require(args.file is not None, "result file required")
        validate_result_file(args.file, args.semantic_disposition)
    elif args.command == "history":
        base = os.environ.get("FOUNDATION_EVENT_BASE") if args.event_base else args.base
        require(args.event_base or args.base is not None, "explicit history baseline required")
        history(base)
    print(args.command.upper() + " OK (mechanical evidence only)")


if __name__ == "__main__":
    try:
        main()
    except SemanticDispositionRequired:
        print("V1_SEMANTIC_DISPOSITION_REQUIRED: independent original-bound disposition missing", file=sys.stderr)
        sys.exit(1)
    except (Invalid, KeyError, TypeError, ValueError, OSError, subprocess.SubprocessError):
        print("FOUNDATION_GATE_FAILED: invalid input, binding, environment or history", file=sys.stderr)
        sys.exit(1)
