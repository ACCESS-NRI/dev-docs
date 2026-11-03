!!! info "Policy status"
    **Status:** agreed by the GitHub Management Group in [dev-docs#40](https://github.com/ACCESS-NRI/dev-docs/issues/40) (November 2025) and [dev-docs#41](https://github.com/ACCESS-NRI/dev-docs/issues/41) (April 2026).

ACCESS-NRI manages two GitHub organisations: 
 - [ACCESS-NRI](https://github.com/ACCESS-NRI)
 - [ACCESS Community Hub](https://github.com/ACCESS-Community-Hub/)

The policies on this page apply to the ACCESS-NRI GitHub organisation.

## Overview

Our GitHub organization follows a decentralized repository management model. In this model every repository has at least two designated individual admins responsible for managing access and permissions, while the creation of repositories is centralized.

The goals of this approach are to improve security, clarify responsibilities, and empower staff with a stronger sense of ownership.

## Policy

1. Repository Administration
   - Each repository must have at least two individual admins (not teams).
   - Repository admins are responsible for managing user permissions for their repositories.
2. Default Access
   - All staff members are only granted read-only access to all repositories by default.
3. Repository Creation
   - Only organization admins can create new repositories.
   - Requests for new repositories should be addressed to the ACCESS-NRI GitHub management group (see Communication channels bellow)
   - Once a repository is created, organisation admins will assign initial repository admins.

## Roles and Responsibilities
- Repository Admins
  - Manage access permissions for their repository.
  - Decide who has write or maintainer privileges.
  - Ensure repository policies and best practices are followed.
  - Act as the final authority for changes in their repository.
- Organisation Admins
  - Create new repositories.
  - Assign initial repository admins.
  - Provide support and guidance on organisational policies.

## Benefits of this Structure
- Improved Security: Reduces risks from mistakes or compromised accounts by limiting default permissions.
- Clear Decision-Making: Establishes who has the final say on changes in each repository and clarifies who can/should approve pull requests by identifying who has write access.
- Distributed Responsibility: Shares the workload of repository management across multiple admins.
- Stronger Ownership: gives staff members direct responsibility and authority over repositories.
- Consistent Policy Enforcement: Ensures new repositories follow organisational standards from the start.

## Communication channels

- Requests, questions and announcement regarding the GitHub management should be done on the ["GitHub Management" channel](https://access-nri.zulipchat.com/#narrow/channel/473028-GitHub-Management) on Zulip.
- Requests and questions regarding specific repositories can be done:
  - using the ["GitHub Management" channel](https://access-nri.zulipchat.com/#narrow/channel/473028-GitHub-Management) on Zulip. In that case, make sure you use the appropriate topics or create a new one with an approprate title.
  - By creating a GitHub issue in the appropriate repository.
  - By directly contacting the repository administrators on Zulip or via email. This should only be done if the administrators have added information about how to contact them in the repository's Readme.

## Repository administration

Use the [new repository check-list](../documentation/managing-repositories.md#new-repository-check-list) when setting up a new repository.

### Repository administrators

As stated in the [GitHub management policy](#policy), each repository must have at least two individual administrators. These cannot be teams and there needs to be a very compelling reason for an external user to be made an administrator. The organisation administrators must validate the reason to add an external user as a repository administrator.

### User permissions

We recommend users be given permissions on need basis. That means, for example, that write permissions to a repository should only be given if a user needs those permissions for their work. Repository administrators are free to assign any role to members for the good management of their repositories.

See [User permissions](../documentation/managing-repositories.md#user-permissions) for what read and write permissions allow.

### Branch protections

At a minimum, the default branch of a public repository should always be protected. See [Branch protections](../documentation/managing-repositories.md#branch-protections) for the recommended rulesets.

### Topics

All repositories should be tagged with [the appropriate topics](topic-tags.md) for better discoverability.

### Private repositories

Private repositories should only be used for licensing or security reasons. The same policies and best practices apply to private and public repositories, except for branch protection which is not available for private repositories. If the repository is private for licensing reasons, the documentation must clearly indicate which proprietary licence is used and how to get access.

## Repository creation and naming
In the first instance, all repositories should be created using the ACCESS-NRI [General Repository Template](https://github.com/ACCESS-NRI/template) which contains the correct software COPYRIGHT and LICENSE information.
Repositories should always have a `README.md` providing a description of the repo purpose, content and any useful links / references. The more detailed documentation that can be provided here the better.
### Naming
Repository names should have unique, all lower-case names with words separated by hyphen/dashes. Ideally repo names should be as semantic as possible. 
Examples: 
* `repo`
* `my-repo`
* `my-more-complex-repo`
