ACCESS-NRI has a Readthedocs account, "access-nri". Ask for the credentials on Slack if you need to connect. This is to avoid having documentation that is linked to a specific user.

The accessnri account is linked to the access-bot GitHub user. It has access to the Github organisations:

* ACCESS-NRI
* ACCESS-Hive
* CABLE-LSM

It is possible to add more organisations, for this make sure to invite the access-bot user to your organisation.

It's possible to setup RTD from your own personal account and then add accessnri as a maintainer. Or to setup RTD directly from accessnri account if you don't have a RTD account.

## Setup automatic build from commit and preview for pull requests

You need to set up a webhook through an integration so that RTD can build the docs automatically for each commit. This also enables to build a preview for pull requests. To set up a webhook, you need to do it from the RTD account of one of the owners of the repo. It is preferable if access-bot is an owner of the repository as then permissions will always be granted even when people move on. If access-bot isn't/can't be an owner, add one of the owners as a maintainer on RTD:

* go to the project admin page on readthedocs, `https://readthedocs.org/dashboard/<project-name>/edit/`
* select `Maintainers`
* Invite the owner with their email address or RTD username
* Get the owner to accept the invite

From the account of the owner (access-bot or other), setup the integration:

* go to the project admin page
* go to `integrations`
* click `Add integration`
* choose GitHub incoming webhook

To get previews to build in pull requests, under `Advanced Settings`, select "Build pull requests for this project".
