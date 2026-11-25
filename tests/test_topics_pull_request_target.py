"""Tests for scripts/topics/pull_request_target.py."""

from topics import pull_request_target


def status(reviewed):
    scan = {"a": {"workflows": {"count": 2, "pull_request_target": reviewed}}}
    return pull_request_target.check({"full_name": "a"}, scan).status


def test_a_repo_is_partial_only_when_every_pull_request_target_workflow_is_marked_as_reviewed():
    assert status({}) == "done"
    assert status({"label.yml": True, "binder.yml": True}) == "partial"
    assert status({"label.yml": True, "binder.yml": False}) == "missing"
