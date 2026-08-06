# [Stuff Everything in the prompt]

**Card ID:** CARD-001

## Problem and context

 A simple solution is  prefered  or a fast solution (less development solution) is needed

## How it works

Put all the data (or data cards) as the name suggests in the prompt - this way the LLM will get all the data in the prompt and can process it and read what is relevant for the query.

## Use when

When there is not that much data and expected data growth is also not significant

## Avoid when

When the application or business-specific data is large  OR unequal weightage (or lower weightage) of bias for some data (data cards) in the middle of the prompt can affect the system's business or acceptance citeria

## Trade-offs

This arachiectural approach is useful when all the data available (or needed) can be broght together as in query prompt. If the data is small and is not expected to grow, this approach would help save on development costs of building information pipelines or storage.  However, as data size grows the weightage of data in the middle of the prompt would go down and therby affecting the quality of the application.


## Rejected alternative

Storing the necesary data or embeding in a database such as vertical database and most other apporches that form a dedicated information/data pipeline for inference become unncessary or rejected options when this option can be choosen

## What breaks first at 10×

At 10x more data OR at a point whene relevant cards are not getting identified propery - it must be the first trigger for failure.  A swap must be in-place, When a lower bias  for data (or options) that are on the middle of the the prompt relative to the data at the start and end  shoule be major tell-tell sign. When the data grows way larger (or even a data growth is becomeing larger, a separate information retrieval system that is relevant to the prompt has to be deployed)
