"""Topic: does the repo avoid the pull_request_target event in its GitHub workflows?

Its detection text, in pull_request_target.md, is written for the whole Jupyter community: it explains the risk and
what to do, with links.
"""

from pathlib import PurePosixPath

from topics import DONE, MISSING, NOT_APPLICABLE, PARTIAL, Result, Topic, markdown


def check(repo: dict, scan: dict) -> Result:
    workflows = scan[repo["full_name"]]["workflows"]
    if not workflows["count"]:
        return Result(NOT_APPLICABLE, "No GitHub workflows.")
    reviewed = workflows["pull_request_target"]  # workflow -> whether a zizmor comment marks it as reviewed
    if not reviewed:
        return Result(DONE, "No workflow runs on pull_request_target.")
    disabled = set(workflows.get("disabled", []))  # missing from scans made before step 2 asked GitHub
    unmarked = sorted(path for path, ok in reviewed.items() if not ok and path not in disabled)
    if not unmarked:
        off = sorted(path for path in reviewed if path in disabled)
        on = sorted(path for path in reviewed if path not in disabled)
        reasons = []
        if on:
            has, it = ("has", "it") if len(on) == 1 else ("have", "them")
            reasons.append(f"{names(on)} {has} a zizmor ignore comment: allow the event for {it} in a policy.")
        if off:
            is_, it = ("is", "it") if len(off) == 1 else ("are", "them")
            reasons.append(f"{names(off)} {is_} disabled: delete {it}.")
        return Result(PARTIAL, " ".join(reasons), evidence=sorted(reviewed))
    workflow = "enabled workflow uses" if len(unmarked) == 1 else "enabled workflows use"
    reason = f"{len(unmarked)} {workflow} pull_request_target without a zizmor ignore comment."
    return Result(MISSING, reason, evidence=unmarked)


def names(paths: list[str]) -> str:
    names = [PurePosixPath(path).name for path in paths]
    return names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"


TOPIC = Topic(
    id="pull-request-target",
    title="pull_request_target",
    question="Do the repository's GitHub workflows avoid the pull_request_target event?",
    detection=markdown(__file__),
    meanings={
        DONE: "None of its workflows runs on `pull_request_target`.",
        PARTIAL: (
            "Its workflows that run on `pull_request_target` are all disabled or marked as reviewed with a zizmor"
            " ignore comment. The enabled ones need an event policy that allows the event, and the disabled ones"
            " should be deleted."
        ),
        MISSING: (
            "At least one of its enabled workflows runs on `pull_request_target` and does not have a zizmor ignore"
            " comment."
        ),
        NOT_APPLICABLE: "The repository has no GitHub workflows.",
    },
    check=check,
    org_link=("policy insights", "https://github.com/organizations/{org}/settings/actions/rules/insights"),
)
