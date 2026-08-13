# [Hierarchical summary retrieval for corpus-level questions]

**Card ID:** CARD-004

## Problem and context

Corpus-level questions require the entire corpus of information.

## How it works

Hierarchical summaries of data are used before generation.

## Use when

Broad thematic searches across the whole corpus.

## Avoid when

Local chunk-level questions OR information that changes so fast that summaries are no longer fresh.

## Trade-offs

RAPTOR trees have to be maintained and kept fresh.

## Rejected alternative

Simple flat top-k chunk retrieval is not good for global queries.

## What breaks first at 10×

Derived summaries are stale and updating the indexes is expensive.

## More info

RAPTOR paper: https://openreview.net/pdf?id=GN921JHCRw
