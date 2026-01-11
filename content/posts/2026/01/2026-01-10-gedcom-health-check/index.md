---
title: "A Health Check on My WheelerMcGinty GEDCOM"
date: 2026-01-10
slug: "gedcom-health-check-wheeler-mcginty"
categories: ["genealogy"]
tags:
  - gedcom
  - data-quality
  - wheeler
  - mcginty
  - mackenzie
  - tuttle
  - beasecker
  - places
  - cleanup
summary: "A quick, data-driven snapshot of my current GEDCOM export—tree size, top surname clusters, place hubs, and the cleanup tasks that make the stories stronger."
draft: false
---

Genealogy is equal parts *story* and *systems engineering*: you can’t write compelling narratives if the underlying data is messy.

So I periodically export my database to GEDCOM and do a quick “health check.” Here’s what the latest export reveals.

## Tree size (current export)
This GEDCOM currently contains:

- **Individuals:** 27,840  
- **Families:** 9,307  
- **Sources:** 1,040  
- **Media objects:** 1,555  

That’s a lot of people—and exactly why consistency matters.

## Top surname clusters
Counting surnames as recorded in `NAME` entries (which can include variant spellings and alternate names), the largest clusters include:

1. **Wheeler** — 1,936  
2. **Woodbury** — 997  
3. **Worcester** — 350  
4. **Tuttle** — 270  
5. **Baker** — 256  
6. **Rice** — 250  
7. **Tolles** — 244  
8. **Smith** — 227  
9. **Beasecker** — 209  
10. **Dodge** — 199  

This is useful for prioritizing what gets attention first—both for cleanup and for weekly story releases.

## The “quiet” problem: surname variants
GEDCOM exports make variant problems painfully obvious. Here are two clusters where the same line is currently split across multiple forms.

### McGinty / Ginty variants
- **McGinty** — 89  
- **Mc Ginty** — 5  
- **Mcginty** — 4  
- **Ginty** — 21  

### Mackenzie variants
- **Mackenzie** — 106  
- **MacKenzie** — 7  

These variants matter because they affect:
- tag pages (and what “counts” as the same family line)
- search quality
- duplicate detection
- exports and reports

If you’re researching these lines, try multiple spellings in Search.

## Place hubs: where the paper trail clusters
Place fields are inherently messy (“England” vs “Town, County, State”), but even with inconsistency you can still see strong hubs.

This export shows recurring concentration in:
- **Massachusetts** (especially Essex + Middlesex County towns)
- Midwest cluster: **Indiana / Ohio / Illinois (Chicago)**
- **England** (often recorded generically as “England”)
- A notable cluster in **Mazowieckie, Poland** (appears frequently in place fields)

This is why the site has dedicated **Places** and **Surnames** navigation now:
- **Surnames:** /surnames/
- **Places:** /places/
- **Browse hub:** /browse/

## Data quality checks (because genealogy runs on receipts)
A couple quick “sanity checks” surfaced:

- **Birth-after-death flags:** 24 records where the first captured birth-like year appears later than the first death-like year  
  (usually a swapped date, wrong attachment, or merge artifact)
- **Famous/historical duplicates:** multiple repeated identities (common after merging/importing)
- **Place formatting inconsistency:** the same location appearing in multiple formats

None of this is unusual. It’s just normal maintenance once a tree gets large.

## What I’m doing next
1. Normalize the big surname variants (McGinty/Ginty; Mackenzie/MacKenzie; etc.).  
2. Standardize place formats for the biggest hubs (MA towns/counties; Chicago IL; key Ireland/Poland locations).  
3. Use the cleaned dataset to drive weekly story releases by branch.

If you see a surname split or place variant that should be unified, send me a note.

**Contact:** /contact/
