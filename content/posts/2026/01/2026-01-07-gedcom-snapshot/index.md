---
title: "What My GEDCOM Reveals: A Snapshot of the WheelerMcGinty Tree"
date: 2026-01-07
slug: "gedcom-snapshot-wheeler-mcginty"
categories: ["genealogy"]
tags: ["gedcom", "wheeler", "mcginty", "mackenzie", "tuttle", "data-cleanup", "places", "surnames"]
summary: "A quick, data-driven snapshot of my WheelerMcGinty GEDCOM—top surnames, geographic hubs, and the cleanup tasks that make the stories stronger."
draft: false
---

This site is built from two things: stories and receipts. The “receipts” live in my working genealogy database, and one way I keep myself honest is by periodically exporting a GEDCOM and asking: **what does the tree actually contain?**

Below is a snapshot of the current GEDCOM export.

## Tree size (current export)
- **Individuals:** 27,840  
- **Families:** 9,307  
- **Sources:** 1,040  
- **Media objects:** 1,555  

(Counts are taken directly from the GEDCOM record types.)

## Top surname clusters
Counting surnames as they appear in GEDCOM `NAME` entries (which can include alternate names), the largest clusters are:

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

These counts are useful not just for “what’s big,” but for deciding what to prioritize for cleanup and story releases.

## A real-world problem: surname variants
One thing GEDCOM exports reveal immediately is **how often a surname splits into variants** (spacing, capitalization, indexer choices, etc.). A few examples from this export:

### McGinty / Ginty variants
- **McGinty** — 89  
- **Mc Ginty** — 5  
- **Mcginty** — 4  
- **Ginty** — 21  

### Mackenzie variants
- **Mackenzie** — 106  
- **MacKenzie** — 7  

This matters because it affects:
- tag pages (e.g., `/tags/mcginty/` vs `/tags/ginty/`)
- search relevance
- duplicate detection

Normalizing variants is one of the fastest ways to make the public site feel “clean.”

## Geography: where the paper trail clusters
Place fields are messy by nature (“England” vs “Town, County, State”), but even with inconsistencies you can see strong hubs.

### Birthplace signals (high-level)
By occurrences in birth place entries, the strongest hubs include:
- **Massachusetts** (especially Essex + Middlesex County towns)
- **England** (often recorded generically as “England”)
- Midwest clusters: **Indiana**, **Ohio**, **Illinois**
- A notable cluster in **Poplacin, Mazowieckie, Poland** (shows up frequently)

### Death place signals
Top death places include:
- **England** (again, often generic)
- **Beverly, Essex, Massachusetts**
- **Chicago, Cook, Illinois**
- **Concord, Middlesex, Massachusetts**
- **Poplacin, Mazowieckie, Poland**

This helps me decide which “place hubs” deserve dedicated pages and which tags should be curated.

## Data quality checks (because genealogy runs on receipts)
A few cleanup flags surfaced in this export:

- **24 records** where the first captured birth-like year is later than the first death-like year  
  (usually a swapped date, wrong attachment, or a merge artifact)
- **Duplicate “historical/royalty” profiles** (common after importing/merging)
- **Place formatting inconsistency**
  (“England” vs “Town, County, Country”)

None of these are fatal. They’re just the normal maintenance work of a long-running tree.

## What I’m doing next
1. Normalize the biggest surname variants (McGinty/Ginty; Mackenzie/MacKenzie; etc.).  
2. Standardize places for the biggest hubs (Essex/Middlesex MA; Chicago IL; key Ireland/Poland locations).  
3. Use the cleaned dataset to drive weekly story releases by branch.

If you’re connected to any of these families—or if you notice a place/surname split that should be merged—please reach out via Contact.
