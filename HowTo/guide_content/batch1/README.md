# PNG community guides — Batch 1 (8 October 2026)

The five Markdown files here are the editorial source for IPA company incorporation, RTA vehicle ownership transfer, IRC monthly Salary and Wages Tax (Form S2), IRC GST registration, and business bank accounts (BSP, Kina, Westpac).

## Publication

Django migration HowTo.0003_seed_batch1_png_guides imports these into the existing HowTo and HowToStep models. It creates a disabled editorial attribution account (wikonomi_guides_editorial), labels the pages as community guides (is_official=False), provides citations and source dates, and creates an initial version-history snapshot. Existing guides with the same exact title are not changed.

Run in the deployment environment, using the site's normal migration process:

    python manage.py migrate
    python manage.py showmigrations HowTo

Then visit /howto/ and check the five new public entries and their source links. Git merging alone does not insert data unless that deployment applies the migration.

## Editorial and compliance caveats

- Tax rules: Income Tax Act changes took effect in 2026. Confirm latest IRC Form S2 and withholding calculation guidance.
- GST: Verify the live IRC application channel; no unconfirmed form-screen instructions are represented as authoritative.
- RTA: K115 is the published fee found in the cited regulation, not a fresh local counter quote.
- Banking: Bank fees, minimum balances, accepted IDs and onboarding rules can change.
- IPA: Distinguish company incorporation from business-name registration and foreign-enterprise certification.

The "Editorial verification notes" section in each Markdown document is not imported into the reader-facing guide. Updating the Markdown will not rerun a completed migration: use the live guide editing/version-history workflow instead.

## Validation

Run:

    python manage.py test HowTo

The tests check source structure, presence of official-source links, research dates and removal of editorial-only notes. The existing display now uses Django's urlize filter for clickable source URLs.
