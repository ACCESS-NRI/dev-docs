## CI/CD

Projects should try to include continuous integration and deployment workflows for testing and release. Where possible, these should use [GitHub Actions](https://github.com/features/actions). We have our own repository for custom actions at [ACCESS-NRI/actions](https://github.com/ACCESS-NRI/actions/). Some recommended Actions and examples of their usage are given at the bottom of this document.

## Actions Versioning

When we use actions and reusable workflows in GitHub Actions, we require certain levels of strictness for the version. 

We allow the following, from least to most strict:
* For ACCESS-NRI-internal actions (`access-nri/*` actions of any type) we allow any type of version reference. This includes branch references (including `@main`), tag references (`@2.0.1`) or commit references (`@as2u9e8u2e8u29eu9u8e29e`). This is because we these are developed in-house and are safely maintained. One use case for a less-restrictive version is that the `@main` branch reference can be employed so there are not as many pull requests to update the hashes for cross-repository actions/workflows. 
* For GitHub-published actions (`actions/*`) we allow major branch references (`@v5`), tag references (`@v5.0.1`) or commit references (`@3e892h2b983dhn239dj`). This is because these are core GitHub-created workflows and we have relative certainty as to their stability. 
* For any other action (`*/*`) we only allow commit references (`@r928jn2hdb293e2e298hd`) as we don't have any guarantee as to their stability, or the creators security policies. Although it isn't very readable, you can still put the tag that is associated with that commit in a comment (eg. `- uses some/action@o2udndj29d23jd29d298jdu32  # v0.2.1`).  

## Common Pitfalls (and how to step around them)

### Verified Commits from a Workflow

**TL:DR:** Use our `access-bot` GitHub account to author commits, since it has an associated commit signing key as an org secret. 

All manner of git-related operations can be done in a workflow, similarly to how it is done locally. You can push commits, tags, create branches, etc. By default, these are all authored by GitHubs own `github-actions[bot]` account, and are unverified commits.

For repositories that require signed commits, this will not do. We can't add a signing key to GitHubs own `github-actions[bot]` account. 

To get around this, we have an ACCESS-NRI-owned GitHub Account (`access-bot`) that has a signing key associated with its account. We just need to import the secret key and other details into our workflows using [a GPG Key Importing action](https://github.com/marketplace/actions/import-gpg). 

> [!IMPORTANT]
> Remember to _always_ pin the hashes of custom external third-party actions, _not_ the tag or branch, especially for actions that handle secrets. It is the only way to be certain that an action hasn't been maliciously changed. 

The secrets required are organisation-level `secrets` and `vars`, and are used in an example below:

```yaml
jobs:
  commit:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      - uses: crazy-max/ghaction-import-gpg@01dd5d3ca463c7f10f7f4f7b4f177225ac661ee4  # v6.1.0
        with:
          gpg_private_key: ${{ secrets.GH_ACTIONS_BOT_GPG_PRIVATE_KEY }}
          passphrase: ${{ secrets.GH_ACTIONS_BOT_GPG_PASSPHRASE }}
          git_config_global: true
          git_committer_name: ${{ vars.GH_ACTIONS_BOT_GIT_USER_NAME }}
          git_committer_email: ${{ vars.GH_ACTIONS_BOT_GIT_USER_EMAIL }}
          git_user_signingkey: true
          git_commit_gpgsign: true
          git_tag_gpgsign: true

      - run: |
          echo "Just updating the README..." >> README.md
          git commit -am "Added stuff"
          git push
```

![image](https://github.com/user-attachments/assets/5bbc96d3-8511-4169-b59e-4831f467bc84)

As you can see, our commit is authored by `access-bot`, and has a verified signature, meaning we can have workflow-authored commits that are signed appropriately for repos that require signed commits. 

### Matrices at the Workflow Level (or, How to Create Dependent Jobs for Each Element of a Matrix)

**TL;DR:** Use a matrix job that calls a reusable workflow that has an input of `${{ matrix.element }}` - the reusable workflow can have multiple jobs!

GitHub Actions allows jobs to be done in parallel based on a matrix, like so:

```yml
jobs:
  test:
    name: Test Script With Python Version ${{ matrix.py-version }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        py-version: ['3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.py-version }}
      - run: python -m pytest my_script.py
```

Visually, it'd look something like this:

```txt
 ┌───[Test (3.9)]───┐
─┼───[Test (3.10)]──┼─
 └───[Test (3.11)]──┘
```

This works well for simple jobs, but sometimes the task at hand may be quite complex, and you don't necessarily want to have 1000 steps in the one matrix job - maybe you want to break it up into multiple, dependent jobs, for example one for testing and one for running - something that looks like this (given our previous example):

```txt
 ┌───[Test (3.9)]───[Run (3.9)]───┐
─┼───[Test (3.10)]──[Run (3.10)]──┼─
 └───[Test (3.11)]──[Run (3.11)]──┘
```

#### Pitfall 1: Just make `test` require `run`?

Initially, I'd just made a `run` job require `test`, like so:

```yml
# NOTE: THIS WILL NOT WORK!
jobs:
  test:
    name: Test Script With Python Version ${{ matrix.py-version }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        py-version: ['3.9', '3.10', '3.11']
    steps:
      # Test each ${{ matrix.py-version }} thing
  run:
    name: Run Script With Python Version ${{ matrix.py-version }}
    runs-on: ubuntu-latest
    needs:
      - test  # run only if the associated `py-version` succeeds
    steps:
      # Run each ${{ matrix.py-version }} thing
```

But this actually leads to random behavior, because all the matrix jobs in `test` complete, *only then* `run` starts, with no knowledge of any of the matrix element jobs:

```txt
 ┌───[Test (3.9)]───┐
─┼───[Test (3.10)]──┼──[Run]──
 └───[Test (3.11)]──┘
```

#### Pitfall 2: Each Dependent Job Gets a Matrix, too?

Okay, so why not just make `run` know about the matrix, and `needs: test`?

```yml
# NOTE: THIS WILL NOT WORK, EITHER!
jobs:
  test:
    name: Test Script With Python Version ${{ matrix.py-version }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        py-version: ['3.9', '3.10', '3.11']
    steps:
      # Test each ${{ matrix.py-version }} thing
  run:
    name: Run Script With Python Version ${{ matrix.py-version }}
    runs-on: ubuntu-latest
    needs:
      - test  # run only if the associated `py-version` succeeds
    strategy:  # I'll just add this, then...
      matrix:
        py-version: ['3.9', '3.10', '3.11' ]
    steps:
      # Run each ${{ matrix.py-version }} thing
```

But, each `py-version` job that spawn with `test` and `run` are not linked. For example, the failure of `[Test (3.9)]` would not stop `[Run (3.9)]` specifically from running. They fan in and out, like this:

```txt
 ┌───[Test (3.9)]───┐ ┌───[Run (3.9)]───┐
─┼───[Test (3.10)]──┼─┼───[Run (3.10)]──┼─
 └───[Test (3.11)]──┘ └───[Run (3.11)]──┘
```

#### Solution: Contain `Test`, `Run` in Reusable Workflow

The only way to have dependent, matrix-element-aware jobs is to contain them in a reusable workflow. Since the calling of a reusable workflow is technically a single 'job' (which, within the reusable workflow, can contain more jobs), we can do the following, instead:

```yml
### File: .github/workflows/test-and-run-all-things.yml
on:
  pull-request:
jobs:
  test-and-run-all-versions:
    name: Test and Run with ${{ matrix.py-version }}
    strategy:
      matrix:
        py-version: ['3.9', '3.10', '3.11']
    uses: .github.workflows/test-and-run-one-thing.yml  # a local reusable workflow!
    with:
      py-version: ${{ matrix.py-version }}

### File: .github.workflows/test-and-run-one-thing.yml
on:
  workflow_call:
    inputs:
      py-version:
        type: string
        required: true
        description: A version of python to test and run
jobs:
  test:
    name: Test Script With Python Version ${{ matrix.py-version }}
    runs-on: ubuntu-latest
    steps:
      # Test each ${{ inputs.py-version }} thing (not matrix.py-version!)
  run:
    name: Run Script With Python Version ${{ matrix.py-version }}
    runs-on: ubuntu-latest
    needs:
      - test  # run only if the associated `py-version` succeeds
    steps:
      # Run each ${{ inputs.py-version }} thing (not matrix.py-version!)
```

Which gives us our satisfying:

```txt
 ┌───[Test (3.9)]───[Run (3.9)]───┐
─┼───[Test (3.10)]──[Run (3.10)]──┼─
 └───[Test (3.11)]──[Run (3.11)]──┘
```

#### Further Reading

* [GitHub Article on Reusable Workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
* [GitHub Article on Matrices](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)

### Dynamic `default`s in `inputs`

**TL;DR**: You can't set a `default` of anything in `${{ ... }}`, only static strings. Instead create a job/step that sets that kind of default as an `env`. 

Currently, [only `string`s are allowed in `default`s](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#inputsinput_iddefault). Sometimes, you need the `default` of an `input` to be based on another `input`, or an `env`, or any other thing available in `${{ ... }}`. However, these are not interpreted by GitHub Actions, and no error will be thrown. 

#### The Way That (Annoyingly) Doesn't Work

For example:

```yaml
inputs:
  name:
    type: string
    required: true
  nickname:
    type: string
    required: false
    default: ${{ inputs.name }}
jobs:
  print-name:
    runs-on: ubuntu-latest
    steps:
      - run: echo 'My name is ${{ inputs.name }} and you can call me ${{ inputs.nickname }}!'
```

The result of this with `inputs.name: Jim` will give `"My name is Jim and you can call me !"`, with the empty string being substituted for `${{ inputs.nickname }}`. 

#### The Way That Does Work

So, one has to set the default in a kind of roundabout way. One way to do this is to have a job or step that sets the default as an `env` instead, like so:

```yaml
inputs:
  name:
    type: string
    required: true
  nickname:
    type: string
    required: false
    # default: ${{ inputs.name }}
jobs:
  set-defaults:
    runs-on: ubuntu-latest
    outputs:
      nickname: ${{ steps.defaults.outputs.nickname }}
    steps:
      - id: defaults
        run: |
          if [ -z "${{ inputs.nickname }}" ]; then
            echo "nickname=${{ inputs.name }}" >> $GITHUB_OUTPUT
          else
            echo "nickname=${{ inputs.nickname }}" >> $GITHUB_OUTPUT
          fi
  print-name:
    runs-on: ubuntu-latest
    needs:
      - set-defaults
    steps:
      - run: echo 'My name is ${{ inputs.name }} and you can call me ${{ needs.set-defaults.outputs.nickname }}!'
```

Which will give the appropriate `"My name is Jim and you can call me Jim!"` with no `inputs.nickname`, but will give the correct one when `inputs.nickname` is set - for example, `"My name is Jim and you can call me Jimbo!"` with `inputs.nickname: Jimbo`.

This can be simplified to the step level, if you don't want to make it it's own job. 

## Example Usage of Common Actions

### Checking out your repo

**Action**: [```actions/checkout```](https://github.com/marketplace/actions/checkout)

**Example usage**: https://github.com/ACCESS-NRI/intake-dataframe-catalog/blob/main/.github/workflows/ci.yml#L9

### Setting up Python

**Action** [```actions/setup-python```](https://github.com/marketplace/actions/setup-python)

**Example usage**: https://github.com/ACCESS-NRI/intake-dataframe-catalog/blob/main/.github/workflows/cd.yml#L16

### Customizable code linting/formatting

**Action**: [```pre-commit/action```](https://github.com/marketplace/actions/pre-commita)

**Example usage**: https://github.com/ACCESS-NRI/intake-dataframe-catalog/blob/main/.github/workflows/ci.yml#L11

### Setting up a conda environment

**Action**: [```conda-incubator/setup-miniconda```](https://github.com/marketplace/actions/setup-miniconda)

**Example usage**: https://github.com/ACCESS-NRI/intake-dataframe-catalog/blob/main/.github/workflows/ci.yml#L25

### Uploading code coverage reports to CodeCov

**Action**: [```codecov/codecov-action```](https://github.com/marketplace/actions/codecov)

**Example usage**: https://github.com/ACCESS-NRI/intake-dataframe-catalog/blob/main/.github/workflows/ci.yml#53

### Publishing a Python package to PyPI
>[!TIP]
> For a pure python package, consider using the new [publish-python-package workflow](https://github.com/ACCESS-NRI/actions/blob/main/.github/workflows/README.md#publish-python-package-workflow) instead.

**Action**: [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish)

**Example usage**: https://github.com/ACCESS-NRI/intake-dataframe-catalog/blob/main/.github/workflows/cd.yml#L30

**Note**: The example above uses PyPI "Trusted Publishing". See [here](https://docs.pypi.org/trusted-publishers/) for documentation on how to add a trusted publisher to a PyPI project.

### Publishing a Python package to conda
>[!TIP]
> For a pure python package, consider using the new [publish-python-package workflow](https://github.com/ACCESS-NRI/actions/blob/main/.github/workflows/README.md#publish-python-package-workflow) instead.

**Action**: [```ACCESS_NRI/action-build-and-upload-conda-packages```](https://github.com/ACCESS-NRI/action-build-and-upload-conda-packages)

**Example usage**: [How to use](https://github.com/ACCESS-NRI/action-build-and-upload-conda-packages)

#### Create an Anaconda Token
To use the action above, you need to:

1. Generate an [Anaconda token](https://github.com/ACCESS-NRI/action-build-and-upload-conda-packages?tab=readme-ov-file#anaconda-token) by logging into Anaconda.org, switching to the `accessnri` account and going to "Settings" -> "Access".  
   - Call your new token something like `mypackagename publish`
   - Set read and write access
   - Set the expiration date to some time in the distant future (e.g. 5 years)
2. Add the generated token as a GitHub Secret content within the GitHub repo under _Settings -> Secrets and variables -> Actions -> New repository secret_. Call the new Secret `ANACONDA_TOKEN`.
3. Add `accessnri` as a GitHub Variables content within the GitHub repo under _Settings -> Secrets and variables -> Actions -> Variables tab --> New repository variable_. Call the new Variable `ANACONDA_USER`.

> [!IMPORTANT]
> For the workflow above, you need to be:
> - An admin of the desired GitHub repo (to manage Secrets and Variables)
> - A member of the `accessnri` Anaconda organisation.<br>
>   To get access, ask one of the following members to add you (list up to date as of 15/04/2025):
>   - Aidan Heerdegen
>   - Ben Schroeter
>   - Claire Carouge
>   - Charles Turner
>   - Davide Marchegiani
>   - Dougie Squire
>   - Mike Tetley
>   - Kelsey Druken
>   - Martin Dix
>   - Romain Beucher

## Build-CI/Build-CD

## Defaults for Common Refs

### Build-CI

| Repository | Sourced From | Value |
| ---------- | ------------ | ----- |
| `access-nri/spack` | `build-ci`s [`ci.yml`](https://github.com/ACCESS-NRI/build-ci/blob/b9aa938a4cb15946d4c88b52fd39a184bbdf217b/.github/workflows/ci.yml#L66-L73) | `releases/v1.1` |
| `spack/spack-packages` | `build-ci`s [`ci.yml`](https://github.com/ACCESS-NRI/build-ci/blob/b9aa938a4cb15946d4c88b52fd39a184bbdf217b/.github/workflows/ci.yml#L52-L58), which references `spack-config`s [`repos.yaml`](https://github.com/ACCESS-NRI/spack-config/blob/415c4308e07730e00f92dc3505f7a1bf2eafb0a9/common-api-v2/repos.yaml#L6-L9) | `39aeb9dbcc13b6a53e40c77b672c397e1f4c93ec` |
| `access-nri/access-spack-packages` | `build-ci`s [`ci.yml`](https://github.com/ACCESS-NRI/build-ci/blob/b9aa938a4cb15946d4c88b52fd39a184bbdf217b/.github/workflows/ci.yml#L59-L65) | `api-v2` |
| `access-nri/spack-config` | `build-ci`s [`ci.yml`](https://github.com/ACCESS-NRI/build-ci/blob/b9aa938a4cb15946d4c88b52fd39a184bbdf217b/.github/workflows/ci.yml#L45-L51) | `main` |

### Build-CD

| Repository | Sourced From | Value |
| ---------- | ------------ | ----- |
| `access-nri/spack` | Specific SHA:`build-cd`s [`config/settings.json`](https://github.com/ACCESS-NRI/build-cd/blob/384c5d6556cdcd0547f1aad50185be8b30b18eb4/config/settings.json). Major Version Branch: An MDRs [`config/versions.json`](https://github.com/ACCESS-NRI/model-deployment-template/blob/a4fc903c85a8967a7d8719d64aae3eca147f32c1/config/versions.json#L3) | Varies, example: `89b3f0baae13477ee5384cd30ebf512489a69890`, `1.1` |
| `spack/spack-packages` | `build-cd`s [`config/settings.json`](https://github.com/ACCESS-NRI/build-cd/blob/384c5d6556cdcd0547f1aad50185be8b30b18eb4/config/settings.json) | `8ed34337e15d759890b68682d704aa55dd243537` |
| `access-nri/access-spack-packages` | An MDRs [`config/versions.json`](https://github.com/ACCESS-NRI/model-deployment-template/blob/80272b51077ca8d298dfb3abe3c3d597a82578f0/config/versions.json#L4) | Varies, example: `api-v2` |
| `access-nri/spack-config` | `build-cd`s [`config/settings.json`](https://github.com/ACCESS-NRI/build-cd/blob/384c5d6556cdcd0547f1aad50185be8b30b18eb4/config/settings.json) | `2025.11.003` |