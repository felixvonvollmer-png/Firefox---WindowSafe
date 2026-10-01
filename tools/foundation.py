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
DELTA_ID = "WS-PFDELTA-MAT-20260928-01"
DELTA_BASE = "3bdd7439c221b8f8c83e7374c8bb29898891a4fd"
DELTA_INPUTS = "foundation/inputs/" + DELTA_ID + "/"
DELTA_SUBJECT = "foundation/deltas/" + DELTA_ID + "/subject.json"
DELTA_EVIDENCE = "foundation/deltas/" + DELTA_ID + "/evidence.md"
DELTA_AUTH = DELTA_INPUTS + "WindowSafe_Execution_Authorization_WS-EA-20260928-01.json"
DELTA_MANIFEST_SHA = "bf6a4832c52860a136090790e3ec973b7a6536546a30dcc54711e0f09f69d757"
DELTA_AUTH_SHA = "677c3eb9933cb0f6b3313253fff7f9457f0c342bf0e30ea70fc04f5bfc83e2c4"
DELTA_SOURCES = {
    "foundation/sources/v6-final-20260918/README.md": "c9c0a47d108268059ca5b5825d2d445b44179775",
    "foundation/sources/v6-final-20260918/foundation-1.md": "0c10e10eebcb2b23336cc9cdf4a88305a209fd22",
    "foundation/sources/v6-final-20260918/foundation-2.md": "3034da0fbee6ab79318da25ed65ccdc0933074e5",
}
DELTA_SUPPORT = {
    "AGENTS.md", "README.md", "foundation/context.md", "foundation/architecture.md",
    "reviews/README.md", "epics/README.md", "tools/foundation.py",
    "tests/test_foundation.py", "tests/test_foundation_delta.py", ".github/workflows/foundation.yml",
}
# Separate acceptance state; the reviewed delta subject itself stays immutable.
DELTA_BINDING = "foundation/deltas/" + DELTA_ID + "/binding.json"
DELTA_INTEGRATION_AUTH = "foundation/evidence/pf-delta-integration-authorization.json"
DELTA_INTEGRATION_AUTH_SHA = "ca04feb83e3d2053615f7836e8c79cb5909ab98ab6449b24cab3230ac5a965f1"
DELTA_NEXT_GATE = "REQUIRED_EXTERNAL_REVIEW_BOOTSTRAP_INSTALL_SYNC_OR_NOT_APPLICABLE"
# Exactly one versioned WS-E01 preparation delta after the integrated foundation merge.
EPIC_DELTA_ID = "WS-E01-EP-DELTA-20260929-02"
EPIC_DELTA_BASE = "1cb82c926903b2fd6b497d008db61c71c5d92aca"
EPIC_DELTA_DIR = "epics/WS-E01/deltas/" + EPIC_DELTA_ID + "/"
EPIC_DELTA_SUBJECT = EPIC_DELTA_DIR + "subject.json"
EPIC_DELTA_BINDING = EPIC_DELTA_DIR + "binding.json"
EPIC_DELTA_EVIDENCE = EPIC_DELTA_DIR + "evidence.md"
EPIC_DELTA_AUTH = EPIC_DELTA_DIR + "execution-authorization.json"
EPIC_DELTA_AUTH_SHA = "68ff10124c40995b8740dbbe4ca6e8dfaaac9bab6f33335980dd4588968728ab"
# Exact Project-LLM originals and user authorization: materialized path -> (bytes, SHA-256).
EPIC_DELTA_ORIGINALS = {
    EPIC_DELTA_DIR + "preparation.md": (13661, "ddd12e52b98790a19d57040da82d8ffeec42184f317d19eff87200c86a0d2115"),
    EPIC_DELTA_DIR + "critical-self-review.md": (2872, "12d1d400030077da93220cf792f40bf69949ac8106d33e92e36d52b0320fe765"),
    EPIC_DELTA_DIR + "execution-direction.json": (1012, "5b4f467e2e98a14f36eceec65ca667ee4cafe594a5a81a2a40fc5dc2d186a2de"),
    EPIC_DELTA_DIR + "external-context-sync.json": (1499, "d4bdc815e281f083acd6222d1ff19dc4255e05d2a52038d42bb360b5c61f2062"),
    EPIC_DELTA_DIR + "project-description.md": (7607, "647d8fcffff3c55b8e32f33f0cb80e22591bea77835817db87a96659f52f4ba5"),
    EPIC_DELTA_DIR + "previous-preparation-delta.md": (10859, "e848043bd6cdf8c28e3b9eff72e97ec5c738567a26e5705dfb9851cb65cc074f"),
    EPIC_DELTA_AUTH: (6930, EPIC_DELTA_AUTH_SHA),
}
EPIC_DELTA_FILES = set(EPIC_DELTA_ORIGINALS) | {EPIC_DELTA_SUBJECT, EPIC_DELTA_BINDING, EPIC_DELTA_EVIDENCE}
# Git blobs that must stay exactly as integrated on EPIC_DELTA_BASE.
EPIC_DELTA_PINNED_BLOBS = {
    "epics/WS-E01/preparation.md": "a92fbe87a9640b67367db96631e082864b89e9b3",
    "epics/WS-E01/subject.json": "f12b4756046febfec07b0426a0129bce482ce2d2",
    "epics/WS-E01/binding.json": "930b4c3176a9601e44f7a4b04ff1d4530488b6e1",
    DELTA_BINDING: "8a85ff8481a6bd831b3e2ace3382404762476834",
    "reviews/results/WS-PFR-DELTA-20260928-01.json": "ff96f8b1cac7d9a664339c7df55ddbf77947e3a8",
    DELTA_INPUTS + "WindowSafe_Product_Definition_Delta_WS-PD-DELTA-20260924-01.md":
        "c8d52f1720aa24544b0d24f652e6b9c8d14254ec",
    DELTA_INPUTS + "WindowSafe_Technical_Foundation_Delta_Preparation_WS-TFP-DELTA-20260928-02.md":
        "539dd9d35d40b832c07a779e351e7964af9f8705",
}
EPIC_DELTA_SUPPORT = {
    "AGENTS.md", "README.md", "foundation/context.md", "foundation/engineering.md",
    "reviews/README.md", "epics/README.md", "tools/foundation.py",
    "tests/test_epic_delta.py", ".github/workflows/foundation.yml",
}
F01_EVIDENCE = {"pr": 3, "head": "7d66ca5b025c8f748d7f97b961c496ee450daaa7",
                "role": "READ_ONLY_EXTERNAL_QUALIFICATION_EVIDENCE"}
# The CORRECTION_REQUIRED head of that delta and exactly one bound correction of it.
EPIC_DELTA_REVIEWED = "48d7b0f97eacecd7515f7cbf064955303b0d5767"
EPIC_DELTA_REVIEWED_TREE = "3393b5c6de0dd0c11988b702ca602698f736e290"
EPIC_DELTA_REVIEW_ID = "WS-E01-EPR-DELTA-20260929-01"
EPIC_DELTA_RESULT = "reviews/results/" + EPIC_DELTA_REVIEW_ID + ".json"
EPIC_DELTA_RESULT_ORIGINAL = (13760, "e438cc1fba49bc472e78adbf4b12aa9475e24c2dac0cd187c8a29c5682f16048")
EPIC_CORR_ID = "WS-E01-EP-DELTA-20260929-03"
EPIC_CORR_DIR = "epics/WS-E01/deltas/" + EPIC_CORR_ID + "/"
EPIC_CORR_SUBJECT = EPIC_CORR_DIR + "subject.json"
EPIC_CORR_BINDING = EPIC_CORR_DIR + "binding.json"
EPIC_CORR_EVIDENCE = EPIC_CORR_DIR + "evidence.md"
EPIC_CORR_AUTH = EPIC_CORR_DIR + "execution-authorization.json"
EPIC_CORR_AUTH_SHA = "1672b45700ffc5b4aa1846521e2faf1af06b2334d759f6eeb30af22ed06d16ef"
EPIC_CORR_ORIGINALS = {
    EPIC_CORR_DIR + "correction.md": (8551, "aee88ae816f85489982176fba0089e3555f0cab95585a5f55152d6050e977b3e"),
    EPIC_CORR_DIR + "correction-disposition.json":
        (2385, "9f268ea37fc7716fe2ed4ea8a8270adb780235a376961279f08271989767c1aa"),
    EPIC_CORR_DIR + "correction-critical-self-review.md":
        (1945, "30254913d37577f5766e95904d17738c05d69006af76b939ec2e9d549fad0692"),
    EPIC_CORR_AUTH: (7254, EPIC_CORR_AUTH_SHA),
}
EPIC_CORR_FILES = set(EPIC_CORR_ORIGINALS) | {EPIC_CORR_SUBJECT, EPIC_CORR_BINDING, EPIC_CORR_EVIDENCE}
# Every author of the cumulative corrected subject; none may issue its verdict.
EPIC_CORR_EXCLUDED = [
    "PROJECT_LLM_WS_E01_EP_DELTA_20260929_03",
    "CODING_AGENT_WS_E01_EPDELTA_MAT_20260929_01",
    "CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_01",
]
# Sources the correction run had to read before its first write; bound as review evidence.
EPIC_CORR_PREWRITE = dict({"foundation/architecture.md": "923c8e5820067376f3ea6660bf0307e7bfaa9d6a"},
                          **DELTA_SOURCES)
EPIC_CORR_SUPPORT = EPIC_DELTA_SUPPORT | {"tests/test_epic_correction.py"}
EPIC_CORR_ALLOWED = EPIC_CORR_FILES | EPIC_CORR_SUPPORT | {EPIC_DELTA_RESULT}
# The reviewed head of -03 and exactly one further correction (-04) of it.
EPIC_CORR_REVIEWED = "dee7ab5c9c5b53accd8602105e87523510582e40"
EPIC_CORR_REVIEWED_TREE = "a62713f6d34c054d3064d0d6d999fbcc9cd694d3"
# Results for -03@EPIC_CORR_REVIEWED: historical BLOCKED original and the user-authorized
# replacement for the lost CORRECTION_REQUIRED original; path -> (bytes, SHA-256, verdict).
EPIC_CORR_RESULTS = {
    "reviews/results/WS-E01-EPR-DELTA-20260929-02.json":
        (14361, "dd3cc14785f67107a642328b5644fa5a4a7e02ea89834f9c8e731408fae1dfa8", "BLOCKED"),
    "reviews/results/WS-E01-EPR-DELTA-20260930-04.json":
        (14038, "3096a1fe1333ed89fa8c3e6e588e3a14f38f25157e4fb886afe412726e7649cf", "CORRECTION_REQUIRED"),
}
EPIC_CORR2_ID = "WS-E01-EP-DELTA-20260929-04"
EPIC_CORR2_DIR = "epics/WS-E01/deltas/" + EPIC_CORR2_ID + "/"
EPIC_CORR2_SUBJECT = EPIC_CORR2_DIR + "subject.json"
EPIC_CORR2_BINDING = EPIC_CORR2_DIR + "binding.json"
EPIC_CORR2_EVIDENCE = EPIC_CORR2_DIR + "evidence.md"
EPIC_CORR2_AUTH = EPIC_CORR2_DIR + "execution-authorization.json"
EPIC_CORR2_AUTH_SHA = "638b3ab5cb4bc91d55eda0d530b695470d16adda612943d14f75bf337a85a621"
EPIC_CORR2_FILES = {EPIC_CORR2_SUBJECT, EPIC_CORR2_BINDING, EPIC_CORR2_EVIDENCE, EPIC_CORR2_AUTH}
# Minimum named by the user; the lineage closure below decides what is required.
EPIC_CORR2_MINIMUM_EXCLUDED = [
    "PROJECT_LLM_WS_E01_PREPARATION_20260919_01",
    "PROJECT_LLM_WS_E01_EP_DELTA_20260929_02",
    "PROJECT_LLM_WS_E01_EP_DELTA_20260929_03",
    "PROJECT_LLM_WS_E01_EP_DELTA_20260929_04",
    "CODING_AGENT_WS_E01_EPDELTA_MAT_20260929_01",
    "CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_01",
    "CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_02",
]
EPIC_CORR2_SUPPORT = EPIC_CORR_SUPPORT | {"tests/test_epic_lineage.py"}
EPIC_CORR2_ALLOWED = EPIC_CORR2_FILES | EPIC_CORR2_SUPPORT | set(EPIC_CORR_RESULTS)
# Subjects whose request must satisfy the mechanical lineage closure (historical ones keep their semantics).
LINEAGE_CLOSURE_SUBJECTS = {EPIC_CORR2_SUBJECT}
AUTHOR_FIELDS = ("implementer", "materializer")
# Exact epic rebinding of -04 after its independent PASS, plus one normal PR #5 merge into main.
EPIC_CORR2_REVIEWED = "fa109e1b2cea025918d1cff61a2aaee2ee2b2083"
EPIC_CORR2_REVIEWED_TREE = "58883dc1db31f8d3f5aecbfb41564508c1f53aed"
EPIC_REBIND_RESULT = "reviews/results/WS-E01-EPR-DELTA-20260930-05.json"
EPIC_REBIND_RESULT_ORIGINAL = (20849, "222a82f0bd4573d93eef05515276cbfbbd081b3baaeb699d9b3987045e7b427b")
EPIC_REBINDING = EPIC_CORR2_DIR + "rebinding.json"
EPIC_REBIND_AUTH = EPIC_CORR2_DIR + "integration-authorization.json"
EPIC_REBIND_AUTH_SHA = "012bfd8e3267664719a92f8c31d996805219f287f9345b8cc02d53a17b58d7d2"
EPIC_REBIND_FILES = {EPIC_REBINDING, EPIC_REBIND_AUTH, EPIC_REBIND_RESULT}
EPIC_REBIND_SUPPORT = EPIC_CORR2_SUPPORT | {"tests/test_epic_rebinding.py"}
EPIC_REBIND_ALLOWED = EPIC_REBIND_FILES | EPIC_REBIND_SUPPORT
# The single normal merge that integrated the rebound epic into main.
EPIC_INTEGRATION_MERGE = "714b440c26167f6411420fbbda4be69deb2e9670"
# Separate broad WS-E01 execution authorization; active only after the integration merge.
EPIC_EXECUTION_AUTH = "epics/WS-E01/evidence/broad-execution-authorization.json"
EPIC_EXECUTION_AUTH_SHA = "cced59563b38d5356097ecc2f1efe3da385897023b8ac323882c0d3c5761db6d"
# Never editable during feature execution (new files in other protected areas stay append-only).
EXECUTION_FROZEN_PREFIXES = ("foundation/inputs/", "foundation/sources/", "foundation/deltas/",
                             "foundation/evidence/", "epics/WS-E01/deltas/", "reviews/review-contract.json")
FEATURE_ID_PATTERN = r"WS-E01-F0[1-5]"
EPIC_VERSIONED_SUBJECTS = (EPIC_DELTA_SUBJECT, EPIC_CORR_SUBJECT, EPIC_CORR2_SUBJECT)
# Superseded locator -> (superseding subject, reviewed head it stays bound to).
EPIC_SUPERSEDED_AT = {
    EPIC_DELTA_SUBJECT: (EPIC_CORR_SUBJECT, EPIC_DELTA_REVIEWED),
    EPIC_CORR_SUBJECT: (EPIC_CORR2_SUBJECT, EPIC_CORR_REVIEWED),
    # Accepted, not superseded: the rebound locator still requests the reviewed bytes.
    EPIC_CORR2_SUBJECT: (EPIC_REBINDING, EPIC_CORR2_REVIEWED),
}
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
    if kind == "PROJECT_FOUNDATION_REVIEW" and path == DELTA_SUBJECT:
        reviewed = delta_history(sha)
        if reviewed != sha:
            # A current accepted locator still requests the original reviewed bytes.
            return request(reviewed, path)
    elif kind == "EPIC_PREPARATION_REVIEW" and path in EPIC_VERSIONED_SUBJECTS:
        # Only these exact versioned locators; they also revalidate foundation acceptance.
        delta_history(sha)
        superseded = EPIC_SUPERSEDED_AT.get(path)
        if superseded and superseded[0] in tree_snapshot(sha):
            # A superseded reviewed subject stays bound to its reviewed bytes.
            return request(superseded[1], path)
    else:
        require(path == expected, "subject locator mismatch")
        if kind == "FEATURE_ACCEPTANCE_REVIEW":
            require(re.fullmatch(FEATURE_ID_PATTERN, s["subject_id"]) and EPIC_EXECUTION_AUTH in tree_snapshot(sha),
                    "feature review requires bound WS-E01 execution")
            delta_history(sha)  # Revalidates foundation, epic rebinding and the execution history.
    text(s["implementer"])
    if kind == "FEATURE_ACCEPTANCE_REVIEW":
        # Every author of the feature changeset, including workers, is excluded from its verdict.
        authors = [s["implementer"], *([s["materializer"]] if "materializer" in s else []),
                   *s.get("contributors", [])]
        excluded = s.get("review_excluded_identities")
        require(isinstance(excluded, list) and all(isinstance(v, str) and v.strip() for v in excluded)
                and all(isinstance(v, str) and v.strip() for v in authors)
                and {v.strip().casefold() for v in authors} <= {v.strip().casefold() for v in excluded},
                "REQUEST_INVALID: feature author exclusion incomplete")
    elif path not in (EPIC_CORR_SUBJECT, EPIC_CORR2_SUBJECT):
        require("review_excluded_identities" not in s, "unbound review exclusion set")
    if path in LINEAGE_CLOSURE_SUBJECTS:
        # Fail closed if any author/materializer of the reviewed lineage is not excluded.
        derived = review_exclusion_closure(lambda name: at(sha, name), path)
        excluded = s["review_excluded_identities"]
        require(isinstance(excluded, list) and all(isinstance(v, str) and v.strip() for v in excluded)
                and len({v.strip().casefold() for v in excluded}) == len(excluded), "review exclusion set")
        require({v.casefold() for v in derived} <= {v.strip().casefold() for v in excluded},
                "REQUEST_INVALID: review exclusion closure incomplete")
    require(isinstance(s["evidence_paths"], list) and s["evidence_paths"], "missing subject evidence")
    require(len(s["evidence_paths"]) == len(set(s["evidence_paths"])), "duplicate evidence")
    if kind == "EPIC_PREPARATION_REVIEW" and path not in EPIC_VERSIONED_SUBJECTS:
        epic_preparation(path, lambda name: at(sha, name), sha)
        binding = parse(at(sha, path.replace("subject.json", "binding.json")))
        if binding["status"] == "READY_FOR_AGENT":
            # A current accepted locator still requests the original reviewed bytes.
            return request(binding["epic_preparation_subject_immutable_reference"]["end_sha"], path)
    evidence = [{"path": safe_path(p), "sha256": sha256(at(sha, p))} for p in s["evidence_paths"]]
    req = {
        "schema_version": c["contract_version"],
        "review_type": kind,
        "subject": {"id": s["subject_id"], "path": path, "end_sha": sha},
        "implementer": s["implementer"], "required_authority": c["authorities"][kind],
        "reviewed_evidence": evidence,
        "contract_sha256": sha256(at(sha, CONTRACT_PATH)),
    }
    if path in (EPIC_CORR_SUBJECT, EPIC_CORR2_SUBJECT) or kind == "FEATURE_ACCEPTANCE_REVIEW":
        # Validated by the correction integrity inside delta_history or the feature check above.
        req["review_excluded_identities"] = s["review_excluded_identities"]
    return req


def lineage_owner(read, path):
    """The epic preparation subject owning a referenced epic path, if any."""
    if not isinstance(path, str) or not path.startswith("epics/"):
        return None
    parts = PurePosixPath(safe_path(path)).parts
    for depth in range(len(parts) - 1, 1, -1):
        candidate = "/".join(parts[:depth]) + "/subject.json"
        try:
            subject = parse(read(candidate))
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
        require(subject.get("review_type") == "EPIC_PREPARATION_REVIEW", "lineage owner type")
        return candidate
    raise Invalid("lineage reference without owning subject")


def semantic_references(value):
    """All string values of a subject except its evidence list (inputs are not authorship)."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key != "evidence_paths":
                yield from semantic_references(item)
    elif isinstance(value, list):
        for item in value:
            yield from semantic_references(item)
    elif isinstance(value, str):
        yield value


def review_exclusion_closure(read, path):
    """Transitive authors/materializers of the reviewed preparation/correction/supersession lineage.

    Follows every semantic reference into an epic namespace to its owning subject,
    and includes each lineage subject's recorded authors and each predecessor's bound exclusion set.
    Product/foundation/review inputs are not lineage; no cardinality is assumed.
    """
    identities, seen, pending = set(), set(), [path]
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        subject = parse(read(current))
        for key in AUTHOR_FIELDS:
            if key in subject:
                text(subject[key])
                identities.add(subject[key].strip())
        # The reviewed subject's own set is what is being checked, never a source of truth.
        for value in subject.get("review_excluded_identities", []) if current != path else []:
            text(value)
            identities.add(value.strip())
        for reference in semantic_references(subject):
            owner = lineage_owner(read, reference)
            if owner and owner not in seen:
                pending.append(owner)
    require(identities, "empty review exclusion closure")
    return identities


def self_verdict(identity, req):
    """Historical requests exclude the implementer; a bound set excludes every listed author."""
    if "review_excluded_identities" not in req:
        return identity.casefold() == req["implementer"].casefold()
    excluded = req["review_excluded_identities"]
    require(isinstance(excluded, list) and excluded and req["implementer"] in excluded
            and all(isinstance(value, str) and value.strip() for value in excluded), "review exclusion set")
    return identity.strip().casefold() in {value.strip().casefold() for value in excluded}


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
    require(not self_verdict(r["identity"], req), "self verdict prohibited")
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
    require(not self_verdict(reviewer["identity"], req), "semantic self disposition")
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
    actual = {p.relative_to(base).as_posix() for p in base.rglob("*")
              if p.is_file() and not p.relative_to(base).as_posix().startswith(DELTA_ID + "/")}
    require(expected == actual, "input inventory mismatch")
    if any((root / name).exists() for name in (DELTA_INPUTS, DELTA_SUBJECT, *DELTA_SOURCES)):
        delta_integrity(lambda name: (root / name).read_bytes())
        expected_delta = set(parse((root / (DELTA_INPUTS + "SHA256SUMS.json")).read_bytes())["FILES"])
        actual_delta = {p.relative_to(root / DELTA_INPUTS).as_posix()
                        for p in (root / DELTA_INPUTS).rglob("*") if p.is_file()}
        require(actual_delta == expected_delta | {"SHA256SUMS.json"}, "delta inventory mismatch")
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


def feature_path(path):
    """Feature subjects/evidence for the bound WS-E01 features."""
    return bool(re.fullmatch(r"features/" + FEATURE_ID_PATTERN
                             + r"/(subject\.json|state\.json|[a-z0-9-]+\.md|evidence/[a-z0-9-]+\.(json|md))", path))


def product_path(path):
    """Text sources of the WindowSafe add-on and its qualification probes; no binaries."""
    name = r"[A-Za-z0-9_][A-Za-z0-9_.-]*"
    return bool(re.fullmatch(r"(addon|qualification/ws-e01-f0[1-5])/(" + name + r"/){0,4}" + name
                             + r"\.(ts|js|mjs|json|html|css|svg|md|py|txt)", path)
                and "node_modules" not in path)


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
    allowed |= path in {DELTA_SUBJECT, DELTA_EVIDENCE, DELTA_BINDING} | set(DELTA_SOURCES)
    allowed |= path in EPIC_DELTA_FILES | EPIC_CORR_FILES | EPIC_CORR2_FILES | {EPIC_REBINDING, EPIC_REBIND_AUTH}
    allowed |= feature_path(path) or product_path(path)
    require(allowed, "outside foundation-only path scope")
    require(PurePosixPath(path).name != "manifest.json" or product_path(path), "extension manifest prohibited")


def delta_integrity(read):
    """Verify the new authorization and immutable originals, never issue a verdict."""
    manifest = read(DELTA_INPUTS + "SHA256SUMS.json")
    require(sha256(manifest) == DELTA_MANIFEST_SHA, "delta manifest drift")
    entries = parse(manifest)["FILES"]
    for name, entry in entries.items():
        safe_path(name)
        raw = read(DELTA_INPUTS + name)
        require(len(raw) == entry["bytes"] and sha256(raw) == entry["sha256"], "delta input drift")
    require(sha256(read(DELTA_AUTH)) == DELTA_AUTH_SHA, "delta authorization drift")
    for name, blob in DELTA_SOURCES.items():
        raw = read(name)
        require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == blob,
                "final V6 blob drift")
    subject = parse(read(DELTA_SUBJECT))
    expected = {
        "subject_id": DELTA_ID, "review_type": "PROJECT_FOUNDATION_REVIEW",
        "status": "PROJECT_FOUNDATION_READY_FOR_REVIEW",
        "start_baseline_sha": DELTA_BASE,
        "work_branch": "foundation/ws-pf-delta-20260928-01",
        "execution_authorization_path": DELTA_AUTH,
        "execution_authorization_sha256": DELTA_AUTH_SHA,
        "independent_review_status": "PENDING", "risk": "ELEVATED",
        "external_project_context_sync": "PENDING_AFTER_PROJECT_FOUNDATION_REVIEW_PASS",
        "product_features_started": False, "integration_authorized": False,
        "epic_delta_started": False, "f01_continuation_authorized": False,
        "feature_acceptance_started": False, "operations_policy": "NOT_APPLICABLE_NOT_ACTIVATED",
        "open_material_user_decisions": [],
        "f01_evidence_reference": {
            "pr": 3, "head": "7d66ca5b025c8f748d7f97b961c496ee450daaa7",
            "role": "READ_ONLY_EXTERNAL_QUALIFICATION_EVIDENCE",
        },
        "end_state_binding": "EXACT_COMMIT_SUPPLIED_BY_REVIEW_REQUEST_NO_SELF_REFERENTIAL_SHA",
    }
    for key, value in expected.items():
        require(subject.get(key) == value and type(subject.get(key)) is type(value), "delta subject boundary")
    fields(subject, set(expected) | {"implementer", "evidence_paths"})
    text(subject["implementer"])
    evidence = subject["evidence_paths"]
    required = {DELTA_INPUTS + n for n in entries} | {DELTA_INPUTS + "SHA256SUMS.json", DELTA_EVIDENCE}
    required |= set(DELTA_SOURCES) | DELTA_SUPPORT | {CONTRACT_PATH}
    required |= {"foundation/inputs/inputs/" + n for n in (
        "WindowSafe_Product_Definition_WS-PD-20260917-01.md",
        "WindowSafe_Approval_Record_WS-PD-20260917-01.json",
        "WindowSafe_Technical_Foundation_WS-TFP-20260917-01_r6.md")}
    require(isinstance(evidence, list) and len(evidence) == len(set(evidence))
            and required <= set(evidence), "delta evidence incomplete")
    for name in evidence:
        scope(name)
        read(name)


def tree_snapshot(revision):
    return {entry.split(b"\t", 1)[1].decode(): entry.split(b"\t", 1)[0]
            for entry in git("ls-tree", "-rz", revision).split(b"\0") if entry}


def delta_history(head):
    """Bind this additive run to main without shortening any historical checks.

    Returns the reviewed subject commit: head itself while review is pending, or
    the exact authorized reviewed head once the separate acceptance exists.
    """
    ancestor(DELTA_BASE, head)
    read = lambda name: at(head, name)
    if DELTA_BINDING in tree_snapshot(head):
        # request(reviewed) inside re-runs the unchanged original delta checks;
        # a validated epic delta continuation stops this walk at its exact merge base.
        integrated = foundation_integration_head(head)
        reviewed, allowed = accepted_delta_binding(read, integrated)
        delta_integration_history(reviewed, integrated, allowed)
        return reviewed
    delta_integrity(read)
    manifest = parse(read(DELTA_INPUTS + "SHA256SUMS.json"))["FILES"]
    allowed = DELTA_SUPPORT | {DELTA_SUBJECT, DELTA_EVIDENCE} | set(DELTA_SOURCES)
    allowed |= {DELTA_INPUTS + n for n in manifest} | {DELTA_INPUTS + "SHA256SUMS.json"}
    snapshot = tree_snapshot
    previous = snapshot(DELTA_BASE)
    for revision in git("rev-list", "--reverse", DELTA_BASE + ".." + head).decode().splitlines():
        require(len(git("rev-list", "--parents", "-n", "1", revision).split()) == 2,
                "delta merges prohibited")
        changed = set(git("diff", "--name-only", revision + "^", revision).decode().splitlines())
        require(changed <= allowed, "delta scope drift")
        current = snapshot(revision)
        check_history_maps(previous, current)
        require(current.get("foundation/subject.json") == previous.get("foundation/subject.json"),
                "historical foundation subject drift")
        previous = current
    require(read("foundation/subject.json") == at(DELTA_BASE, "foundation/subject.json"),
            "historical foundation subject drift")
    return head


def accepted_delta_binding(read, head):
    """Consume the authorized PASS; preserve the reviewed delta subject and verdict."""
    raw = read(DELTA_INTEGRATION_AUTH)
    require(sha256(raw) == DELTA_INTEGRATION_AUTH_SHA, "integration authorization hash")
    auth = parse(raw)
    require(auth["DOCUMENT_TYPE"] == "PROJECT_FOUNDATION_PASS_INTEGRATION_AUTHORIZATION"
            and auth["STATUS"] == "AUTHORIZED" and auth["AUTHORITY"] == "USER", "integration authorization")
    require(auth["EXPECTED_MAIN_SHA"] == DELTA_BASE, "integration baseline mismatch")
    reviewed = auth["EXPECTED_REVIEWED_HEAD"]
    require(isinstance(reviewed, str) and re.fullmatch(SHA_PATTERN, reviewed)
            and commit(reviewed) == reviewed, "reviewed delta SHA")
    require(git("rev-parse", reviewed + "^{tree}").decode().strip() == auth["EXPECTED_REVIEWED_TREE"],
            "reviewed delta tree")
    ancestor(reviewed, head)
    require(DELTA_BINDING not in tree_snapshot(reviewed), "acceptance requires pending original")
    require(read(DELTA_SUBJECT) == at(reviewed, DELTA_SUBJECT), "immutable delta subject drift")
    req = request(reviewed, DELTA_SUBJECT)
    for item in req["reviewed_evidence"]:
        if protected(item["path"]):
            require(sha256(read(item["path"])) == item["sha256"], "immutable delta evidence drift")
    exact = auth["EXACT_REVIEW_RESULT"]
    reference = safe_path(exact["TARGET"])
    require(re.fullmatch(r"reviews/results/" + ID_PATTERN + r"\.json", reference), "result locator")
    result_raw = read(reference)
    require(len(result_raw) == exact["BYTES"] and sha256(result_raw) == exact["SHA256"],
            "integration original result mismatch")
    result = parse(result_raw)
    validate_result(result, req, parse(at(reviewed, CONTRACT_PATH)), PurePosixPath(reference).name)
    require(result["verdict"] == exact["VERDICT"] == "PASS"
            and result["review_type"] == "PROJECT_FOUNDATION_REVIEW", "foundation PASS required")
    expected = {
        "status": "PROJECT_FOUNDATION_ACCEPTED",
        "subject_id": DELTA_ID,
        "review_type": "PROJECT_FOUNDATION_REVIEW",
        "project_foundation_subject_immutable_reference": req["subject"],
        "project_foundation_review_result_reference": reference,
        "project_foundation_review_result_sha256": exact["SHA256"],
        "independent_review_verdict": "PASS",
        "open_critical_blocking_major_findings": "NONE",
        "open_nonblocking_finding_ids": [item["id"] for item in result["findings"] if item["status"] == "OPEN"],
        "execution_authorization_reference": DELTA_INTEGRATION_AUTH,
        "execution_authorization_sha256": DELTA_INTEGRATION_AUTH_SHA,
        "external_project_context_sync": "PENDING",
        "next_gate": DELTA_NEXT_GATE,
        "epic_delta_started": False,
        "epic_rebinding_started": False,
        "f01_continuation_authorized": False,
        "feature_acceptance_started": False,
        "product_features_started": False,
        "release_or_production_authorized": False,
        "f01_evidence_reference": parse(at(reviewed, DELTA_SUBJECT))["f01_evidence_reference"],
        "execution_scope": "PROJECT_FOUNDATION_PASS_INTEGRATION_ONLY__NO_CONTEXT_SYNC_EPIC_OR_FEATURE_EXECUTION",
    }
    # Canonical JSON comparison also rejects type drift such as 0 for false.
    require(json.dumps(parse(read(DELTA_BINDING)), sort_keys=True) == json.dumps(expected, sort_keys=True),
            "accepted binding mismatch")
    allowed = DELTA_SUPPORT | {DELTA_BINDING, DELTA_INTEGRATION_AUTH, reference}
    require(set(git("diff", "--name-only", reviewed, head).decode().splitlines()) <= allowed,
            "post-review integration scope")
    return reviewed, allowed


def delta_integration_history(reviewed, head, allowed):
    """Every post-review commit, plus at most one exact normal merge into DELTA_BASE."""
    merges = set()
    previous = tree_snapshot(reviewed)
    for revision in git("rev-list", "--reverse", reviewed + ".." + head).decode().splitlines():
        parents = git("rev-list", "--parents", "-n", "1", revision).decode().split()[1:]
        if len(parents) == 2:
            require(parents[0] == DELTA_BASE and not merges, "authorized foundation normal merge required")
            ancestor(reviewed, parents[1])
            require(git("rev-parse", revision + "^{tree}") == git("rev-parse", parents[1] + "^{tree}"),
                    "foundation integration tree drift")
            require(at(parents[1], DELTA_BINDING) == at(head, DELTA_BINDING), "merge acceptance mismatch")
            merges.add(revision)
            previous = tree_snapshot(parents[1])
        else:
            require(len(parents) == 1, "integration merges prohibited")
            changed = set(git("diff", "--name-only", parents[0], revision).decode().splitlines())
            require(changed <= allowed, "post-review integration scope")
        current = tree_snapshot(revision)
        check_history_maps(previous, current)
        previous = current
    return merges


def delta_integration_merges(head):
    """The validated normal merge of the accepted delta, if one exists."""
    if DELTA_BINDING not in tree_snapshot(head):
        return set()
    reviewed = delta_history(head)
    # Only up to the integrated foundation state; a later epic merge is validated separately.
    integrated = EPIC_DELTA_BASE if EPIC_DELTA_SUBJECT in tree_snapshot(head) else head
    return set(git("rev-list", "--min-parents=2", reviewed + ".." + integrated).decode().splitlines())


def epic_delta_merges(head):
    """The validated normal merge of the rebound epic delta, if one exists."""
    if EPIC_REBINDING not in tree_snapshot(head):
        return set()
    return epic_delta_history(head)


def delta_scope_head(head):
    paths = git("ls-tree", "-r", "--name-only", head).decode().splitlines()
    if DELTA_SUBJECT not in paths:
        return head
    delta_history(head)
    return DELTA_BASE


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def epic_delta_expected():
    """Exact pre-review subject/binding values; acceptance needs a new bound transition."""
    product = "foundation/inputs/inputs/WindowSafe_Product_Definition_WS-PD-20260917-01.md"
    technical = "foundation/inputs/inputs/WindowSafe_Technical_Foundation_WS-TFP-20260917-01_r6.md"
    references = {
        "epic_preparation_delta_reference": EPIC_DELTA_DIR + "preparation.md",
        "epic_preparation_critical_self_review_reference": EPIC_DELTA_DIR + "critical-self-review.md",
        "previous_preparation_delta_reference": EPIC_DELTA_DIR + "previous-preparation-delta.md",
        "project_foundation_binding_reference": DELTA_BINDING,
        "project_foundation_review_result_reference": "reviews/results/WS-PFR-DELTA-20260928-01.json",
        "approved_product_definition_reference": product,
        "approved_product_approval_reference": "foundation/inputs/inputs/WindowSafe_Approval_Record_WS-PD-20260917-01.json",
        "approved_product_delta_reference":
            DELTA_INPUTS + "WindowSafe_Product_Definition_Delta_WS-PD-DELTA-20260924-01.md",
        "approved_product_delta_approval_reference":
            DELTA_INPUTS + "WindowSafe_Product_Delta_Approval_WS-PD-DELTA-APPROVAL-20260928-01.json",
        "project_technical_foundation_reference": technical,
        "technical_foundation_delta_reference":
            DELTA_INPUTS + "WindowSafe_Technical_Foundation_Delta_Preparation_WS-TFP-DELTA-20260928-02.md",
        "technical_foundation_delta_binding_reference":
            DELTA_INPUTS + "WindowSafe_Technical_Foundation_Delta_Binding_WS-TFP-DELTA-BIND-20260928-01.json",
        "external_project_context_sync_reference": EPIC_DELTA_DIR + "external-context-sync.json",
        "external_project_description_reference": EPIC_DELTA_DIR + "project-description.md",
        "user_execution_direction_reference": EPIC_DELTA_DIR + "execution-direction.json",
        "execution_authorization_path": EPIC_DELTA_AUTH,
    }
    historical = {
        "epic_preparation_id": "WS-E01-EP-20260919-01",
        "preparation_path": "epics/WS-E01/preparation.md",
        "subject_path": "epics/WS-E01/subject.json",
        "binding_path": "epics/WS-E01/binding.json",
        "reviewed_end_sha": "644b81f63dcc1990bc894a9c2c9bd8dc24a98c04",
        "review_result_reference": "reviews/results/WS-E01-EPR-20260919-02.json",
        "binding_status": "READY_FOR_AGENT__HISTORICAL_PRESERVED_NOT_CURRENT_F01_AUTHORIZATION",
    }
    subject = dict(references,
        subject_id=EPIC_DELTA_ID, epic_id="WS-E01", review_type="EPIC_PREPARATION_REVIEW",
        status="EPIC_PREPARATION_DELTA_READY_FOR_REVIEW",
        end_state_binding="EXACT_COMMIT_SUPPLIED_BY_REVIEW_REQUEST_NO_SELF_REFERENTIAL_SHA",
        epic_preparation_delta_id=EPIC_DELTA_ID,
        previous_preparation_delta_id="WS-E01-EP-DELTA-20260929-01",
        current_canonical_baseline_or_main_sha=EPIC_DELTA_BASE,
        work_branch="prep/ws-e01-delta-20260929-02",
        execution_authorization_sha256=EPIC_DELTA_AUTH_SHA,
        historical_epic_preparation=historical,
        project_foundation_status="PROJECT_FOUNDATION_ACCEPTED",
        project_foundation_review_verdict="PASS",
        external_project_context_sync="CONFIRMED_BY_USER",
        user_execution_direction="USER_CONFIRMED_DIRECTION",
        epic_research_reuse_or_delta_status="REUSED_NO_MATERIAL_DELTA",
        epic_preparation_critical_self_review_status=SELF_REVIEW_COMPLETE,
        open_material_user_decisions_required_before_start=[],
        independent_review_status="PENDING", risk="ELEVATED",
        ready_for_agent=False, product_features_started=False,
        browser_profile_tests_executed=False, f01_continuation_authorized=False,
        exact_epic_rebinding_created=False, broad_ws_e01_execution_authorization_created=False,
        feature_acceptance_started=False, f01_evidence_reference=F01_EVIDENCE)
    binding = {
        "status": "REVIEW_REQUIRED",
        "epic_id": "WS-E01",
        "epic_preparation_subject_id": EPIC_DELTA_ID,
        "epic_preparation_subject_path": EPIC_DELTA_SUBJECT,
        "current_canonical_baseline_or_main_sha": EPIC_DELTA_BASE,
        "project_foundation_binding_reference": DELTA_BINDING,
        "project_foundation_review_result_reference": references["project_foundation_review_result_reference"],
        "external_project_context_sync": "CONFIRMED_BY_USER",
        "epic_research_reuse_or_delta_status": "REUSED_NO_MATERIAL_DELTA",
        "epic_preparation_critical_self_review_status": SELF_REVIEW_COMPLETE,
        "independent_epic_preparation_review": "PENDING",
        "epic_preparation_review_result_reference": None,
        "exact_epic_rebinding": "PENDING",
        "open_critical_blocking_major_findings": "NONE_AT_SELF_REVIEW__INDEPENDENT_REVIEW_PENDING",
        "open_material_user_decisions_required_before_start": "NONE",
        "ready_for_agent": False,
        "f01_continuation_authorized": False,
        "broad_ws_e01_execution_authorization": "NOT_CREATED",
        "execution_authorization_reference": EPIC_DELTA_AUTH,
        "execution_authorization_sha256": EPIC_DELTA_AUTH_SHA,
        "historical_epic_binding_reference": historical["binding_path"],
        "historical_epic_binding": "PRESERVED",
        "execution_scope": "EPIC_PREPARATION_DELTA_MATERIALIZATION_ONLY__NO_REVIEW_VERDICT_REBINDING_OR_FEATURE_EXECUTION",
    }
    required = set(references.values()) | {historical[k] for k in (
        "preparation_path", "subject_path", "binding_path", "review_result_reference")}
    return subject, binding, required


def epic_delta_integrity(read):
    """Mechanical binding of the one versioned WS-E01 delta; never an independent verdict."""
    for name, (size, digest) in EPIC_DELTA_ORIGINALS.items():
        raw = read(name)
        require(len(raw) == size and sha256(raw) == digest, "epic delta original drift")
    for name, blob in EPIC_DELTA_PINNED_BLOBS.items():
        require(git_blob(read(name)) == blob, "pinned epic delta reference drift")
    auth = parse(read(EPIC_DELTA_AUTH))
    target = auth["MATERIALIZATION_TARGET"]
    require(auth["STATUS"] == "AUTHORIZED" and auth["AUTHORITY"] == "USER"
            and auth["TARGET_REPOSITORY"]["EXPECTED_START_MAIN_SHA"] == EPIC_DELTA_BASE
            and target["SUBJECT_PATH"] == EPIC_DELTA_SUBJECT and target["READY_FOR_AGENT"] is False
            and auth["MERGE_AUTHORIZED"] is False and auth["F01_CONTINUATION_AUTHORIZED"] is False,
            "epic delta authorization")
    bound = {item["SHA256"] for item in auth["BOUND_PROJECT_LLM_ARTIFACTS"].values()}
    require(bound == {digest for name, (_, digest) in EPIC_DELTA_ORIGINALS.items() if name != EPIC_DELTA_AUTH},
            "epic delta artifact binding")
    expected, binding, required = epic_delta_expected()
    subject = parse(read(EPIC_DELTA_SUBJECT))
    fields(subject, set(expected) | {"implementer", "materializer", "evidence_paths"})
    for key, value in expected.items():
        # Canonical JSON comparison also rejects type drift such as 0 for false.
        require(json.dumps(subject[key], sort_keys=True) == json.dumps(value, sort_keys=True),
                "epic delta subject boundary")
    text(subject["implementer"])
    text(subject["materializer"])
    require(json.dumps(parse(read(EPIC_DELTA_BINDING)), sort_keys=True) == json.dumps(binding, sort_keys=True),
            "epic delta binding must stay pending")
    evidence = subject["evidence_paths"]
    required |= (EPIC_DELTA_FILES - {EPIC_DELTA_SUBJECT}) | set(EPIC_DELTA_PINNED_BLOBS)
    required |= EPIC_DELTA_SUPPORT | set(DELTA_SOURCES) | {CONTRACT_PATH}
    require(isinstance(evidence, list) and len(evidence) == len(set(evidence))
            and required <= set(evidence) and EPIC_DELTA_SUBJECT not in evidence, "epic delta evidence incomplete")
    for name in evidence:
        scope(name)
        read(name)


def epic_delta_history(head):
    """Linear exact-scope continuation from the integrated foundation merge only.

    Once the bound correction subject exists, every commit after the exact
    CORRECTION_REQUIRED head uses the correction allowlist instead; the reviewed
    delta namespace remains append-only and outside that allowlist.
    """
    ancestor(EPIC_DELTA_BASE, head)
    tree = tree_snapshot(head)
    corrected, corrected2 = set(), set()
    if EPIC_CORR_SUBJECT in tree:
        ancestor(EPIC_DELTA_REVIEWED, head)
        corrected = set(git("rev-list", EPIC_DELTA_REVIEWED + ".." + head).decode().splitlines())
    if EPIC_CORR2_SUBJECT in tree:
        require(EPIC_CORR_SUBJECT in tree, "second correction requires first")
        ancestor(EPIC_CORR_REVIEWED, head)
        corrected2 = set(git("rev-list", EPIC_CORR_REVIEWED + ".." + head).decode().splitlines())
    rebound, merges = set(), set()
    if EPIC_REBINDING in tree:
        require(EPIC_CORR2_SUBJECT in tree, "rebinding requires reviewed subject")
        ancestor(EPIC_CORR2_REVIEWED, head)
        rebound = set(git("rev-list", EPIC_CORR2_REVIEWED + ".." + head).decode().splitlines())
    executing = set()
    if EPIC_EXECUTION_AUTH in tree:
        require(EPIC_REBINDING in tree, "execution requires exact rebinding")
        ancestor(EPIC_INTEGRATION_MERGE, head)
        executing = set(git("rev-list", EPIC_INTEGRATION_MERGE + ".." + head).decode().splitlines())
    previous = tree_snapshot(EPIC_DELTA_BASE)
    for revision in git("rev-list", "--reverse", "--topo-order", EPIC_DELTA_BASE + ".." + head).decode().splitlines():
        if revision in executing:
            continue  # Checked per parent by execution_history below.
        parents = git("rev-list", "--parents", "-n", "1", revision).decode().split()[1:]
        if len(parents) == 2 and rebound and not merges:
            # Exactly one normal merge of the rebound integration head into the bound main.
            require(parents[0] == EPIC_DELTA_BASE
                    and (revision == head or (executing and revision == EPIC_INTEGRATION_MERGE)),
                    "authorized epic delta merge required")
            ancestor(EPIC_CORR2_REVIEWED, parents[1])
            require(EPIC_REBINDING in tree_snapshot(parents[1])
                    and at(parents[1], EPIC_REBINDING) == at(head, EPIC_REBINDING), "merge rebinding mismatch")
            require(git("rev-parse", revision + "^{tree}") == git("rev-parse", parents[1] + "^{tree}"),
                    "epic delta integration tree drift")
            merges.add(revision)
            previous = tree_snapshot(parents[1])
            continue
        require(len(parents) == 1, "epic delta merges prohibited")
        changed = set(git("diff", "--name-only", parents[0], revision).decode().splitlines())
        if revision in rebound:
            allowed = EPIC_REBIND_ALLOWED
        elif revision in corrected2:
            allowed = EPIC_CORR2_ALLOWED
        elif revision in corrected:
            allowed = EPIC_CORR_ALLOWED
        else:
            allowed = EPIC_DELTA_FILES | EPIC_DELTA_SUPPORT
        require(changed <= allowed, "epic delta scope drift")
        current = tree_snapshot(revision)
        check_history_maps(previous, current)
        previous = current
    epic_delta_integrity(lambda name: at(head, name))
    if corrected:
        epic_correction_integrity(lambda name: at(head, name))
    if corrected2:
        epic_correction2_integrity(lambda name: at(head, name))
    if rebound:
        epic_rebinding_integrity(lambda name: at(head, name))
    if executing:
        require(EPIC_INTEGRATION_MERGE in merges, "execution requires the integration merge")
        execution_authorization_integrity(lambda name: at(head, name))
        merges |= execution_history(executing)
    return merges


def execution_history(revisions):
    """Feature execution after the integration merge: scoped, append-only, up-to-date merges only."""
    merges = set()
    for revision in revisions:
        parents = git("rev-list", "--parents", "-n", "1", revision).decode().split()[1:]
        current = tree_snapshot(revision)
        if len(parents) == 2:
            # A PR merge must not combine unreviewed trees: the merged tree is the PR head's tree.
            require(git("rev-parse", revision + "^{tree}") == git("rev-parse", parents[1] + "^{tree}"),
                    "execution merge must be up to date")
            ancestor(EPIC_INTEGRATION_MERGE, parents[0])
            merges.add(revision)
        else:
            require(len(parents) == 1, "execution octopus merge prohibited")
            for path in git("diff", "--name-only", parents[0], revision).decode().splitlines():
                scope(path)
                require(not path.startswith(EXECUTION_FROZEN_PREFIXES), "frozen path changed during execution")
        for parent in parents:
            check_history_maps(tree_snapshot(parent), current)
    return merges


def execution_authorization_integrity(read):
    """The separate broad WS-E01 authorization; it creates no verdict and no acceptance."""
    raw = read(EPIC_EXECUTION_AUTH)
    require(sha256(raw) == EPIC_EXECUTION_AUTH_SHA, "broad execution authorization hash")
    auth = parse(raw)
    require(auth["STATUS"] == "AUTHORIZED" and auth["AUTHORITY"] == "USER" and auth["EPIC_ID"] == "WS-E01"
            and auth["REQUIRED_EPIC_REBINDING"] == {"path": EPIC_REBINDING, "sha256": sha256(read(EPIC_REBINDING))}
            and auth["INTEGRATION_MERGE"] == EPIC_INTEGRATION_MERGE
            and auth["FEATURE_DIRECTION"] == "F01 -> F02 -> {F03,F04} -> F05"
            and auth["STOP_AT"] == "EPIC_CONVERGED" and auth["NEXT_EPIC_SELECTION_BY_AGENT"] is False
            and auth["SELF_PASS_ALLOWED"] is False and auth["RELEASE_OR_PRODUCTION_AUTHORIZED"] is False,
            "broad execution authorization")
    rebinding = parse(read(EPIC_REBINDING))
    require(rebinding["status"] == "READY_FOR_AGENT" and rebinding["ready_for_agent"] is True,
            "execution requires READY_FOR_AGENT")


def epic_correction_expected():
    """Exact pre-rereview values; the factual preparation content is the reviewed delta's."""
    subject, binding, _ = epic_delta_expected()
    blob = EPIC_DELTA_PINNED_BLOBS["epics/WS-E01/binding.json"]
    superseded = {
        "id": EPIC_DELTA_ID, "path": EPIC_DELTA_SUBJECT,
        "end_sha": EPIC_DELTA_REVIEWED, "tree": EPIC_DELTA_REVIEWED_TREE,
        "execution_authorization_path": EPIC_DELTA_AUTH,
        "review_id": EPIC_DELTA_REVIEW_ID, "review_result_reference": EPIC_DELTA_RESULT,
        "review_result_sha256": EPIC_DELTA_RESULT_ORIGINAL[1], "review_verdict": "CORRECTION_REQUIRED",
        "status": "HISTORICAL_CORRECTION_REQUIRED_PRESERVED",
    }
    subject = dict(subject,
        subject_id=EPIC_CORR_ID, epic_preparation_delta_id=EPIC_CORR_ID,
        implementer=EPIC_CORR_EXCLUDED[0], materializer=EPIC_CORR_EXCLUDED[2],
        review_excluded_identities=EPIC_CORR_EXCLUDED,
        execution_authorization_path=EPIC_CORR_AUTH, execution_authorization_sha256=EPIC_CORR_AUTH_SHA,
        correction_id="WS-E01-EP-CORR-20260929-02",
        correction_reference=EPIC_CORR_DIR + "correction.md",
        correction_disposition_reference=EPIC_CORR_DIR + "correction-disposition.json",
        correction_critical_self_review_reference=EPIC_CORR_DIR + "correction-critical-self-review.md",
        superseded_subject=superseded,
        historical_epic_binding_git_blob=blob,
        architecture_reference="foundation/architecture.md",
        mandatory_prewrite_reads=EPIC_CORR_PREWRITE,
        product_truth_change="NONE", technical_foundation_change="NONE", epic_product_scope_change="NONE")
    binding = dict(binding,
        epic_preparation_subject_id=EPIC_CORR_ID, epic_preparation_subject_path=EPIC_CORR_SUBJECT,
        independent_epic_preparation_review="PENDING_REREVIEW",
        open_critical_blocking_major_findings="NONE_AT_SELF_REVIEW__INDEPENDENT_REREVIEW_PENDING",
        execution_authorization_reference=EPIC_CORR_AUTH, execution_authorization_sha256=EPIC_CORR_AUTH_SHA,
        review_excluded_identities=EPIC_CORR_EXCLUDED,
        superseded_subject_reference=EPIC_DELTA_SUBJECT, superseded_subject_end_sha=EPIC_DELTA_REVIEWED,
        superseded_review_result_reference=EPIC_DELTA_RESULT, superseded_review_verdict="CORRECTION_REQUIRED",
        historical_epic_binding_git_blob=blob,
        execution_scope="EPIC_PREPARATION_DELTA_CORRECTION_ONLY__NO_REVIEW_VERDICT_REBINDING_MERGE_OR_FEATURE_EXECUTION")
    return subject, binding


def epic_correction_integrity(read):
    """Mechanical binding of the one correction of the reviewed delta; never a verdict."""
    for name, (size, digest) in EPIC_CORR_ORIGINALS.items():
        raw = read(name)
        require(len(raw) == size and sha256(raw) == digest, "epic correction original drift")
    result_raw = read(EPIC_DELTA_RESULT)
    require((len(result_raw), sha256(result_raw)) == EPIC_DELTA_RESULT_ORIGINAL, "correction source review drift")
    require(commit(EPIC_DELTA_REVIEWED) == EPIC_DELTA_REVIEWED
            and git("rev-parse", EPIC_DELTA_REVIEWED + "^{tree}").decode().strip() == EPIC_DELTA_REVIEWED_TREE
            and EPIC_CORR_SUBJECT not in tree_snapshot(EPIC_DELTA_REVIEWED), "reviewed delta head")
    for name in EPIC_DELTA_FILES:
        require(read(name) == at(EPIC_DELTA_REVIEWED, name), "reviewed delta namespace drift")
    result = parse(result_raw)
    validate_result(result, request(EPIC_DELTA_REVIEWED, EPIC_DELTA_SUBJECT),
                    parse(at(EPIC_DELTA_REVIEWED, CONTRACT_PATH)), PurePosixPath(EPIC_DELTA_RESULT).name)
    require(result["verdict"] == "CORRECTION_REQUIRED", "correction source verdict")
    blob = git_blob(read("epics/WS-E01/binding.json"))
    require(re.fullmatch(SHA_PATTERN, blob) and blob == EPIC_DELTA_PINNED_BLOBS["epics/WS-E01/binding.json"],
            "historical binding blob")
    auth = parse(read(EPIC_CORR_AUTH))
    repository, correction, source = auth["TARGET_REPOSITORY"], auth["CORRECTION"], auth["EXACT_SOURCE_REVIEW"]
    require(auth["STATUS"] == "AUTHORIZED" and auth["AUTHORITY"] == "USER"
            and repository["EXPECTED_MAIN_SHA"] == EPIC_DELTA_BASE
            and repository["EXPECTED_START_HEAD"] == EPIC_DELTA_REVIEWED
            and repository["EXPECTED_START_TREE"] == EPIC_DELTA_REVIEWED_TREE
            and (source["BYTES"], source["SHA256"]) == EPIC_DELTA_RESULT_ORIGINAL
            and source["TRANSFER_TARGET"] == EPIC_DELTA_RESULT and source["VERDICT"] == "CORRECTION_REQUIRED"
            and correction["CORRECTED_SUBJECT_PATH"] == EPIC_CORR_SUBJECT
            and correction["REVIEW_EXCLUDED_IDENTITIES"] == EPIC_CORR_EXCLUDED
            and correction["FULL_HISTORICAL_EPIC_BINDING_BLOB"] == blob
            and auth["MERGE_AUTHORIZED"] is False and auth["F01_CONTINUATION_AUTHORIZED"] is False
            and auth["PRODUCT_IMPLEMENTATION_AUTHORIZED"] is False, "epic correction authorization")
    bound = {item["sha256"] for item in auth["BOUND_PROJECT_LLM_ARTIFACTS"].values()}
    require(bound == {digest for name, (_, digest) in EPIC_CORR_ORIGINALS.items() if name != EPIC_CORR_AUTH},
            "epic correction artifact binding")
    prewrite = {item["path"]: item["git_blob"] for item in auth["MANDATORY_PREWRITE_READS"]}
    require(prewrite == EPIC_CORR_PREWRITE, "mandatory pre-write sources")
    for name, value in prewrite.items():
        require(git_blob(read(name)) == value, "mandatory pre-write source drift")
    expected, binding = epic_correction_expected()
    subject = parse(read(EPIC_CORR_SUBJECT))
    fields(subject, set(expected) | {"evidence_paths"})
    for key, value in expected.items():
        # Canonical JSON comparison also rejects type drift and truncated locators.
        require(json.dumps(subject[key], sort_keys=True) == json.dumps(value, sort_keys=True),
                "epic correction subject boundary")
    require(json.dumps(parse(read(EPIC_CORR_BINDING)), sort_keys=True) == json.dumps(binding, sort_keys=True),
            "epic correction binding must stay pending")
    evidence = subject["evidence_paths"]
    required = set(parse(read(EPIC_DELTA_SUBJECT))["evidence_paths"]) | {EPIC_DELTA_SUBJECT, EPIC_DELTA_RESULT}
    required |= (EPIC_CORR_FILES - {EPIC_CORR_SUBJECT}) | EPIC_CORR_SUPPORT | set(EPIC_CORR_PREWRITE)
    required |= set(EPIC_DELTA_PINNED_BLOBS) | {CONTRACT_PATH}
    require(isinstance(evidence, list) and len(evidence) == len(set(evidence))
            and required <= set(evidence) and EPIC_CORR_SUBJECT not in evidence,
            "epic correction evidence incomplete")
    for name in evidence:
        scope(name)
        read(name)


def epic_correction2_expected():
    """Exact pre-rereview values of -04; review_excluded_identities is checked by closure instead."""
    subject, binding = epic_correction_expected()
    results = [dict(review_id=PurePosixPath(path).stem, review_result_reference=path, bytes=size,
                    review_result_sha256=digest, review_verdict=verdict)
               for path, (size, digest, verdict) in sorted(EPIC_CORR_RESULTS.items())]
    results[1]["provenance_class"] = "RECONSTRUCTED_FROM_REVIEW_TRANSCRIPT"
    results[1]["replaces_unavailable_original"] = "WS-E01-EPR-DELTA-20260929-03"
    superseded = {
        "id": EPIC_CORR_ID, "path": EPIC_CORR_SUBJECT,
        "end_sha": EPIC_CORR_REVIEWED, "tree": EPIC_CORR_REVIEWED_TREE,
        "execution_authorization_path": EPIC_CORR_AUTH,
        "review_results": results,
        "status": "HISTORICAL_CORRECTION_REQUIRED_PRESERVED",
    }
    del subject["review_excluded_identities"]
    subject = dict(subject,
        subject_id=EPIC_CORR2_ID, epic_preparation_delta_id=EPIC_CORR2_ID,
        implementer="PROJECT_LLM_WS_E01_EP_DELTA_20260929_04",
        materializer="CODING_AGENT_WS_E01_EPDELTA_CORR_20260929_02",
        execution_authorization_path=EPIC_CORR2_AUTH, execution_authorization_sha256=EPIC_CORR2_AUTH_SHA,
        second_correction_id="WS-E01-EP-CORR-20260930-04",
        superseded_subject=superseded,
        review_exclusion_rule="DERIVED_TRANSITIVE_LINEAGE_AUTHORS_AND_MATERIALIZERS_SUBSET_OF_SUBJECT_SET")
    del binding["review_excluded_identities"]
    binding = dict(binding,
        epic_preparation_subject_id=EPIC_CORR2_ID, epic_preparation_subject_path=EPIC_CORR2_SUBJECT,
        execution_authorization_reference=EPIC_CORR2_AUTH, execution_authorization_sha256=EPIC_CORR2_AUTH_SHA,
        superseded_subject_reference=EPIC_CORR_SUBJECT, superseded_subject_end_sha=EPIC_CORR_REVIEWED,
        superseded_review_result_reference=results[1]["review_result_reference"],
        superseded_review_verdict="CORRECTION_REQUIRED",
        superseded_blocked_review_result_reference=results[0]["review_result_reference"],
        review_exclusion_rule=subject["review_exclusion_rule"])
    return subject, binding


def epic_correction2_integrity(read):
    """Mechanical binding of the -04 correction and its lineage closure; never a verdict."""
    require(commit(EPIC_CORR_REVIEWED) == EPIC_CORR_REVIEWED
            and git("rev-parse", EPIC_CORR_REVIEWED + "^{tree}").decode().strip() == EPIC_CORR_REVIEWED_TREE
            and EPIC_CORR2_SUBJECT not in tree_snapshot(EPIC_CORR_REVIEWED), "reviewed correction head")
    for name in EPIC_DELTA_FILES | EPIC_CORR_FILES | {EPIC_DELTA_RESULT}:
        require(read(name) == at(EPIC_CORR_REVIEWED, name), "reviewed correction namespace drift")
    raw = read(EPIC_CORR2_AUTH)
    require(sha256(raw) == EPIC_CORR2_AUTH_SHA, "second correction authorization hash")
    auth = parse(raw)
    reviewed_req = request(EPIC_CORR_REVIEWED, EPIC_CORR_SUBJECT)
    contract = parse(at(EPIC_CORR_REVIEWED, CONTRACT_PATH))
    bound = {item["TARGET"]: (item["BYTES"], item["SHA256"], item["VERDICT"]) for item in auth["SOURCE_REVIEWS"]}
    require(bound == EPIC_CORR_RESULTS, "second correction source reviews")
    for path, (size, digest, verdict) in EPIC_CORR_RESULTS.items():
        result_raw = read(path)
        require((len(result_raw), sha256(result_raw)) == (size, digest), "second correction source review drift")
        result = parse(result_raw)
        validate_result(result, reviewed_req, contract, PurePosixPath(path).name)
        require(result["verdict"] == verdict, "second correction source verdict")
    repository, correction = auth["TARGET_REPOSITORY"], auth["CORRECTION"]
    require(auth["STATUS"] == "AUTHORIZED" and auth["AUTHORITY"] == "USER"
            and repository["EXPECTED_MAIN_SHA"] == EPIC_DELTA_BASE
            and repository["EXPECTED_START_HEAD"] == EPIC_CORR_REVIEWED
            and repository["EXPECTED_START_TREE"] == EPIC_CORR_REVIEWED_TREE
            and correction["CORRECTED_SUBJECT_PATH"] == EPIC_CORR2_SUBJECT
            and correction["MINIMUM_REVIEW_EXCLUDED_IDENTITIES"] == EPIC_CORR2_MINIMUM_EXCLUDED
            and auth["F01_CONTINUATION_AUTHORIZED"] is False
            and auth["PRODUCT_IMPLEMENTATION_AUTHORIZED"] is False, "second correction authorization")
    for name, value in EPIC_CORR_PREWRITE.items():
        require(git_blob(read(name)) == value, "mandatory pre-write source drift")
    expected, binding = epic_correction2_expected()
    subject = parse(read(EPIC_CORR2_SUBJECT))
    fields(subject, set(expected) | {"review_excluded_identities", "evidence_paths"})
    for key, value in expected.items():
        require(json.dumps(subject[key], sort_keys=True) == json.dumps(value, sort_keys=True),
                "second correction subject boundary")
    excluded = subject["review_excluded_identities"]
    require(isinstance(excluded, list) and all(isinstance(v, str) and v == v.strip() and v for v in excluded)
            and len({v.casefold() for v in excluded}) == len(excluded), "review exclusion set")
    derived = review_exclusion_closure(read, EPIC_CORR2_SUBJECT)
    folded = {v.casefold() for v in excluded}
    require({v.casefold() for v in derived} <= folded, "REQUEST_INVALID: review exclusion closure incomplete")
    require({v.casefold() for v in EPIC_CORR2_MINIMUM_EXCLUDED} <= folded, "authorized minimum exclusions")
    actual = parse(read(EPIC_CORR2_BINDING))
    require(actual.get("review_excluded_identities") == excluded, "second correction binding exclusions")
    actual = {k: v for k, v in actual.items() if k != "review_excluded_identities"}
    require(json.dumps(actual, sort_keys=True) == json.dumps(binding, sort_keys=True),
            "second correction binding must stay pending")
    evidence = subject["evidence_paths"]
    required = set(parse(read(EPIC_CORR_SUBJECT))["evidence_paths"]) | {EPIC_CORR_SUBJECT} | set(EPIC_CORR_RESULTS)
    required |= (EPIC_CORR2_FILES - {EPIC_CORR2_SUBJECT}) | EPIC_CORR2_SUPPORT | set(EPIC_CORR_PREWRITE)
    required |= set(EPIC_DELTA_PINNED_BLOBS) | {CONTRACT_PATH}
    require(isinstance(evidence, list) and len(evidence) == len(set(evidence))
            and required <= set(evidence) and EPIC_CORR2_SUBJECT not in evidence,
            "second correction evidence incomplete")
    for name in evidence:
        scope(name)
        read(name)


def epic_rebinding_expected(read, req, result):
    """Accepted state derived from the unchanged pending -04 binding; no feature authority."""
    pending = parse(read(EPIC_CORR2_BINDING))
    return dict(pending,
        status="READY_FOR_AGENT", ready_for_agent=True,
        independent_epic_preparation_review="PASS", exact_epic_rebinding="CREATED",
        epic_preparation_subject_immutable_reference=req["subject"],
        epic_preparation_review_result_reference=EPIC_REBIND_RESULT,
        epic_preparation_review_result_sha256=EPIC_REBIND_RESULT_ORIGINAL[1],
        open_critical_blocking_major_findings="NONE",
        open_nonblocking_finding_ids=[item["id"] for item in result["findings"] if item["status"] == "OPEN"],
        pending_binding_reference=EPIC_CORR2_BINDING,
        current_epic_binding_for="WS-E01",
        historical_epic_binding="PRESERVED_SUPERSEDED_AS_CURRENT_BY_THIS_REBINDING",
        execution_authorization_reference=EPIC_REBIND_AUTH,
        execution_authorization_sha256=EPIC_REBIND_AUTH_SHA,
        broad_ws_e01_execution_authorization="NOT_CREATED__SEPARATE_RECORD_REQUIRED",
        f01_continuation_authorized=False,
        execution_scope="EXACT_EPIC_REBINDING_AND_PR5_NORMAL_MERGE_ONLY__NO_FEATURE_EXECUTION")


def epic_rebinding_integrity(read):
    """Consume the independent PASS of -04 and bind the accepted epic state; never a verdict."""
    require(commit(EPIC_CORR2_REVIEWED) == EPIC_CORR2_REVIEWED
            and git("rev-parse", EPIC_CORR2_REVIEWED + "^{tree}").decode().strip() == EPIC_CORR2_REVIEWED_TREE
            and EPIC_REBINDING not in tree_snapshot(EPIC_CORR2_REVIEWED), "reviewed rebinding head")
    for name in EPIC_DELTA_FILES | EPIC_CORR_FILES | EPIC_CORR2_FILES | {EPIC_DELTA_RESULT} | set(EPIC_CORR_RESULTS):
        require(read(name) == at(EPIC_CORR2_REVIEWED, name), "reviewed subject namespace drift")
    raw = read(EPIC_REBIND_AUTH)
    require(sha256(raw) == EPIC_REBIND_AUTH_SHA, "rebinding authorization hash")
    auth = parse(raw)
    exact = auth["EXACT_REVIEW_RESULT"]
    require(auth["STATUS"] == "AUTHORIZED" and auth["AUTHORITY"] == "USER"
            and auth["EXPECTED_MAIN_SHA"] == EPIC_DELTA_BASE
            and auth["EXPECTED_REVIEWED_HEAD"] == EPIC_CORR2_REVIEWED
            and auth["EXPECTED_REVIEWED_TREE"] == EPIC_CORR2_REVIEWED_TREE
            and auth["REVIEWED_SUBJECT_PATH"] == EPIC_CORR2_SUBJECT
            and (exact["TARGET"], exact["BYTES"], exact["SHA256"], exact["VERDICT"])
                == (EPIC_REBIND_RESULT, *EPIC_REBIND_RESULT_ORIGINAL, "PASS")
            and auth["MERGE"] == "ONE_NORMAL_MERGE_COMMIT_OF_PR5_INTO_EXPECTED_MAIN"
            and auth["F01_CONTINUATION_AUTHORIZED"] is False
            and auth["PRODUCT_IMPLEMENTATION_AUTHORIZED"] is False, "rebinding authorization")
    result_raw = read(EPIC_REBIND_RESULT)
    require((len(result_raw), sha256(result_raw)) == EPIC_REBIND_RESULT_ORIGINAL, "rebinding original result drift")
    result = parse(result_raw)
    req = request(EPIC_CORR2_REVIEWED, EPIC_CORR2_SUBJECT)
    validate_result(result, req, parse(at(EPIC_CORR2_REVIEWED, CONTRACT_PATH)), PurePosixPath(EPIC_REBIND_RESULT).name)
    require(result["verdict"] == "PASS" and result["review_type"] == "EPIC_PREPARATION_REVIEW", "epic PASS required")
    expected = epic_rebinding_expected(read, req, result)
    # Canonical JSON comparison also rejects type drift such as 1 for true.
    require(json.dumps(parse(read(EPIC_REBINDING)), sort_keys=True) == json.dumps(expected, sort_keys=True),
            "epic rebinding mismatch")

def foundation_integration_head(head):
    """The integrated foundation state; a later bound epic delta is checked on its own."""
    if EPIC_DELTA_SUBJECT not in tree_snapshot(head):
        return head
    epic_delta_history(head)
    return EPIC_DELTA_BASE


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
    require(set(git("diff", "--name-only", reviewed, delta_scope_head(head)).decode().splitlines()) <= allowed,
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
    if (root / DELTA_BINDING).exists():
        accepted_delta_binding(lambda name: (root / name).read_bytes(), foundation_integration_head(commit("HEAD")))
    if (root / EPIC_DELTA_SUBJECT).exists():
        epic_delta_integrity(lambda name: (root / name).read_bytes())
    if (root / EPIC_CORR_SUBJECT).exists():
        epic_correction_integrity(lambda name: (root / name).read_bytes())
    if (root / EPIC_CORR2_SUBJECT).exists():
        epic_correction2_integrity(lambda name: (root / name).read_bytes())
    if (root / EPIC_REBINDING).exists():
        epic_rebinding_integrity(lambda name: (root / name).read_bytes())
    if (root / EPIC_EXECUTION_AUTH).exists():
        execution_authorization_integrity(lambda name: (root / name).read_bytes())
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
    if (root / DELTA_SUBJECT).exists():
        require("foundation.py request --sha HEAD --subject " + DELTA_SUBJECT in workflow,
                "missing delta CI request")
    if (root / EPIC_DELTA_SUBJECT).exists():
        require("foundation.py request --sha HEAD --subject " + EPIC_DELTA_SUBJECT in workflow,
                "missing epic delta CI request")
    if (root / EPIC_CORR_SUBJECT).exists():
        require("foundation.py request --sha HEAD --subject " + EPIC_CORR_SUBJECT in workflow,
                "missing epic correction CI request")
    if (root / EPIC_CORR2_SUBJECT).exists():
        require("foundation.py request --sha HEAD --subject " + EPIC_CORR2_SUBJECT in workflow,
                "missing second epic correction CI request")
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
    return path.startswith(("foundation/inputs/", "foundation/sources/", "foundation/evidence/", "foundation/deltas/", "reviews/results/", "reviews/dispositions/")) or bool(re.fullmatch(r"epics/" + ID_PATTERN + r"/.+", path))


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
    # Only the exact merge already validated against the accepted delta binding.
    delta_merges = delta_integration_merges(head) | epic_delta_merges(head)
    integrations = set(delta_merges)
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
                if merge in delta_merges:
                    continue
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
