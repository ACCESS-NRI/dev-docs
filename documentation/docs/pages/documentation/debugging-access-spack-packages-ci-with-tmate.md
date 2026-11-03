{Draft written by Google Gemini 3 Flash, for discussion and review}
{Reviewed by Tommy}

This guide provides specific instructions for developers of the `access-spack-packages` repository (as well as any Model Component Repository with the tag `build-ci-enabled`) to troubleshoot build failures using `tmate`.

## 1. How to Enable Debugging
`tmate` is disabled by default for efficiency, as one will need to manually enter and exit the ssh session for all jobs to complete. To enable it for a specific PR or test run, you must temporarily modify the repository's configuration.

### Procedure:
1.  Open the file: for example, [.github/workflows/ci.yml](https://github.com/ACCESS-NRI/access-spack-packages/blob/main/.github/workflows/ci.yml)
2.  Locate the `ci` job at the bottom of the file.
3.  Change `allow-ssh-into-spack-install: false` to `true`.

```yaml
    uses: access-nri/build-ci/.github/workflows/ci.yml@v3
    with:
      ...
      allow-ssh-into-spack-install: true  # <--- Set this to true
```

4.  Commit and push this change to your branch.

---

## 2. Accessing the Session
1.  Once the push is detected, the GitHub Action will start.
2.  It will process the `setup-ci` job to identify your changed packages.
3.  In the `ci` job, after the Spack installation attempt finishes, it will create a `tmate` session.
4.  Open the GitHub Actions log for the specific package build and find the **"Tmate - Create session"** step to get your SSH command. It will only be available to the author of the commit. 
5.  After connecting, **press `q`** to dismiss the `tmate` splash screen and reach the interactive shell.

---

## 3. Investigating Package Failures
Since most repositories test multiple manifests in a matrix, you will be placed in a container dedicated to **one specific manifest**.

### Identify what matched:
Inside the session, check which manifest and package were selected:
```bash
cat /tmp/artifact-output/job_outputs.json | jq .template_value
```

### Important Locations in `/tmp`:
- The environment that installed the manifest is named `default`. Manifest information is under `/opt/environments/default`.
- **`/tmp/root/spack-stage/`**: This is where Spack actually builds the packages.
  - If a build fails, you can `cd` into the relevant subfolder here to see the patched source code and build logs.

### Essential Commands:
- **Activate Spack**:
  ```bash
  . /opt/spack/share/spack/setup-env.sh
  spack env activate default
  ```
- **Find the failed build directory**:
  ```bash
  spack location -s <your-package-name>
  ```
- **Check the Spack recipe being tested**:
  For `access-spack-packages`, the recipes being tested are in the root of the workspace:
  `/__w/access-spack-packages/access-spack-packages/spack_repo/access/nri/packages/`

---

## 4. Troubleshooting Checklist
- [ ] **Concretization error?** Run `spack spec` to see why dependencies aren't resolving.
- [ ] **Compilation error?** Check the log in the stage directory using `cat $(spack location -s <pkg>)/.spack-build-out.txt`.
- [ ] **Checksum error?** Verify the URL and SHA in your `package.py`.
- [ ] **Patch error?** Check if your patches apply cleanly to the source in the stage directory.

---

## 6. Specifics for `um` and `um-createbc`

The UM models are more complex due to their use of the **`UmBasePackage`** and the **FCM** build system.

### A. Resource Fetching (The Patch Phase)
These models dynamically clone multiple repositories (UM, JULES, CASIM, etc.) during the Spack `patch` phase into the staging directory.
- **Where to look**: `/tmp/root/spack-stage/spack-stage-um-*/spack-src/resources/`
- **Common Issue**: If a `ref` (like `um_ref` or `shumlib_ref`) is invalid or inaccessible, the `patch` phase will fail. Use `tmate` to manually test `git clone` with the credentials provided.

### B. Environment Variables & Rose Config
The build logic is heavily driven by environment variables mapped from the model's `rose-app.conf`.
- **Check the logs**: The Spack install log will contain `tty.info` messages printing every environment variable set by `UmBasePackage`.
- **Verification**: If you suspect a variable is wrong (e.g., `CPATH` or `fcm_sys_flags`), check these logs first.

### C. Verbose FCM Builds
For debugging only, change the build phase to run `fcm make -vv`.
- **Source of Truth**: The primary log for the entire build process is located at:
  `/tmp/root/spack-stage/spack-stage-*/spack-build/fcm-make.log`
- **Internal Task Logs**: Detailed logs for specific build tasks (if they reach the compilation stage) can be found in:
  `/tmp/root/spack-stage/spack-stage-*/spack-build/build-*/log/`
- **Debugging**: You can manually rerun the build or inspect exactly what was parsed in:
  `/tmp/root/spack-stage/spack-stage-*/spack-build/fcm-make-as-parsed.cfg`

### D. Manual Test Trigger
Since `um` is often excluded from automatic PR tests, you may need to trigger it via **Workflow Dispatch**:
1. Go to **Actions** -> **CI** -> **Run workflow**.
2. Select your branch.
3. In `Packages to test`, enter `um` or `um_createbc`.
4. Ensure `allow-ssh-into-spack-install` is set to `true` if you need to debug interactively.

---

## 7. Cleaning Up
Once you have identified the issue:
1.  **Exit the session**: Type `exit`.
2.  **Revert the change**: Don't forget to change `allow-ssh-into-spack-install` back to `false` in your `ci.yml` before merging your PR.
