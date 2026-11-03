## Introduction

There are two recommended versioning schemes for software - semantic versioning (SemVer) and calendar versioning.
There is one recommended versioning scheme for `json` schemas - SchemaVer.  

## Versioning Types

### Semantic versioning

[Semantic versioning](https://semver.org/), which uses the familiar MAJOR.MINOR.PATCH numeric version string.

From the website summary:

> Given a version number MAJOR.MINOR.PATCH, increment the:
> 
> MAJOR version when you make incompatible API changes
> MINOR version when you add functionality in a backwards compatible manner
> PATCH version when you make backwards compatible bug fixes
>
> Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

### Calendar versioning

[Calendar versioning](https://calver.org) uses date based versioning. There is a wider spread of usage, but an example is Ubuntu which uses YY.0M, e.g. 4.10 was their first release in October 2004.

From the website summary:

> Different projects use different systems for versioning, but common practices have emerged. For instance, point-separated numbers (e.g., 3.1.4) are all but given. Another common versioning pattern incorporates a time-based element, usually part of the release date.
>
> This date-based approach has come to be called Calendar Versioning, or CalVer for short.

### SchemaVer

[SchemaVer](https://docs.snowplow.io/docs/pipeline-components-and-applications/iglu/common-architecture/schemaver/) uses a versioning schema that is similar to SemVer. As noted by their website:
> Given a version number `MODEL-REVISION-ADDITION`, increment the:
>    * `MODEL` when you make a breaking schema change which will prevent interaction with any historical data
>    * `REVISION` when you make a schema change which may prevent interaction with some historical data
>    * `ADDITION` when you make a schema change that is compatible with all historical data


## Versioning Artifacts

### Models

In the absence of an existing versioning scheme [calendar versioning](https://calver.org/) is the preferred versioning scheme. Models do not usually have a clear API, which is a specific requirement of semantic versioning. Calendar versioning has the benefit of being able to infer the time when the code was released, which is useful by itself, but also has utility for comparing with known efforts within the community, e.g. important studies, CMIP and IPCC releases etc.

The recommended version is `YYYY.0M.MINOR` where `MINOR` is a zero-padded 3 digit number, starting at 000 and incremented for subsequent versions in the same year+month. It is 3 digits rather than 2 to remove ambiguity that it might represent zero-padded day (see [related discussion](https://github.com/ACCESS-NRI/ACCESS-OM/issues/6#issuecomment-1478909140)). There can be a Spack release tag. e.g. `YYYY.0M.MINOR-RELEASE`. 

If the new minor version is released in a different month to the current version, it is permissable to only increment the minor version and leave the month as is, to indicate that the versions are closely related. Closely related is ambiguous, but an example might be if the changes in the latest release are further modifications to code that was changed or added in the previous version. In this case it makes sense to bundle the changes under a single major version update. This is to indicate that the new release is closely related to the previous and only a minor modification.

### Model configurations

Model configurations, e.g. [ACCESS-OM2](https://github.com/ACCESS-NRI/access-om2-configs), use a specific version of a model but can change configuration options independent of model version <a href="#note1" id="note1ref"><sup>1</sup></a>. As a result model configurations need to be versioned independently of the model version.

Model configurations are versioned with a modified semantic versioning approach, with just `MAJOR` and `MINOR` version numbers. For model configurations `MAJOR` version is incremented when a change is made that causes the configuration to no longer be bit reproducible. `MINOR` version is incremented when there is a change that does not break bit reproducibility.

This gives user certainty that they can use any model configuration version with the same major version and be confident it will be bit reproducible. A user can also see when the minor version changes, alerting them to the fact that there have been some changes that could affect them, and they should consult the GitHub release page for more information.

### Software

Software should us semantic versioning where possible.

### `json` Schema

`json` schema should use SchemaVer where possible. 


<a id="note1" href="#note1ref"><sup>1</sup></a> In some cases changes in configuration options are tied to changes in a component of model, and therefore related to specific model versions.