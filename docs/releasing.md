# Release procedure

Repository: https://github.com/avkaz/nap-driven-development

1. Update the single kit version in `skills/ndd-setup/VERSION`, changelog and any
   versioned documentation examples. No installer embeds a separate release version.
2. Run the automated suite and the applicable [agent scenarios](testing.md).
   Check Windows PowerShell 5.1/7 and macOS results; record actual tested agent
   versions. Do not label unexecuted platform/agent checks as passed.
3. Run `python3 scripts/build_release.py`. Inspect `dist/ndd-kit-VERSION.zip`
   and its `.sha256` file. Rebuilding the same source creates the same ZIP bytes;
   source text line endings and filesystem timestamps don't affect the archive.
4. Extract the archive to a fresh directory and smoke-test its installers with
   explicit disposable target directories. Check its README links and bundled assets.
5. Review the final diff. When authorized to publish, commit the reviewed version,
   tag it `vVERSION`, and create a GitHub Release with the ZIP, checksum, changelog
   and exact compatibility results. These are maintainer actions, not actions
   performed by setup or the packaging script.

CI builds downloadable artifacts but has read-only repository permissions and
does not publish a release. A local implementation pass without Git metadata
cannot commit/tag or verify an upstream remote state. Restore a proper checkout
before publication; never infer the current remote contents from a copied folder.

## First public candidate

0.3.0 makes setup read-only by default, uses only bundled templates and adds clean
uninstall. Existing 0.1/0.2 project documents are preserved. Unreceipted machine
installs and legacy feature plans still require adoption/review. Uninstall with
this release also removes backups retained by 0.2.
If manual platform/agent gates remain pending, publish only as a clearly marked
prerelease after explicit maintainer approval, or finish the gates first.

## Optional features

Development links are supported but not the normal installation. Repo vendoring,
plugin-marketplace distribution, automatic parallel tasks and background updates
are not part of this release. They need separate demonstrated requirements and
compatibility testing before being added.
