"""Topic: does the repo avoid the pull_request_target event in its GitHub workflows?

Its detection text, in pull_request_target.md, is written for the whole Jupyter community: it explains the risk and
what to do, with links.
"""

from topics import DONE, MISSING, NOT_APPLICABLE, PARTIAL, Result, Topic, markdown


def check(repo: dict, scan: dict) -> Result:
    workflows = scan[repo["full_name"]]["workflows"]
    if not workflows["count"]:
        return Result(NOT_APPLICABLE, "No GitHub workflows.")
    reviewed = workflows["pull_request_target"]  # workflow -> whether a zizmor comment marks it as reviewed
    if not reviewed:
        return Result(DONE, "No workflow runs on pull_request_target.")
    if all(reviewed.values()):
        reason = "All workflows have a zizmor ignore comment: it needs a policy that allows pull_request_target."
        return Result(PARTIAL, reason, evidence=sorted(reviewed))
    unmarked = sorted(path for path, ok in reviewed.items() if not ok)
    workflow = "workflow uses" if len(unmarked) == 1 else "workflows use"
    reason = f"{len(unmarked)} {workflow} pull_request_target without a zizmor ignore comment."
    return Result(MISSING, reason, evidence=unmarked)


TOPIC = Topic(
    id="pull-request-target",
    title="pull_request_target",
    question="Do the repository's GitHub workflows avoid the pull_request_target event?",
    detection=markdown(__file__),
    meanings={
        DONE: "None of its workflows runs on `pull_request_target`.",
        PARTIAL: (
            "Its workflows that run on `pull_request_target` are all marked as reviewed with a zizmor ignore comment."
            " It needs an event policy that allows the event."
        ),
        MISSING: (
            "At least one of its workflows runs on `pull_request_target` and does not have a zizmor ignore comment."
        ),
        NOT_APPLICABLE: "The repository has no GitHub workflows.",
    },
    check=check,
)
