"""Prepare a fresh public Git clone and isolated, existing CPython 3.14.4 runtime.

This is environment preparation, never an independent review or finding closure.
No interpreter installation, admin action, provider, or browser invocation occurs.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import venv


PUBLIC_URL = "https://github.com/felixvonvollmer-png/Firefox---WindowSafe.git"
BASE = "4ba2c473fe4d90c85d94ee2b2f5cc5777d115109"
RUN_START = "9b6dd621deec1193bfdfbdfa730e8f9349c73fd6"


def prepare(destination, sha):
    if platform.python_implementation() != "CPython" or sys.version_info[:3] != (3, 14, 4):
        raise ValueError("ENVIRONMENT_BLOCKED: actual CPython 3.14.4 required")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise ValueError("full candidate SHA required")
    destination = destination.absolute()
    destination.mkdir(mode=0o700)  # Exclusive; never reuse or overwrite another context.
    repo = destination / "repository"
    report = {
        "status": "ENVIRONMENT_BLOCKED", "evidence_class": "LOCAL_AGENT_REPORTED",
        "purpose": "ENVIRONMENT_PREPARATION_NOT_INDEPENDENT_REVIEW",
        "subject_sha": sha, "cumulative_base": BASE, "run_start": RUN_START,
        "F02": "OPEN_REQUIRES_FUTURE_INDEPENDENT_PREFLIGHT_AND_FINAL_RESULT_VALIDATION",
        "public_clone_source": PUBLIC_URL, "directory": str(destination),
        "runtime": {"implementation": platform.python_implementation(), "version": platform.python_version(),
                    "base_executable": str(Path(sys.executable).resolve()),
                    "base_executable_sha256": hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
                    "platform": platform.platform()},
        "commands": [],
    }

    def run(argv, cwd=destination, extra_env=None):
        result = subprocess.run([str(a) for a in argv], cwd=cwd, env=dict(os.environ, GIT_TERMINAL_PROMPT="0", **(extra_env or {})),
                                capture_output=True, text=True, timeout=240)
        report["commands"].append({"argv": [str(a) for a in argv], "cwd": str(cwd),
                                   "extra_env": extra_env or {}, "exit": result.returncode,
                                   "stdout": result.stdout, "stderr": result.stderr})
        if result.returncode:
            raise ValueError("ENVIRONMENT_BLOCKED: preparation command failed; inspect preparation.json")
        return result.stdout.strip()

    try:
        report["git_version"] = run(["git", "--version"])
        run(["git", "clone", "--no-checkout", PUBLIC_URL, repo])
        run(["git", "checkout", "--detach", sha], repo)
        run(["git", "remote", "set-url", "--push", "origin", "DISABLED_READ_ONLY"], repo)
        if run(["git", "rev-parse", "--is-shallow-repository"], repo) != "false":
            raise ValueError("full Git history required")
        for commit in (BASE, RUN_START, sha):
            run(["git", "cat-file", "-e", commit + "^{commit}"], repo)
        run(["git", "merge-base", "--is-ancestor", BASE, RUN_START], repo)
        run(["git", "merge-base", "--is-ancestor", RUN_START, sha], repo)
        run(["git", "fsck", "--full"], repo)
        report["subject_tree"] = run(["git", "rev-parse", sha + "^{tree}"], repo)
        venv.EnvBuilder(with_pip=False).create(destination / "runtime")
        python = destination / "runtime/bin/python"
        report["runtime"]["prepared_executable"] = str(python)
        run([python, "-c", "import platform,sys; assert platform.python_implementation() == 'CPython'; assert sys.version_info[:3] == (3,14,4); print(sys.version)"], repo)
        tool = [python, "tools/foundation.py"]
        request = run([*tool, "request", "--sha", sha], repo)
        (destination / "review-request.json").write_text(request + "\n")
        contract = subprocess.check_output(["git", "show", sha + ":reviews/review-contract.json"], cwd=repo)
        (destination / "review-contract.json").write_bytes(contract)
        run([*tool, "schema-preflight", "--sha", sha, "--schema", destination / "review-contract.json"], repo)
        run([*tool, "check"], repo)
        run([python, "-m", "unittest", "discover", "-s", "tests", "-v"], repo)
        run([*tool, "build", "--verify-repeat"], repo)
        for result in ("WS-PFR-20260917-01", "WS-PFR-20260918-01"):
            run([*tool, "validate-result", "--file", "reviews/results/" + result + ".json"], repo)
        run([*tool, "history", "--base", BASE], repo)
        run([*tool, "history", "--event-base"], repo, {"FOUNDATION_EVENT_BASE": "0" * 40})
        run(["git", "diff", "--check"], repo)
        if run(["git", "status", "--porcelain"], repo):
            raise ValueError("prepared checkout must remain clean")
        report["status"] = "PREPARED_REQUIRES_INDEPENDENT_EXECUTION"
    finally:
        (destination / "preparation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "subject_sha": sha, "record": str(destination / "preparation.json"),
                      "python": report["runtime"]["prepared_executable"], "repository": str(repo), "F02": report["F02"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    try:
        prepare(args.destination, args.sha)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print("ENVIRONMENT_BLOCKED:", str(error), file=sys.stderr)
        sys.exit(1)
