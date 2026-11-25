"""Topic: does the repo avoid the pull_request_target event in its GitHub workflows?

Its detection text is written for the whole Jupyter community: it explains the risk and what to do, with links.
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
        "A workflow that runs on pull_request_target gets the repository's secrets and a token that can write to it,"
        " even for a pull request that anyone opened from a fork. That is safe as long as the workflow never runs the"
        " pull request's code. If it checks out that code and then builds, tests or installs it, anyone can open a"
        ' pull request that steals the secrets or pushes to the repository. This is known as a "pwn request", and it'
        " has caused real supply-chain attacks."
        "\n\n"
        "GitHub now adds a default policy that blocks the event in public repositories without an Actions event"
        " policy of their own. For now it only records the runs it would block. GitHub plans to start blocking them"
        " on December 2, 2026, unless an organization or repository policy says otherwise."
        "\n\n"
        "Most workflows can move to the pull_request event, which runs without secrets for pull requests from forks."
        " Some need pull_request_target, like ones that label pull requests or post checks on them: keep those only if"
        " they never run the pull request's code, and allow the event in a policy. Read more in"
        " [GitHub's guide to pull_request_target]"
        "(https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target), and see which"
        " runs the policy would block with"
        " [policy insights](https://docs.github.com/en/actions/how-tos/administer/control-workflow-execution)."
        "\n\n"
        'We look for the event in the "on" key of each workflow in .github/workflows.'
    ),
    meanings={
        DONE: "None of its workflows runs on pull_request_target.",
        PARTIAL: "Not used: a workflow runs on the event or not.",
        MISSING: "At least one of its workflows runs on pull_request_target.",
        NOT_APPLICABLE: "The repository has no GitHub workflows.",
    },
    check=check,
)
