!!! info "Policy status"
    **Status:** moved from the wiki; formal approval not recorded.

## Actions Versioning

When we use actions and reusable workflows in GitHub Actions, we require certain levels of strictness for the version. 

We allow the following, from least to most strict:
* For ACCESS-NRI-internal actions (`access-nri/*` actions of any type) we allow any type of version reference. This includes branch references (including `@main`), tag references (`@2.0.1`) or commit references (`@as2u9e8u2e8u29eu9u8e29e`). This is because we these are developed in-house and are safely maintained. One use case for a less-restrictive version is that the `@main` branch reference can be employed so there are not as many pull requests to update the hashes for cross-repository actions/workflows. 
* For GitHub-published actions (`actions/*`) we allow major branch references (`@v5`), tag references (`@v5.0.1`) or commit references (`@3e892h2b983dhn239dj`). This is because these are core GitHub-created workflows and we have relative certainty as to their stability. 
* For any other action (`*/*`) we only allow commit references (`@r928jn2hdb293e2e298hd`) as we don't have any guarantee as to their stability, or the creators security policies. Although it isn't very readable, you can still put the tag that is associated with that commit in a comment (eg. `- uses some/action@o2udndj29d23jd29d298jdu32  # v0.2.1`).  

> [!IMPORTANT]
> Remember to _always_ pin the hashes of custom external third-party actions, _not_ the tag or branch, especially for actions that handle secrets. It is the only way to be certain that an action hasn't been maliciously changed. 
