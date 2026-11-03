To help with discoverability, all the repositories in the ACCESS-NRI GitHub organisation must use appropriate topic tags.

## Introduction

Our GitHub organisation has well over 100 repositories and it can be difficult to browse or find repositories:

https://github.com/orgs/ACCESS-NRI/repositories?type=all

As an organisation we are using topic tags on repositories to help with discovery. The topics we use are divided into different categories. The categories are listed bellow, along with the corresponding topics currently in use. If you can't find an appropriate topic for you repository in this list, please get in touch with the ACCESS-NRI GitHub management group before creating a new topic.

See [Using topics to search for repositories](../documentation/managing-repositories.md#using-topics-to-search-for-repositories) for examples of searches using topics.

## Models

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

## Type

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

## Deployment method

For repositories that have the `deployment` or `documentation` topics, through what means are they deployed. Current options are:
- `conda`: a conda environment
- `spack`: software installed via spack 
- `github-pages`: a website deployed using GitHub Pages
- `readthedocs`: documentation deployed using Read the Docs.

## Earth systems

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

## Other

These topics include properties not covered by the previous categories. For example, repositories that are forks should have the `fork` topic.

Currently this category includes the following topics:
- `fork`: this repository is a fork
- `template`: this repository is a template
- `payu`: configurations using payu for workflow management
- `cylc`: configurations using cylc for workflow management
- `inputs`: this repository is related to model inputs

## Reserved

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

## Deprecated topics

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
