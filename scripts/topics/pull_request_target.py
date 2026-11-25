"""Topic: does the repo avoid the pull_request_target event in its GitHub workflows?

Its detection text, in pull_request_target.md, is written for the whole Jupyter community: it explains the risk and
what to do, with links.
"""

from topics import DONE, MISSING, NOT_APPLICABLE, PARTIAL, Result, Topic, markdown


def check(repo: dict, scan: dict) -> Result:
    workflows = scan[repo["full_name"]]["workflows"]
    if not workflows["count"]:
        return Result(NOT_APPLICABLE, "No GitHub workflows.")
    if "pull_request_target" in workflows["triggers"]:
        return Result(MISSING, "A workflow runs on pull_request_target.")
    return Result(DONE, "No workflow runs on pull_request_target.")


TOPIC = Topic(
    id="pull-request-target",
    title="pull_request_target",
    question="Do the repository's GitHub workflows avoid the pull_request_target event?",
    detection=markdown(__file__),
    meanings={
        DONE: "None of its workflows runs on `pull_request_target`.",
        PARTIAL: "Not used: a workflow runs on the event or not.",
        MISSING: "At least one of its workflows runs on `pull_request_target`.",
        NOT_APPLICABLE: "The repository has no GitHub workflows.",
    },
    check=check,
)
