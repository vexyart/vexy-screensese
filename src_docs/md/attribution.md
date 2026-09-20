# Attribution

Vexy Screensese is an AGPLv3 fork of [Cap](https://github.com/CapSoftware/Cap), © Cap Software, Inc. Most of the documentation under **Cap Docs** in this site's navigation is adapted from Cap's own documentation, licensed AGPLv3, with the following changes:

- Rebranded from "Cap" to "Vexy Screensese" throughout, except where a sentence refers to the upstream project, `cap.so`, or Cap Software, Inc. by name.
- Pages that only concern the commercial cap.so cloud offering — billing, teams and organizations, sharing/comments/analytics/embeds on cap.so, the migration tooling, the REST API and webhooks, and the cap.so-integrated agent tooling — have been left out, since they do not apply to a self-hosted install.
- Internal links were rewritten to point at the pages that were actually kept, or turned into plain text where the target page was left out.
- A handful of sentences were adjusted by hand for accuracy once rebranded (for example, self-hosting's `git clone` instructions now point at this fork).

Portions adapted from the Cap documentation, © Cap Software, Inc., AGPLv3.

The import is done by [`src_docs/import_cap_docs.py`](https://github.com/vexyart/vexy-screensese/blob/main/src_docs/import_cap_docs.py), a repeatable script — re-run it whenever the upstream docs change.
