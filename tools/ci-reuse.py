#!/usr/bin/env python3
"""Conservatively reuse successful PR jobs for task-document-only followups."""
import io
import json
import os
import re
import subprocess
import sys
import zipfile

SHA = re.compile(r"^[0-9a-f]{40}$")
DOC = re.compile(r"^TaskFlowDocs/(?:achieved/)?\d{4}-\d{2}-\d{2}-[^/]+/(?:[^/]+/)*[^/]+\.md$")
JOBS = {
    "smoke": ("smoke (ubuntu-latest)", "smoke (macos-latest)", "smoke (windows-latest)"),
    "release": ("release",),
    "evals": ("evals",),
}


def run(*args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5).stdout


def api(path):
    return json.loads(run("gh", "api", path))


def context():
    result = {key: os.environ.get("TF_CI_" + key.upper(), "") for key in ("repo", "pr", "base", "head", "run")}
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", result["repo"]):
        raise ValueError("invalid repository")
    if not all(result[k].isdigit() and int(result[k]) > 0 for k in ("pr", "run")):
        raise ValueError("invalid run or PR")
    if not SHA.fullmatch(result["base"]) or not SHA.fullmatch(result["head"]):
        raise ValueError("invalid commit")
    return result


def metadata_matches(meta, candidate, current):
    return (isinstance(meta, dict) and meta.get("repo") == current["repo"]
            and meta.get("pr") == current["pr"] and meta.get("base") == current["base"]
            and meta.get("head") == candidate.get("head_sha")
            and meta.get("run") == str(candidate.get("id"))
            and isinstance(meta.get("head"), str) and bool(SHA.fullmatch(meta["head"]))
            and candidate.get("event") == "pull_request" and candidate.get("status") == "completed" and candidate.get("conclusion") == "success"
            and (candidate.get("head_repository") or {}).get("full_name") == current["repo"])


def docs_only(raw):
    paths = raw.split(b"\0")
    if not paths or paths[-1] != b"":
        return False
    paths = paths[:-1]
    try:
        return bool(paths) and all(DOC.fullmatch(p.decode("utf-8")) for p in paths)
    except UnicodeDecodeError:
        return False


def successful_jobs(jobs, expected_head):
    names = [job.get("name") for job in jobs]
    return {job.get("name") for job in jobs if names.count(job.get("name")) == 1
            and job.get("head_sha") == expected_head and job.get("status") == "completed"
            and job.get("conclusion") == "success"}


def metadata_from_artifact(repo, artifact):
    if artifact.get("expired") or not 0 < artifact.get("size_in_bytes", 0) <= 16384:
        raise ValueError("unusable artifact")
    archive = run("gh", "api", f"repos/{repo}/actions/artifacts/{artifact['id']}/zip")
    if len(archive) > 16384:
        raise ValueError("oversized artifact")
    with zipfile.ZipFile(io.BytesIO(archive)) as data:
        entries = data.infolist()
        if len(entries) != 1 or entries[0].filename != "metadata.json" or entries[0].file_size > 4096:
            raise ValueError("invalid artifact contents")
        return json.loads(data.read(entries[0]))


def find_reusable(current):
    repo = current["repo"]
    runs = api(f"repos/{repo}/actions/workflows/hooks.yml/runs?event=pull_request&status=success&per_page=20").get("workflow_runs", [])
    checked = 0
    for candidate in runs:
        if str(candidate.get("id")) == current["run"] or not SHA.fullmatch(candidate.get("head_sha", "")):
            continue
        if (candidate.get("head_repository") or {}).get("full_name") != repo:
            continue
        try:
            old = candidate["head_sha"]
            run("git", "merge-base", "--is-ancestor", old, current["head"])
            if not docs_only(run("git", "diff", "--no-renames", "--name-only", "-z", old, current["head"])):
                continue
            # The prior PR must not control the workflow, metadata writer or
            # earlier classifier that produced its claimed baseline.
            run("git", "diff", "--quiet", current["base"], old, "--", ".github/workflows/hooks.yml", "tools/ci-reuse.py", "tools/workflow-affected")
            checked += 1
            if checked > 3:
                break
            artifacts = api(f"repos/{repo}/actions/runs/{candidate['id']}/artifacts?per_page=100").get("artifacts", [])
            match = next((a for a in artifacts if a.get("name") == "taskflow-ci-" + str(candidate["id"])), None)
            if not match or not metadata_matches(metadata_from_artifact(repo, match), candidate, current):
                continue
            job_data = api(f"repos/{repo}/actions/runs/{candidate['id']}/jobs?per_page=100&filter=latest")
            jobs = job_data.get("jobs", [])
            if job_data.get("total_count") != len(jobs):
                continue
            passed = successful_jobs(jobs, old)
            result = {key: all(name in passed for name in names) for key, names in JOBS.items()}
            if any(result.values()):
                return result, candidate["html_url"]
        except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError, zipfile.BadZipFile, json.JSONDecodeError):
            continue
    return {key: False for key in JOBS}, ""


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "write":
        with open(sys.argv[2], "w", encoding="utf-8") as out:
            json.dump(context(), out)
        return
    result, source = {key: False for key in JOBS}, ""
    try:
        result, source = find_reusable(context())
    except (ValueError, KeyError, TypeError, OSError, subprocess.SubprocessError, zipfile.BadZipFile, json.JSONDecodeError):
        pass
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
        for key, value in result.items():
            out.write(f"reuse_{key}={'true' if value else 'false'}\n")
    print("Previous successful run: " + source if source and any(result.values()) else "No reusable run; normal checks apply.")
    if source and any(result.values()):
        print("Reused jobs: " + ", ".join(key for key, value in result.items() if value))


if __name__ == "__main__":
    main()
