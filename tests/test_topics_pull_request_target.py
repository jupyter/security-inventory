"""Tests for scripts/topics/pull_request_target.py."""

from topics import pull_request_target


def status(reviewed, disabled=()):
    scan = {"a": {"workflows": {"count": 2, "pull_request_target": reviewed, "disabled": list(disabled)}}}
    return pull_request_target.check({"full_name": "a"}, scan).status


def test_a_repo_is_partial_only_when_every_pull_request_target_workflow_is_marked_as_reviewed():
    assert status({}) == "done"
    assert status({"label.yml": True, "binder.yml": True}) == "partial"
    assert status({"label.yml": True, "binder.yml": False}) == "missing"


def test_a_disabled_workflow_counts_as_reviewed():
    assert status({"label.yml": True, "binder.yml": False}, disabled=["binder.yml"]) == "partial"
    assert status({"label.yml": False, "binder.yml": False}, disabled=["binder.yml"]) == "missing"


def test_a_missing_repo_lists_the_workflows_to_fix_and_to_delete():
    reviewed = {"label.yml": True, "binder.yml": False, "fix.yml": False}
    scan = {"a": {"workflows": {"count": 3, "pull_request_target": reviewed, "disabled": ["fix.yml"]}}}
    result = pull_request_target.check({"full_name": "a"}, scan)
    assert result.evidence == ["binder.yml", "fix.yml"]
    assert result.reason.endswith("fix.yml is disabled.")


def test_a_partial_repo_names_the_reviewed_and_the_disabled_workflows():
    scan = {"a": {"workflows": {"count": 3, "pull_request_target": {"label.yml": True, "fix.yml": False}}}}
    scan["a"]["workflows"]["disabled"] = ["fix.yml"]
    reason = pull_request_target.check({"full_name": "a"}, scan).reason
    assert reason == "label.yml has a zizmor ignore comment. fix.yml is disabled."
