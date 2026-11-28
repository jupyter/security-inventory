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


def test_a_missing_repo_lists_only_the_workflows_to_fix():
    scan = {"a": {"workflows": {"count": 2, "pull_request_target": {"label.yml": True, "binder.yml": False}}}}
    assert pull_request_target.check({"full_name": "a"}, scan).evidence == ["binder.yml"]
