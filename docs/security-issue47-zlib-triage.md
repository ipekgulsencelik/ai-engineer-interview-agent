# Issue #47 — zlib runtime security blocker (2026-11-22)

**Status: RELEASE BLOCKED.** This is an evidence record for reviewers, not a vulnerability waiver, an exception file, or release authorization.

## Reproducible observations

- Draft PR: #53 — experimental Python 3.11 + Debian 12 Distroless runtime with APT-signed `libssl3` 3.0.22 and `zlib1g`.
- Exact image: `ai-interview-bookworm-patch:7a8dd26e6937e7997c8ccaa300efeb29888f1be5`.
- GitHub Actions run: https://github.com/ipekgulsencelik/ai-engineer-interview-agent/actions/runs/45051989602
- Docker build: PASS. Python 3.11 / PyTorch / sentence-transformers imports, signed OpenSSL checksum and actual dynamic-library version, and nonroot runtime test: PASS.
- The live HTTP health step executed before the Trivy step; review its logs independently to confirm final behavior.
- **Actual built-image strict Trivy: FAIL, exit 1** (zero exclusions): `zlib1g` version `1:1.2.13.dfsg-1`; two reported advisories: `CVE-2023-45853` CRITICAL / will_not_fix and `CVE-2026-85091` HIGH / affected. An independent minimal-image preflight run #45052452509 reported the same two findings; this is not solely a Python dependency-layer effect.

## Vendor evidence and separate triage

| Advisory | Official Debian source information as of 2026-11-22 | Decision |
|---|---|---|
| CVE-2023-45853 (MiniZip) | Debian's Bookworm tracker note says `contrib/minizip` was not built from this `zlib` source version and no affected binary was shipped from it. The tracker nonetheless labels the source package vulnerable. | **Candidate for evidence-based not-affected disposition**, subject to validating exact runtime contents, bill of materials, and independent security reviewer. Do not silently suppress the scanner warning. |
| CVE-2026-85091 (zlib gz_write) | Debian Security Tracker lists Bookworm `1:1.2.13.dfsg-1` as **vulnerable** without a fixed Bookworm package. Debian's DSA-6613-1 lists the fixed Trixie package `1:1.3.dfsg+really1.3.1-1+deb13u1`. Some historical advisories describe a narrower affected range, but the Debian tracker and reproduced vulnerability discussions explicitly include 1.2.13. | **Unresolved security blocker**. Do not assert it is a false positive or bypass Trivy. |

Evidence:
- https://security-tracker.debian.org/tracker/CVE-2023-45853
- https://security-tracker.debian.org/tracker/CVE-2026-85091
- https://security-tracker.debian.org/tracker/DSA-6613-1
- https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1146895
- https://github.com/ipekgulsencelik/ai-engineer-interview-agent/actions/runs/45052452509

## Approved engineering next steps — none completed by this note

1. **Prefer vendor-supported remediation:** monitor Debian Bookworm security for a signed, corrected `zlib1g` package or select a maintained distro/runtime **with both OpenSSL and zlib patched** and verified Python 3.11 / PyTorch compatibility. Do not copy a Debian 13 binary into Debian 12 without a complete ABI, SBOM and provenance review.
2. If upstream/backport work is proposed, use auditable signed sources, verified source patch, reproducible build, real package-version and checksum metadata, regression tests and independent sign-off. It must not merely change the package metadata.
3. For MiniZip's not-affected claim only, independently verify absence of the vulnerable MiniZip implementation and its reachability in the **actual final image**; attach a reviewed VEX/exception only under an explicitly approved risk policy. This cannot resolve the independent zlib HIGH finding.
4. Rerun **strict full final-image Trivy without exceptions**, locked production `pip-audit`, native imports, live HTTP health and SQLite retrieval, nonroot/read-only and persisted state, SBOM/provenance/signature/digest and cross-platform release gates.
5. Keep issue #47 open and draft PRs #48–#53 unmerged until release-owner and security reviewer approval. No image publish or deployment.

**Do not** weaken `severity`, set `ignore-unfixed`, use `.trivyignore` to hide a known real vulnerability, falsify `/var/lib/dpkg/status.d`, or treat a base-only scan as final-image approval.
