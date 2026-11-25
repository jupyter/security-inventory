A workflow that runs on `pull_request_target` gets the repository's secrets and a token that can write to it, even for a pull request that anyone opened from a fork. That is safe as long as the workflow never runs the pull request's code. If it checks out that code and then builds, tests or installs it, anyone can open a pull request that steals the secrets or pushes to the repository.

GitHub will by default start blocking workflow runs triggered by the `pull_request_target` event starting December 2, 2026 (though we may extend that deadline with an org-wide policy).

Most workflows can move to the `pull_request` event, which runs without secrets for pull requests from forks. Some need `pull_request_target`, like ones that label pull requests or post checks on them. Keep those only if they never run the pull request's code, and mark each one as reviewed with a `# zizmor: ignore[dangerous-triggers]` comment. A repository whose `pull_request_target` workflows are all marked shows as partial: it still needs an event policy that allows the event. Read more in [GitHub's guide to `pull_request_target`](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target), and see which runs the policy would block with [policy insights](https://docs.github.com/en/actions/how-tos/administer/control-workflow-execution).

To detect workflows using `pull_request_target`, we look for `pull_request_target` in the `on` key of each workflow in `.github/workflows`, and for the zizmor comment anywhere in the workflow:

```yaml
on:
  pull_request_target:  # zizmor: ignore[dangerous-triggers] only adds labels, runs no code from the pull request
    ...
```
