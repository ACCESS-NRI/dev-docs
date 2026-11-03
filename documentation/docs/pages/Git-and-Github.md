## Git

## Repository creation and naming
In the first instance, all repositories should be created using the ACCESS-NRI [General Repository Template](https://github.com/ACCESS-NRI/template) which contains the correct software COPYRIGHT and LICENSE information.
Repositories should always have a `README.md` providing a description of the repo purpose, content and any useful links / references. The more detailed documentation that can be provided here the better.
### Naming
Repository names should have unique, all lower-case names with words separated by hyphen/dashes. Ideally repo names should be as semantic as possible. 
Examples: 
* `repo`
* `my-repo`
* `my-more-complex-repo`

## Topic tags

To help with discoverability, all the repositories in the ACCESS-NRI GitHub organisation must use appropriate topic tags. For a list of all topics tags and a detailed explanation on how to use them, see the corresponding [section](https://github.com/ACCESS-NRI/dev-docs/wiki/GitHub-Organizations#topic-tags).

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
All feature branches should be named using the naming convention described above prefixed with a unique issue number.

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


## Manage multiple Git commit identities on the same machine
If you use a single machine for multiple projects that require different Git commit identities (i.e., `user.name` and `user.email` values), you can configure Git to automatically select the correct author information based on the project's directory.

This is particularly useful for separating, for example, work-related and personal projects.

### Overview
The core idea is to group projects that share the same Git identity under a common parent directory. Git can then apply a specific configuration automatically when working inside that directory.

For example, in a work machine you could use the folder `/path/to/personal` to store all the personal Git repositories (while the work-related repositories might be spread across multiple folders).

### Git configuration Setup
This folder-based approach requires:
- A _global_ Git configuration (`~/.gitconfig`)
- One or more _project-specific_ Git configuration files

#### Project-specific Git Configuration
Create a dedicated Git configuration file for each identity. This file should define the commit identity (and any other Git settings) specific to that group of projects.

For example, you could create a personal configuration file at `~/.personal-gitconfig` with the following content:
```
[user]
    name = <your-personal-git-name>
    email = <your-personal-git-email>
```

#### Global Git Configuration
Your global Git configuration file (usually `~/.gitconfig`) should:
- Define your default commit identity
- Use `includeIf` to conditionally load the project-specific Git configuration when working inside a specific directory

For example, for a default Git identity associated with your work, personal Git configuration located at `~/.personal-gitconfig` and all personal Git repositories stored at `/path/to/personal`, the global Git configuration could be:
```
[user]
    name = <your-work-git-name>
    email = <your-work-git-email>

# Other custom global settings ...

[includeIf "gitdir:/path/to/personal"]
	path = ~/.personal-gitconfig
```

This setup ensures that commits are automatically associated with the correct author name and email based on the repository location.

> [!TIP]
> To add additional project-specific Git configurations, create a new configuration file for each identity and add a corresponding `[includeIf ...]` section to your global Git configuration with the appropriate settings.

For more information, refer to [Git configuration documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration).




## Github
All <i>direct</i> Github actions (e.g. repo creation, naming etc) follow the [Git style guide](https://github.com/ACCESS-NRI/dev-docs/wiki/Git-and-Github#git) above.

* Use the anu.edu.au email address for your commits
* Enable [two-factor authentication](#two-factor-authentication)
* Enable [commit signing](#signed-commits)

## Two-factor Authentication

Two-factor authentication is an important security measure to protect your account and all ACCESS-NRI Staff must enable it. Outside contributors with write access to ACCESS-NRI Organisation repos are also required to enable 2FA.

There is [extensive GitHub documentation covering how to enable 2FA](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication).

Some notes:

- It is a good idea to configure more than one 2FA method in case you lose access
- Both BitWarden and Microsoft Authenticator are TOTP apps that are already in use by many in the organisation
- The GitHub Mobile app is also a convenient 2FA method

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

## Signed commits
Signed commits are very important.<br>
_Git_ by itself does not track and validate user action on commits. This means you can easily impersonate someone else and push commits under their name (for more information, refer to [Why You Should Sign All Your Git Commits](https://betterprogramming.pub/why-and-how-you-should-sign-all-your-git-commits-94435516edae)).

### Sign your commits using SSH

1. **Generate a new SSH key**<br>
   If you don't have one already, [generate a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key) and [add your ssh key to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#adding-your-ssh-key-to-the-ssh-agent).
2. **Add your public SSH key to GitHub**<br>
   If you don't have an SSH already added to GitHub, [add the SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).
3. **Set up signed commits with SSH**<br>
   To set up signed commits using SSH run the following commands (by substituting the path to your public SSH key):
   ```
   git config --global gpg.format ssh
   git config --global user.signingkey ~/.ssh/<path-to-your-ssh-key.pub>
   ```
4. **Set up signed commits globally**<br>
   To set _Git_ to sign all commits globally by default, run:
   ```
   git config --global commit.gpgsign true
   ```
5. **Create an _allowed signers_ file**<br> 
   The _allowed signers_ file is a list of trusted public SSH keys that tell _Git_ who is allowed to sign commits.<br>
   To create the file run the following commands (by substituting your email and public SSH key content):
   ```
   mkdir -p ~/.config/git
   cat > ~/.config/git/allowed_signers <<< "<your@email.address> <your-public-ssh-key-content>"
   ```
   Then, to inform _Git_ about this file, use the following command:
   ```
   git config --global gpg.ssh.allowedSignersFile ~/.config/git/allowed_signers
   ```
6. **Add your public SSH key as a signing key to GitHub**<br>
   In GitHub's Settings, go to the [SSH and GPG keys panel](https://github.com/settings/keys).<br>
   Click on "New SSH key" and change the "Key type" to _Signing Key_.<br>
   <img src="https://www.git-tower.com/blog/media/pages/posts/setting-up-ssh-for-commit-signing/bbbcbc261a-1715780496/github-signing-key.png" alt="github-singing-key-image" width="500px"><br>
   Copy your public SSH key content in the box and click on "Add SSH key".

You are set! You should now see a _Verified_ green tag next to your commit messages on GitHub.<br>
<img src="https://www.git-tower.com/blog/media/pages/posts/setting-up-ssh-for-commit-signing/7d9f4c5fde-1715780496/github-verified.png" alt="verified-tag" width="500px">

### Sign commits on _Gadi_

On _Gadi_, depending on which `ssh-keygen` distribution you are using, when trying to issue a signed commit you might get an error similar to the following:

> error: ssh-keygen -Y sign is needed for ssh signing (available in openssh version 8.2p1+)

To solve this issue, the recommended option is to set the [`gpg.ssh.program`](https://git-scm.com/docs/git-config#Documentation/git-config.txt-gpgltformatgtprogram) _Git_ configuration option to an `ssh-keygen` executable with version `>= 8.2p1`. A suitable `ssh-keygen` executable is available in `vk83`.<br>
To set the `gpg.ssh.program` option to the `ssh-keygen` executable in `vk83`, run:
``` 
git config --global gpg.ssh.program /g/data/vk83/apps/spack/0.22/release/linux-rocky8-x86_64_v4/gcc-14.1.0/openssh-9.8p1-srryuoi3qbdh2jo6kptsqodjz3fj7e64/bin/ssh-keygen
```
> [!IMPORTANT]
> To use the `ssh-keygen` executable in `vk83`, you need to be a member of the `vk83` project.<br>
> For more information on joining specific NCI projects, refer to [How to connect to a project](https://opus.nci.org.au/display/Help/How+to+connect+to+a+project).

### Sign old commits
After [enabling signed commits](#sign-your-commits-using-ssh), you can sign old commits by running:
```
git rebase --exec 'git commit --amend --no-edit -n -S' -i <GITREF>
```
with `<GITREF>` usually being a _Git_ ref to the last signed commit.<br>
For example, to sign all commits within a feature branch (branched off `main`), run:
```
git rebase --exec 'git commit --amend --no-edit -n -S' -i main
```

Instead, to sign the last 3 commits within a branch, run:
```
git rebase --exec 'git commit --amend --no-edit -n -S' -i HEAD~3
```

> [!IMPORTANT]
> Signing old commits changes the _Git_ history (as all `git rebase` commands do). Therefore, the new signed commits will have to be force-pushed to `origin`. Instead of simply using `git push --force`, we recommend using the safer [`--force-with-lease`](https://www.atlassian.com/blog/it-teams/force-with-lease):
> ```
> git push --force-with-lease
> ```

## Git setup on Gadi using local SSH keys
It is possible to to run `git` commands (including signing commits) from _Gadi_, without having to set new SSH keys for authentication and signing, but using your local SSH keys instead. 
To do so, follow the steps below:

### 1. Add `ForwardAgent yes` to your local `~/.ssh/config` for the _Gadi_ Host
Your _Gadi_ Host should look something like:
```
Host gadi
   Hostname gadi.nci.org.au
   User <your_username>
   IdentityFile <path_to_gadi_ssh_private_key>
   ForwardAgent yes
   ...
```
This step should only be done once.
Alternatively, for every connection you can run the SSH command using `ssh -A ...`
  
### 2. Add the ssh-keys to your local SSH agent
1. Start an SSH agent by running:
   ```
   eval "$(ssh-agent -s)"
   ```
2. **Add your _Git_ authentication and signing SSH keys to the agent**
   To add an SSH key to the agent run:
   ```
   ssh-add <path_to_the_ssh_private_key>
   ```
   You will prompted to insert the SSH key passphrase.
   Repeat the step for each SSH key you wish to add.
  
This steps should be done for each new local session (for example every time you open a new instance of your terminal app or you reboot your computer).

### 3. Set `defaultKeyCommand` in your _Gadi_ `~/.gitconfig`
On _Gadi_, set the command run by _Git_ when looking for the signing key by running
```
git config --global gpg.ssh.defaultKeyCommand "ssh-add -L"
```

> [!IMPORTANT]
> `ssh-add -L` lists all keys added to the ssh-agent (including the forwarded from local ones). This will always work if the agent only has one ssh-key added, but might select a wrong SSH key if multiple ones are present, resulting in your commits not being correctly signed.
> To avoid this, the suggestion is to specify a custom command that outputs the SSH key you use for signing.<br>
> For example, if by running `ssh-add -L` your signing key starts with `ssh-rsa AAABCDEF...` your command could be:
> ```
> git config --global gpg.ssh.defaultKeyCommand "sh -c 'ssh-add -L | grep \"^ssh-rsa AAABCDEF\"'"
> ``` 