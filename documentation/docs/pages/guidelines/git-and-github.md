## Branches
### Permanent branches
Permanent branches should contain two default branches:
* `main` (or `master` for legacy repositories)
  * Fully tested code ready for release
* `development`
  * For release-candidate code ready to be tested

### Adding features and creating feature branches
To add a new feature to an existing `development` branch, first create an [issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues) to both describe the new feature and/or problem being solved, and generate a unique issue number for tracking. Feature branches should be as short-lived as possible and reference an issue directly (where possible). Issues should be closed when feature branches are merged or terminated.

### Fork management
A workflow has been developed to enable ACCESS-NRI to be a MOM6 node whilst having flexibility to have releases that differ from the Mom-ocean repository, this workflow may be applicable to other development efforts where there is an interest in contributing to upstream development efforts. Further details of the [workflow are here](https://github.com/ACCESS-NRI/MOM6/wiki). 

### Naming
All feature branches should be named using the [repository naming convention](../policies/repository-management.md#naming) prefixed with a unique issue number.

`[issue number]-[short-name-separated-by-hyphens]`

Examples:
* `9-some-issue`
* `12-some-other-issue`

See [here](https://deepsource.io/blog/git-branch-naming-conventions/#1-use-issue-tracker-ids-in-branch-names).

For model configuration repositories, where branches in the repository represent different model configurations, use the branch being merged into in the issue branch name.

`[issue number]-[target branch name]`

Examples:
* `21-dev-025deg_jra55do_ryf` for issue 21's changes of `dev-025deg_jra55do_ryf` branch
* `99-dev-preindustrial+concentrations`

## Pull Requests
### Reviewers
* Check that the Pull Request is actually "green-lit" for review before reviewing.
* Checkout the PR branch and inspect entire files as required. e.g. Search for variables that have been removed.
* The task of the reviewer is to review code, not to trigger the merge.
### Assignees
* The creator of the PR shall include details of the testing that was completed.
* The Assignee is responsible for triggering the merge.

## Issues
### Guidelines for creating issues

1. **Be clear and concise**: Explain the problem or issue in as few words as possible. Be specific and provide all relevant details.
2. **Short and descriptive title**: The title is the most visible part of your issue, you want it short and to the point.
3. **Provide context:** Explain why the problem is important and how it affects you or others. Provide any relevant background information that will help others understand the issue.
4. **Provide a way to reproduce the issue:** Clearly outline the steps needed to reproduce the issue, and provide any relevant logs or error messages. Ideally include a [Minimal Complete Verifiable Example (MCVE)](http://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports).
5. **Include relevant files or code:** If the issue is related to a specific file or piece of code, include it in the issue description.
6. **Provide a desired outcome:** Explain what you expect to happen when the issue is resolved.
7. **Use proper grammar and spelling:** Poor grammar and spelling can make it difficult for others to understand your issue, so be sure to proofread your message before submitting it.
8. **Be respectful:** Treat others as you would like to be treated. Be respectful and polite in your interactions with others, even if you are frustrated or upset.
9. **Use relevant labels:** Use relevant labels to help others quickly identify the type of issue you are reporting.
10. **Provide updates:** Keep the issue updated as you continue to work on it, and provide any additional information that may be helpful to others.

By following these guidelines, you can help ensure that your GitHub issue is clear, concise, and easy for others to understand and work on.

### Guidelines

Empty issues are an anti-pattern. There should be some descriptive text in the body of the issue. Not only is it good practice, an empty issue sends a message, and it isn't a good one.

Pull requests should always be associated with an issue. The issue is for outlining the problem, discuss approaches and background. The pull request is where the codebase is updated to fix the related issue, including detailed code review.
