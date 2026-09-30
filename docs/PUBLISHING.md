# Publish the first preview

Prepared 2026-10-01. Target: **IT-Shelter-Labs/research-first-builder**.
Selected commit author: [melroncod](https://github.com/melroncod).
The user selected this public profile for authorship; organization ownership is separate from attribution.
Repository-specific Git identity uses the ID-based GitHub noreply address, not a private mailbox.

## Readiness

The implementation, local tests, real examples, documentation and demo are ready for a **0.1.0-rc1 preview**.
The [desktop full task](acceptance/DESKTOP_BOOKMARKS.md) passed via explicit skill-file invocation.
Complete native selector discovery in the actual target project and inspect hosted CI before promoting a stable release.
Native Claude acceptance and a comparative benchmark remain open; neither receives a badge or unsupported claim.
[Detailed gates](RELEASE_STATUS.md).

## Desktop route

1. Sign into GitHub Desktop with the account that can create repositories in IT-Shelter-Labs.
2. **File → Add local repository**: choose the local `research-first-builder` product folder, not its parent workspace.
3. Review the initial local commit and files; the archives and caches are excluded from source control.
4. **Publish repository**: name `research-first-builder`; Organization `IT-Shelter-Labs`.
5. Description: `Make your coding agent justify architecture with real sources before it builds.`
6. For a public preview, clear **Keep this code private**. A private staging repository is also possible if you prefer to inspect hosted checks first.
7. Publish, then inspect **Actions**. Fix any failing Windows/Linux/lint job before presenting the preview as green.

Official instructions: [add a local repository](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-a-repository-from-your-local-computer-to-github-desktop),
[publish an existing project](https://docs.github.com/en/desktop/adding-and-cloning-repositories/adding-an-existing-project-to-github-using-github-desktop).
If the organization is absent, use the correct account or obtain repository-creation permission from its owner.

## Browser + existing Git route

Create an **empty** repository under IT-Shelter-Labs on GitHub. Name it `research-first-builder` and choose visibility.
Do not initialize a second README, license or .gitignore: the local repository already contains them.
Then authenticate Git normally and, from the local product repository, add its remote and push main:

```text
git remote add origin https://github.com/IT-Shelter-Labs/research-first-builder.git
git push -u origin main
```

These commands assume an initial local commit and no existing origin. Inspect an existing remote rather than deleting
or replacing it automatically. No force push is needed. Do not upload the entire Content OS workspace or a ZIP as the source repository.
[Official existing-code guide](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github?platform=windows).

## Finish the public preview

- Add topics: `ai`, `coding-agents`, `agent-skills`, `claude-code`, `codex`, `developer-tools`, `software-architecture`, `research`, `open-source`.
- Enable an actual private vulnerability-reporting route in repository settings and update SECURITY.md accordingly.
- Once the URL is live, update the README's local-candidate publication statement and test remote installation in a fresh project before advertising it:

```text
npx skills@1.7.0 add IT-Shelter-Labs/research-first-builder --skill research-first-build --agent codex --copy
```

- Draft a release with tag **v0.1.0-rc1**, target **main**, title **Research First Builder 0.1.0-rc1**.
- Use [prepared release notes](RELEASE_NOTES_0.1.0_RC1.md), mark **This is a pre-release**, and attach the two clean ZIPs plus SHA256SUMS from dist.
- If immutable releases are enabled, attach all assets to the draft before publishing.
[Official release instructions](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## Materials needed

The organization handle, author profile and successful desktop task artifacts have already been supplied and reviewed.
A repository URL
and normal authorized GitHub access are needed for publishing; a profile URL alone does not grant write access.

Additional photographs, screenshots or artwork are not prerequisites. The repository contains an original demo GIF.
An existing IT Shelter avatar/logo and preferred brand link are optional launch polish. A screenshot helps only when
the actual UI/error is unclear. Passwords, tokens and recovery codes are not materials to send in chat.
