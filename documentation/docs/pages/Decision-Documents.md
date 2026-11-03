## Background and Usage

This is a page for the creation of project-specific design decision documents for an enduring record of significant decisions made during throughout a given project. 

An example document is below:

| Name | Date | Context | Decision | Alternatives Considered |
|------|------|---------|----------|-------------------------|
| CI/CD Platform | 27/02/2025 | We need to pick a particular platform for CI/CD builds | Ended up picking GitHub Actions because it is tightly coupled to our development platform - GitHub! | Also considered CircleCI, since it was already used in some projects, but there was less knowledge in the team about it |


## Build-CI

## Build CI 2.0

| Name | Date | Context | Decision | Alternatives Considered |
|------|------|---------|----------|-------------------------|
| Don't Load and Find Compilers in Container | 06/03/2025 | For the runner image, we must do `spack load <compilers> && spack compiler find` in order to find upstream compilers every time we run the container. We were looking to find ways to do this at build time, or container start time, but the above commands are shell-specific and aren't propagated when attaching | Instead, extend `spack-config/spack-enable.bash` to run these | Attempted to have a long `CMD ". spack-enable && spack load ... && ...` but it exited prematurely |
| No schema for build-ci | 13/03/2025 | Is there anything that is a must-enforce for model component spack manifests? | Ended up going with sensible defaults via higher-level configuration scopes (but can be overridden by users) rather than a schema | Considered enforcing concretizer.unify:false and view:false via schema, but decided against it |
| Inject PR ref in spack manifests | 28/03/2025 | We needed a way to inject the PR version of the model component in the manifests without having to change the ref every commit | Change the manifest to a jinja template and fill in {{ pr }} on run. Also allows future data to be injected via a `inputs.spack-manifest-data-path` | Considered a more basic `sed` of a `__REF__` marker in the manifest, but was a bit sketchy |

## Build-CD

| Name | Date | Context | Decision | Alternatives Considered |
|------|------|---------|----------|-------------------------|

## Spack versioning

See [related issue where these guidelines were discussed](https://github.com/ACCESS-NRI/spack-packages/issues/285) for more background.

### Design choices

- If the version defined in the spack package recipe is the same as the tag used in the `git` repository it makes it obvious they are the pointing to the same code commit, and we can add CI checks to enforce this, and detect any change in commit hash.
- Avoiding `git` tag `REF`s in `@git.REF` avoids confusion and formulations like `@git.8.7.0=8.6.0` when tags and versions look almost the same.
- Default infinity version makes it not *necessary* to specify a RHS version. It will always default to `stable`, the most recent version of the package for the specified `spack-packages` version.
- There are six possible infinity versions: 
	 - `develop > main > master > head > trunk > stable`. 
  `develop`, `main`, `master` and `head` already have `git` connotations, and `trunk` has meaning in `svn`-land, so `stable` is the choice for non-numeric infinity version .
- Using full git commit hashes ensures there are never collision hashes. Full hashes are the [only trusted `git` method recommended by spack](https://spack.readthedocs.io/en/latest/packaging_guide_creation.html#git). For consistency and to avoid confusion full hashes should be used in all contexts: spack package recipes and MDR manifest files.

### Implementation

Insisting on using spack versions in release deployments places a burden on developers, who must do the following when moving from a develop (draft) workflow to a release workflow:

1. Tag all source code versions and create releases (usually automatically by GitHub)
2. Create PRs to add new versions to spack packages
3. Review/merge cycle for PRs
4. Tag `ACCESS-NRI/spack-packages` repository
5. Update deployment `spack.yaml` and `versions.json`

### CI/CD checks

We can use CI to help developers with the compliance headache, and to ensure consistency.

`ACCESS-NRI/spack-packages`:

- PR: check for new tags in packages (only since most recent version tag to not pull in spurious history). Suggest edit in comment. Option: could pattern match tags or use release tags and create direct commit.
- PR: Insist spack package recipe `version()` contains valid tags and commits
- PR: insist existing spack package recipe versions and associated `git` commit hash never change.
- PR: Insist preferred `stable` infinity version exists with `branch` defined

`ACCESS-NRI/build-cd`:

- Draf PR: Insist `@git.REF` package versions use full 40 character commit hashes (**not** tags or short hashes).
- Non-Draft PR: Insist package versions only use `spack versions`, **not**  `@git.REF`.
- PR: Check spack-packages version (in `versions.json`). If not most recent tag: warn (draft) or  error (non-draft).

Note that these checks may not be available for some time due to resourcing constraints.