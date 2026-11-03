## User permissions

By default, all members of the ACCESS-NRI GitHub organisation have read permissions to all repositories in the organisation, including all private repositories. Read permissions allow users to:

- clone a repository
- create issues
- create a pull request from a fork

Write permissions are needed if a user needs to:

- push to the repository, including creating a new branch on the repository (not through a fork)
- use the pre-release infrastructure, as pre-release builds are not triggered for forks
- merge a pull request

Please refer to [GitHub documentation](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization#permissions-for-each-role) for a full description of the permissions for each role and details of other existing roles.

## Branch protections

You can find recommended rulesets [here](https://github.com/ACCESS-NRI/.github/tree/main/rulesets). You will need to first download the JSON file with your preferred ruleset and then import it to your new repository (see the README with the rulesets).

## Security Settings

GitHub gives many security and code quality tools in the `Security and quality` tab above a repository. This is only accessible to Org/Repo Administrators. 

For example, the following may be of use:

* You can set up [Dependabot](http://docs.github.com/code-security/supply-chain-security/understanding-your-software-supply-chain/about-supply-chain-security#what-is-dependabot) to automatically scan (and open PRs) for dependency vulnerabilities (in many common formats, requirements.txt, packages.json, etc...)
* Or Code Scanning to detect common vulnerabilities and errors in the code itself
* Or Secret Protection so you are notified if you accidentally commit a secret - or make it so you can't push secrets to the codebase to begin with

See https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository for more info

## New repository check-list

To ensure new repositories follow our [policies](../policies/repository-management.md) and best-practices, we recommend using the following check-list when creating a new repository:

- [ ] Add at least two administrators to the repository
- [ ] Add relevant topics
- [ ] Add [branch protection rules](https://github.com/ACCESS-NRI/.github/tree/main/rulesets) and security settings
- [ ] Give users write permissions, on need basis

## Using topics to search for repositories

Here are some examples of searches using the topics.

All repositories related to ocean models:

https://github.com/search?q=topic%3Aocean+org%3AACCESS-NRI&type=Repositories

or sea-ice

https://github.com/search?q=topic%3Asea-ice+org%3AACCESS-NRI&type=Repositories

All spack deployment repositories:

https://github.com/search?q=topic%3Adeployment+topic%3Aspack+org%3AACCESS-NRI&type=repositories

All MOM related component code repositories:

https://github.com/search?q=org%3AACCESS-NRI+fork%3Atrue+topic%3Acomponent+MOM&type=repositories

Note that search function on GitHub, by default, does not include forks. To include forks in the search one needs to add the `fork:true` option.
