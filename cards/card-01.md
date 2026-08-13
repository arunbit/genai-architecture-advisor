# [Stuff Everything in the prompt]

**Card ID:** CARD-001

## Problem and context

A simple solution is preferred or a fast solution (less development solution) is needed.

## How it works

Put all the data (or data cards) as the name suggests in the prompt—this way the LLM will get all the data in the prompt and can process it and read what is relevant for the query.

## Use when

When there is not that much data and expected data growth is also not significant.

## Avoid when

When the application or business-specific data is large OR unequal weightage (or lower weightage) of bias for some data (data cards) in the middle of the prompt can affect the system's business or acceptance criteria.

## Trade-offs

This architecture is useful when all the data available (or needed) can be brought together as in a query prompt. If the data is small and is not expected to grow, this approach would help save on development costs of building information pipelines or storage. However, as data size grows, the weightage of data in the middle of the prompt would go down, thereby affecting the quality of the application.

## Rejected alternative

Storing the necessary data or embeddings in a database such as a vector database and most other approaches that form a dedicated information/data pipeline for inference become unnecessary or rejected options when this option can be chosen.

## What breaks first at 10×

At 10x more data OR at a point when relevant cards are not getting identified properly, it must be the first trigger for failure. A swap must be in place. When a lower bias for data (or options) in the middle of the prompt relative to the data at the start and end appears, it should be a major telltale sign. When the data grows much larger (or even data growth is becoming larger), a separate information retrieval system that is relevant to the prompt has to be deployed.

## More info

https://aclanthology.org/2024.tacl-1.9.pdf
