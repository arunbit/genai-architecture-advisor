# [Query Decomposition workflow]

**Card ID:** CARD-005

## Problem and context

When single query can not cover the multi-part request and multiple queres are needed

## How it works

Based on the request, multiple subqueries are intiated and synthesized onto a single forkflow

## Use when

When single query can not cover the multi-part request and multiple queres are needed

## Avoid when

A single query (or no query) is sufficient for generation

## Trade-offs

Multi-part querying infrastrucrture has to be maintained

## Rejected alternative

WHen a single query or a flat infrastructure is sufficient

## What breaks first at 10×

The latency required is not sufficient
