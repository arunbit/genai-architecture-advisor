# [Hybrid (vector and keyword) Retrival]

**Card ID:** CARD-003

## Problem and context

When information needed cant be just be obtained semantically from vector search or just from basic keyword search (BM25)

## How it works

Reciprocal Ranked Fusion (RRF) merges both the vector search and BM25 using ranked lists

## Use when

When systems are able to process the right amounts of data to form the merged lists within the allowed latecy to create highly relevant data before generation

## Avoid when

The latency requied to do an effective merged ranking does not agree with the expected latency OR simply data is too small for this approach to be sued.

## Trade-offs

Expensive to manage multiple systems (BM25 and vertical db ) to be current and effective to have the latency within target

## Rejected alternative

Dense or RAG only retrival

## What breaks first at 10×

The cost of bringing together the merged list starts exceeding the latency expecation  and then finally the data exceeds so much that the latency is also exceding way beyond tolerable levels.
