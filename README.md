# Hydraulic Analogy hosting

This repository hosts https://hydraulicanalogy.com/ and its circuit simulator
at https://hydraulicanalogy.com/app/. It serves the same released educational
Inertance application directly, without forwarding visitors to inertance.org.
The root address automatically opens `/app/` over HTTPS, preserving query
parameters and preset hashes. The older demo and About page remain accessible
at `/lab/` and `/about/`.

Verified 7 October 2026. The complete [hosting/Porkbun/publishing runbook](https://github.com/Lucasfrit/inertance-site/blob/main/docs/DEPLOYMENT.md)
records both domains, certificate work, current DNS and deployment evidence.
Inertance's DTU block is separate from the certificates; this independent domain
worked through normal DNS on the same network.

## Releases

GitHub Actions reads the public `Lucasfrit/inertance-site` main branch, copies
only visitor pages and assets, rewrites the primary-domain URLs for this domain,
replaces the landing page with `entry.html` to open the simulator automatically,
and deploys an artifact to GitHub Pages. No private simulator checkout or secret
is needed. Source/build folders and project documents are excluded from the
deployment. The app runtime and presets are unchanged.

Each deployment verifies that GitHub's HTTPS enforcement remains enabled.
Pages settings are maintained by the repository owner; the deployment token
does not have administrative permission to change them.

The workflow runs on changes to this repository, on manual dispatch, and hourly
at minute 17 UTC to pick up upstream releases. A push to upstream does not
instantly trigger this repository. GitHub schedules may be delayed and
can be disabled after 60 days of repository inactivity; check Actions if this
copy stops updating. For an immediate update:

```sh
gh workflow run pages.yml --repo Lucasfrit/hydraulicanalogy-site
```

`/release.json` records the exact public upstream revision. Application source
and licenses remain in the upstream repository and published `/LICENSE`.

## Domain

GitHub Pages uses custom Actions publishing with custom domain
`hydraulicanalogy.com`. Set the custom domain in Pages settings before DNS.
Porkbun URL forwarding must be removed. Apex A records must be:

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

`www` CNAME must point to `lucasfrit.github.io`. The Porkbun GitHub template also
sets the four official GitHub Pages IPv6 AAAA records:
`2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`,
`2606:50c0:8003::153`. Preserve email and verification
records. Enable HTTPS enforcement once GitHub issues the certificate. The HTTPS
apex entry should return 200 and open `/app/`; HTTP and www should redirect to
the HTTPS apex, with no redirect to inertance.org.

On 7 October 2026 the forwarding rule was removed and these DNS records were
applied through Porkbun, with TTL 600 seconds. The two email MX records
(`fwd1.porkbun.com` priority 10, `fwd2.porkbun.com` priority 20), SPF TXT
(`v=spf1 include:_spf.porkbun.com ~all`) and two existing ACME
verification TXT records were preserved. Authoritative DNS and public
DNS-over-HTTPS confirm the new records. The domain serves the copy directly.
GitHub's Let's Encrypt certificate covers the apex and www names and expires
on 5 January 2027. HTTPS enforcement is enabled: HTTP and www redirect to
https://hydraulicanalogy.com/ with the requested path preserved. Live desktop
and phone smoke checks passed with normal DNS and TLS validation.

Local preparation, with a clean checkout of the public upstream repository:

```sh
python3 tools/prepare_site.py ../inertance-site /tmp/hydraulicanalogy-preview
```

To verify a new release after its deployment finishes:

```sh
gh run list --repo Lucasfrit/hydraulicanalogy-site --workflow pages.yml --limit 5
curl -fsS https://hydraulicanalogy.com/release.json
# From the sibling inertance-site checkout; use the expected app source stamp.
SITE_ORIGIN=https://hydraulicanalogy.com SOURCE_REV=763d364 node tools/check-live.cjs
```

The upstream revision in release.json is the primary repository commit, not this
repository's commit or the private simulator stamp. Routine app updates require
no Porkbun or certificate edits; update the primary generated app, then sync here.
