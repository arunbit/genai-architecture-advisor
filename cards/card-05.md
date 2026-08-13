# [Query Decomposition Workflow]

**Card ID:** CARD-005

## Problem and context

When a single query cannot cover the multi-part request and multiple queries are needed.

## How it works

Based on the request, multiple subqueries are initiated and synthesized into a single workflow.

## Use when

When a single query cannot cover the multi-part request and multiple queries are needed.

## Avoid when

A single query (or no query) is sufficient for generation.

## Trade-offs

Multi-part querying infrastructure has to be maintained.

## Rejected alternative

When a single query or a flat infrastructure is sufficient.

## What breaks first at 10×

The required latency cannot be met.
