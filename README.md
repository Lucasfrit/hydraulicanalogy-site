# Hydraulic Analogy hosting

This repository hosts https://hydraulicanalogy.com/ and its circuit simulator
at https://hydraulicanalogy.com/app/. It serves the same released educational
Inertance application directly, without forwarding visitors to inertance.org.

## Releases

GitHub Actions reads the public `Lucasfrit/inertance-site` main branch, copies
only visitor pages and assets, rewrites the primary-domain URLs for this domain,
and deploys an artifact to GitHub Pages. No private simulator checkout or secret
is needed. Source/build folders and project documents are excluded from the
deployment. The app runtime and presets are unchanged.

The workflow runs on changes to this repository, on manual dispatch, and hourly
at minute 17 to pick up upstream releases. GitHub schedules may be delayed and
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

`www` CNAME must point to `lucasfrit.github.io`. Preserve email and verification
records. Enable HTTPS enforcement once GitHub issues the certificate. The apex
should serve HTTP 200; www should redirect to this apex, with no redirect to
inertance.org.

Local preparation, with a clean checkout of the public upstream repository:

```sh
python3 tools/prepare_site.py ../inertance-site /tmp/hydraulicanalogy-preview
```
