A workflow that is triggered by the `pull_request_target` event gets the repository's secrets and a token that can write to it. As long as the workflow does not ever run code from the pull request, this is safe. However, if the workflow runs any code from the PR (for example, checking out and building the PR's code), the PR can exfiltrate the secrets. Most workflows can move to the `pull_request` event, which runs without secrets for pull requests from forks. See [GitHub's guide to `pull_request_target`](https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target) and [zizmor's `dangerous-triggers` audit](https://docs.zizmor.sh/audits/#dangerous-triggers) for more info.

GitHub will start blocking workflow runs triggered by `pull_request_target` by default starting December 2, 2026 (though we may extend that deadline with an org-wide policy).

To detect workflows using `pull_request_target`, we look for `pull_request_target` in the `on` key of each workflow in `.github/workflows`, and we also look for a `zizmor: ignore[dangerous-triggers]` comment which indicates the workflow has been manually reviewed and judged safe.

Example of a workflow counted as `missing` and needs to be evaluated and fixed:

```yaml
on:
  pull_request_target:
    ...
```

Example of a workflow counted as `partial` since it has a zizmor comment indicating the workflow has been reviewed and judged safe. We will still need to set up a policy to allow the `pull_request_target` event.

```yaml
on:
  pull_request_target:  # zizmor: ignore[dangerous-triggers] only adds labels, runs no code from the pull request
    ...
```

To list the workflows in a repo that still need to be fixed, run this in the repo.

```sh
for f in .github/workflows/*.y*ml; do grep -qE '^ *(on:.*|- *)?pull_request_target' "$f" && ! grep -q 'zizmor: *ignore\[[^]]*dangerous-triggers' "$f" && echo "$f"; done
```
