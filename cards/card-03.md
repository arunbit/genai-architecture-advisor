# [Hybrid (vector and keyword) Retrieval]

**Card ID:** CARD-003

## Problem and context

When information needed can't be obtained semantically from vector search alone or from basic keyword search (BM25) alone.

## How it works

Reciprocal Rank Fusion (RRF) merges vector search and BM25 using ranked lists.

## Use when

When systems are able to process the right amounts of data to form the merged lists within the allowed latency to create highly relevant data before generation.

## Avoid when

The latency required to do an effective merged ranking does not agree with the expected latency OR the data is simply too small for this approach to be used.

## Trade-offs

It is expensive to manage multiple systems (BM25 and a vector database) so they remain current and effective while keeping latency within the target.

## Rejected alternative

Dense-only retrieval.

## What breaks first at 10×

The cost of bringing together the merged list starts exceeding the latency expectation, and then finally the data grows so much that the latency also exceeds tolerable levels.
