"""Topic: does the repo avoid the pull_request_target event in its GitHub workflows?

A pull_request_target workflow runs with the base repo's secrets and a write token, even for a pull request from a
fork. If it checks out or runs the pull request's code, anyone who opens one can take over the repo. GitHub is turning
the event off by default, so a repo that uses it should move to pull_request, or check that it is safe and keep it on.
"""

from topics import DONE, MISSING, NOT_APPLICABLE, PARTIAL, Result, Topic

EVENT = "pull_request_target"


def check(repo: dict, scan: dict) -> Result:
    workflows = scan[repo["full_name"]]["workflows"]
    if not workflows["count"]:
        return Result(NOT_APPLICABLE, "No GitHub workflows.")
    if EVENT in workflows["triggers"]:
        return Result(MISSING, f"A workflow runs on {EVENT}.")
    return Result(DONE, f"No workflow runs on {EVENT}.")


TOPIC = Topic(
    id="pull-request-target",
    title="pull_request_target",
    question="Do the repository's GitHub workflows avoid the pull_request_target event?",
    detection=(
        'We read the events in the "on" key of each workflow in .github/workflows. A pull_request_target workflow'
        " runs with the repository's secrets and a write token, even for pull requests from forks. GitHub now turns"
        " the event off by default; see"
        " https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target."
    ),
    meanings={
        DONE: "None of its workflows runs on pull_request_target.",
        PARTIAL: "Not used: a workflow runs on the event or not.",
        MISSING: "At least one of its workflows runs on pull_request_target.",
        NOT_APPLICABLE: "The repository has no GitHub workflows.",
    },
    check=check,
)
