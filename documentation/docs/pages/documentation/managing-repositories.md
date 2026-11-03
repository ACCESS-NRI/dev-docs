ACCESS-NRI manages two GitHub organisations: 
 - [ACCESS-NRI](https://github.com/ACCESS-NRI)
 - [ACCESS Community Hub](https://github.com/ACCESS-Community-Hub/)

## ACCESS-NRI GitHub Organization

## Repository Management Policies

### Overview

Our GitHub organization follows a decentralized repository management model. In this model every repository has at least two designated individual admins responsible for managing access and permissions, while the creation of repositories is centralized.

The goals of this approach are to improve security, clarify responsibilities, and empower staff with a stronger sense of ownership.

### Policy

1. Repository Administration
   - Each repository must have at least two individual admins (not teams).
   - Repository admins are responsible for managing user permissions for their repositories.
2. Default Access
   - All staff members are only granted read-only access to all repositories by default.
3. Repository Creation
   - Only organization admins can create new repositories.
   - Requests for new repositories should be addressed to the ACCESS-NRI GitHub management group (see Communication channels bellow)
   - Once a repository is created, organisation admins will assign initial repository admins.

### Roles and Responsibilities
- Repository Admins
  - Manage access permissions for their repository.
  - Decide who has write or maintainer privileges.
  - Ensure repository policies and best practices are followed.
  - Act as the final authority for changes in their repository.
- Organisation Admins
  - Create new repositories.
  - Assign initial repository admins.
  - Provide support and guidance on organisational policies.

### Benefits of this Structure
- Improved Security: Reduces risks from mistakes or compromised accounts by limiting default permissions.
- Clear Decision-Making: Establishes who has the final say on changes in each repository and clarifies who can/should approve pull requests by identifying who has write access.
- Distributed Responsibility: Shares the workload of repository management across multiple admins.
- Stronger Ownership: gives staff members direct responsibility and authority over repositories.
- Consistent Policy Enforcement: Ensures new repositories follow organisational standards from the start.

### Communication channels

- Requests, questions and announcement regarding the GitHub management should be done on the ["GitHub Management" channel](https://access-nri.zulipchat.com/#narrow/channel/473028-GitHub-Management) on Zulip.
- Requests and questions regarding specific repositories can be done:
  - using the ["GitHub Management" channel](https://access-nri.zulipchat.com/#narrow/channel/473028-GitHub-Management) on Zulip. In that case, make sure you use the appropriate topics or create a new one with an approprate title.
  - By creating a GitHub issue in the appropriate repository.
  - By directly contacting the repository administrators on Zulip or via email. This should only be done if the administrators have added information about how to contact them in the repository's Readme.


## Topic tags

### Introduction

Our GitHub organisation has well over 100 repositories and it can be difficult to browse or find repositories:

https://github.com/orgs/ACCESS-NRI/repositories?type=all

As an organisation we are using topic tags on repositories to help with discovery. The topics we use are divided into different categories. The categories are listed bellow, along with the corresponding topics currently in use. If you can't find an appropriate topic for you repository in this list, please get in touch with the ACCESS-NRI GitHub management group before creating a new topic.

#### Models

These topics note that a given repository is associated with a climate model, either through being a model component, a deployment repository, model configurations, etc. Some examples:
  - ACCESS-NRI/ACCESS-OM2 has the `access-om2` topic, as it is the model's deployment repository.
  - ACCESS-NRI/MOM5 has the `access-esm1p5`, `access-esm1p6`, and `access-om2 topics` as it is a component of those models.

Topics in this category currently in use are:
- `access-am3`
- `access-cm2`
- `access-cm3`
- `access-esm1p5`
- `access-esm1p6`
- `access-esm3`
- `access-om2`
- `access-om3`
- `access-ram3`
- `access-issm`
- `cable`
- `roms`

#### Type

These topics note that a given repository is of a certain type, like a model component, documentation, a model configuration, etc. Some examples:
- ACCESS-NRI/ACCESS-OM2 has the `deployment` topic, as it is a model deployment repository.
- ACCESS-NRI/MOM5 has the `component` topic.

All repositories should have one of these topics assigned to them.

Topics in this category currently in use are:

- `actions`: GitHub actions to be used in CI/CD workflows
- `configuration`: repository storing model configurations
- `component`: model component code
- `deployment`: repository used to deploy software or webpages
- `documentation`: repository storing any type of documentation
- `evaluation`: scripts or code used for model evaluation
- `experiment`: repository storing logs from experiments using an ACCESS model
- `release-infrastructure`: code, tools and configuration files used to release and deploy software
- `reporting`: scripts and tools used for gathering and processing various types of information
- `tool`: software tools
- `visualisation`: scripts or code used for data visualisation

*Note:* the preference is to have only one type topic per repository. However, we know there are some special cases that require several types (e.g. configuration repositories with documentation will have `configuration`, `documentation`).

For documentation repositories, please add the `documentation` topic but not the `deployment` topic. Then add a deployment method topic (see below).

#### Deployment method

For repositories that have the `deployment` or `documentation` topics, through what means are they deployed. Current options are:
- `conda`: a conda environment
- `spack`: software installed via spack 
- `github-pages`: a website deployed using GitHub Pages
- `readthedocs`: documentation deployed using Read the Docs.

#### Earth systems

This notes that a given repository is relevant to a particular earth system. For example, ACCESS-NRI/ACCESS-OM2 has the `ocean`, `sea-ice`, and `biogeochemistry` topics.

Topics in this category currently in use are:
- `atmosphere`
- `biogeochemistry`
- `coupler`
- `cryosphere`
- `land`
- `ocean`
- `sea-ice`
- `waves`

#### Other

These topics include properties not covered by the previous categories. For example, repositories that are forks should have the `fork` topic.

Currently this category includes the following topics:
- `fork`: this repository is a fork
- `template`: this repository is a template
- `payu`: configurations using payu for workflow management
- `cylc`: configurations using cylc for workflow management
- `inputs`: this repository is related to model inputs

#### Reserved

 These are topics reserved for special ACCESS-NRI usage:
- `build-ci-enabled`
- `atmosphere-team`
- `data-team`
- `ism-team`
- `land-team`
- `med-team`
- `model-release-team`
- `no-backup`
- `ocean-team`
- `regional-ocean-team`
- `software-transformation-team`
- `user-training-team`

The `team` topics are used to indicate that at least one person from that team is managing the repository. 

#### Using topics to search for repositories

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

#### Deprecated topics

The following topics where used in the past, but should not be used anymore:

- `apache2`: deleted, as GitHub provides a license qualifier when searching for repositories.
- `carbon-cycle`: deleted, use `biogeochemistry` instead.
- `cmip7`: deleted, as the only repository that was using it, `CMIP7-Hackathon`, is archived and could be found by simply searching for "CMIP7", as that's part of the repository name.
- `coastri`: deleted, as the only repository using it, `CoastRI-ROMS`, could be found by simply searching for "CoastRI", as that's part of the repository name. Other topics, in particular `roms`, could also be used instead.
- `coupling`: merged with coupler.
- `deprecated`: deleted, as repositories should be archived instead.
- `grafana`: deleted.
- `ice-sheet`: deleted, use `cryosphere` instead.
- `infrastructure`: deleted, instead use `release-infrastructure` where appropriate.
- `jules`: deleted, as we don't support it stand-alone and is therefore not an ACCESS model.
- `library`: deleted, as unlikely someone would use it to search for something. Also, several packages can be build as libraries or as stand-alone executables (e.g.: MOM6), so could be misleading.
- `model`: deleted, as people should instead use the actual model name in combination with the `type` topics to find what they are looking for.
- `model-evaluation`: renamed to `evaluation`.
- `python`: deleted, as GitHub provides a language qualifier when searching for repositories.
- `reproducibility`: deleted.
- `testing`: deleted.
- `unified-model`: deleted, as models using the UM already have a name, even the atmosphere only (eg, ACCESS-AM).
- `working-group`: deleted, as there was only one repository using it, `WG_storage_admin`, and it can be found, for example, by searching for "WG".

## Repository administration recommended policies and best practices

### Repository administrators

As stated in the [GitHub management policy](#repository-management-policies), each repository must have at least two individual administrators. These cannot be teams and there needs to be a very compelling reason for an external user to be made an administrator. The organisation administrators must validate the reason to add an external user as a repository administrator.

### User permissions

We recommend users be given permissions on need basis. That means, for example, that write permissions to a repository should only be given if a user needs those permissions for their work. By default, all members of the ACCESS-NRI GitHub organisation have read permissions to all repositories in the organisation, including all private repositories. Read permissions allow users to:

- clone a repository
- create issues
- create a pull request from a fork

Write permissions are needed if a user needs to:

- push to the repository, including creating a new branch on the repository (not through a fork)
- use the pre-release infrastructure, as pre-release builds are not triggered for forks
- merge a pull request

Please refer to [GitHub documentation](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization#permissions-for-each-role) for a full description of the permissions for each role and details of other existing roles. Repository administrators are free to assign any role to members for the good management of their repositories.

### Branch protections

At a minimum, the default branch of a public repository should always be protected. You can find recommended rulesets [here](https://github.com/ACCESS-NRI/.github/tree/main/rulesets). You will need to first download the JSON file with your preferred ruleset and then import it to your new repository (see the README with the rulesets).

### Topics

All repositories should be tagged with [the appropriate topics](#topic-tags) for better discoverability.

### Security Settings

GitHub gives many security and code quality tools in the `Security and quality` tab above a repository. This is only accessible to Org/Repo Administrators. 

For example, the following may be of use:

* You can set up [Dependabot](http://docs.github.com/code-security/supply-chain-security/understanding-your-software-supply-chain/about-supply-chain-security#what-is-dependabot) to automatically scan (and open PRs) for dependency vulnerabilities (in many common formats, requirements.txt, packages.json, etc...)
* Or Code Scanning to detect common vulnerabilities and errors in the code itself
* Or Secret Protection so you are notified if you accidentally commit a secret - or make it so you can't push secrets to the codebase to begin with

See https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository for more info

### Private repositories

Private repositories should only be used for licensing or security reasons. The same policies and best practices apply to private and public repositories, except for branch protection which is not available for private repositories. If the repository is private for licensing reasons, the documentation must clearly indicate which proprietary licence is used and how to get access.

### New repository check-list

To ensure new repositories follow our policies and best-practices, we recommend using the following check-list when creating a new repository:

- [ ] Add at least two administrators to the repository
- [ ] Add relevant topics
- [ ] Add [branch protection rules](https://github.com/ACCESS-NRI/.github/tree/main/rulesets) and security settings
- [ ] Give users write permissions, on need basis
---