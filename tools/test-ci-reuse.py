#!/usr/bin/env python3
import importlib.util
import io
import json
import pathlib
import subprocess
import unittest
from unittest.mock import mock_open, patch
import zipfile

spec = importlib.util.spec_from_file_location("ci_reuse", pathlib.Path(__file__).with_name("ci-reuse.py"))
reuse = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reuse)

OLD, HEAD, BASE = "a" * 40, "b" * 40, "c" * 40
CURRENT = {"repo": "owner/repo", "pr": "12", "base": BASE, "head": HEAD, "run": "20"}
CANDIDATE = {"id": 19, "head_sha": OLD, "event": "pull_request", "status": "completed", "conclusion": "success",
             "head_repository": {"full_name": "owner/repo"}, "html_url": "https://example.invalid/run/19"}
META = {"repo": "owner/repo", "pr": "12", "base": BASE, "head": OLD, "run": "19"}
ARTIFACT = {"id": 1, "name": "taskflow-ci-19", "expired": False, "size_in_bytes": 200}
DOCS = b"TaskFlowDocs/2026-11-10-demo/plan.md\0"


class ReuseTests(unittest.TestCase):
    def test_only_task_markdown_is_eligible(self):
        self.assertTrue(reuse.docs_only(DOCS))
        for paths in (b"", b"TaskFlowDocs/todo.md\0", b"hooks/task\0", b"TaskFlowDocs/2026-11-10-demo/code.py\0", DOCS + b"hooks/task\0", b"\xff\0"):
            self.assertFalse(reuse.docs_only(paths))

    def test_identity_and_base_must_match(self):
        self.assertTrue(reuse.metadata_matches(META, CANDIDATE, CURRENT))
        for changes in ({"base": "d" * 40}, {"pr": "13"}, {"repo": "other/repo"}, {"head": "d" * 40}, {"run": "18"}):
            self.assertFalse(reuse.metadata_matches({**META, **changes}, CANDIDATE, CURRENT))
        self.assertFalse(reuse.metadata_matches(META, {**CANDIDATE, "head_repository": None}, CURRENT))
        self.assertFalse(reuse.metadata_matches(META, {**CANDIDATE, "status": "in_progress"}, CURRENT))

    def test_skipped_failed_and_duplicate_jobs_are_not_success(self):
        jobs = [{"name": "evals", "head_sha": OLD, "status": "completed", "conclusion": "skipped"},
                {"name": "release", "head_sha": OLD, "status": "completed", "conclusion": "success"},
                {"name": "release", "head_sha": OLD, "status": "completed", "conclusion": "failure"},
                {"name": "other", "head_sha": HEAD, "status": "completed", "conclusion": "success"}]
        self.assertEqual(reuse.successful_jobs(jobs, OLD), set())

    def test_valid_run_reuses_only_executed_jobs(self):
        jobs = [{"name": name, "head_sha": OLD, "status": "completed", "conclusion": "success"} for name in reuse.JOBS["smoke"] + reuse.JOBS["evals"]]
        jobs.append({"name": "release", "head_sha": OLD, "status": "completed", "conclusion": "skipped"})
        def api(path):
            if "/workflows/" in path:
                return {"workflow_runs": [CANDIDATE]}
            if "/artifacts?" in path:
                return {"artifacts": [ARTIFACT]}
            return {"jobs": jobs, "total_count": len(jobs)}
        def command(*args):
            if args[1] == "diff":
                if "--quiet" in args:
                    return b""
                self.assertIn("--no-renames", args)
                return DOCS
            return b""
        with patch.object(reuse, "api", side_effect=api), patch.object(reuse, "run", side_effect=command), patch.object(reuse, "metadata_from_artifact", return_value=META):
            result, source = reuse.find_reusable(CURRENT)
        self.assertEqual(result, {"smoke": True, "release": False, "evals": True})
        self.assertEqual(source, CANDIDATE["html_url"])

    def test_force_push_nonancestor_and_unavailable_api_fail_closed(self):
        with patch.object(reuse, "api", return_value={"workflow_runs": [CANDIDATE]}), patch.object(reuse, "run", side_effect=subprocess.CalledProcessError(1, "git")):
            result, source = reuse.find_reusable(CURRENT)
        self.assertFalse(any(result.values()))
        self.assertEqual(source, "")

    def test_skipped_followup_does_not_hide_earlier_success(self):
        earlier = {**CANDIDATE, "id": 18, "html_url": "https://example.invalid/run/18"}
        jobs = [{"name": name, "head_sha": OLD, "status": "completed", "conclusion": "success"} for name in reuse.JOBS["smoke"]]
        def api(path):
            if "/workflows/" in path:
                return {"workflow_runs": [CANDIDATE, earlier]}
            if "/artifacts?" in path:
                number = 19 if "/19/" in path else 18
                return {"artifacts": [{**ARTIFACT, "id": number, "name": f"taskflow-ci-{number}"}]}
            return {"jobs": [] if "/19/" in path else jobs, "total_count": 0 if "/19/" in path else len(jobs)}
        def metadata(repo, artifact):
            return {**META, "run": str(artifact["id"])}
        with patch.object(reuse, "api", side_effect=api), patch.object(reuse, "run", side_effect=lambda *a: DOCS if "--name-only" in a else b""), patch.object(reuse, "metadata_from_artifact", side_effect=metadata):
            result, source = reuse.find_reusable(CURRENT)
        self.assertTrue(result["smoke"])
        self.assertEqual(source, earlier["html_url"])

    def test_modified_metadata_writer_and_incomplete_jobs_fail_closed(self):
        def api(path):
            if "/workflows/" in path:
                return {"workflow_runs": [CANDIDATE]}
            if "/artifacts?" in path:
                return {"artifacts": [ARTIFACT]}
            return {"jobs": [], "total_count": 1}
        def command(*args):
            if "--quiet" in args:
                raise subprocess.CalledProcessError(1, "git diff")
            return DOCS if args[1] == "diff" else b""
        with patch.object(reuse, "api", side_effect=api), patch.object(reuse, "run", side_effect=command):
            result, _ = reuse.find_reusable(CURRENT)
        self.assertFalse(any(result.values()))
        with patch.object(reuse, "api", side_effect=api), patch.object(reuse, "run", side_effect=lambda *a: DOCS if "--name-only" in a else b""), patch.object(reuse, "metadata_from_artifact", return_value=META):
            result, _ = reuse.find_reusable(CURRENT)
        self.assertFalse(any(result.values()))

    def test_artifact_rejects_extra_files_and_expired(self):
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("metadata.json", "{}")
            z.writestr("../escape", "ignored")
        with patch.object(reuse, "run", return_value=archive.getvalue()):
            with self.assertRaises(ValueError):
                reuse.metadata_from_artifact("owner/repo", ARTIFACT)
            with self.assertRaises(ValueError):
                reuse.metadata_from_artifact("owner/repo", {**ARTIFACT, "expired": True})

    def test_reads_only_valid_metadata_artifact(self):
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, "w") as z:
            z.writestr("metadata.json", json.dumps(META))
        with patch.object(reuse, "run", return_value=archive.getvalue()):
            self.assertEqual(reuse.metadata_from_artifact("owner/repo", ARTIFACT), META)

    def test_main_api_failure_writes_false_outputs(self):
        output = mock_open()
        with patch.object(reuse, "context", return_value=CURRENT), patch.object(reuse, "find_reusable", side_effect=subprocess.CalledProcessError(1, "gh")), patch("builtins.open", output), patch.dict(reuse.os.environ, {"GITHUB_OUTPUT": "output"}), patch.object(reuse.sys, "argv", ["ci-reuse.py"]):
            reuse.main()
        writes = "".join(call.args[0] for call in output().write.call_args_list)
        self.assertEqual(writes, "reuse_smoke=false\nreuse_release=false\nreuse_evals=false\n")


if __name__ == "__main__":
    unittest.main()
