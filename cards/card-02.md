# [Top-K Vector Retrieval Augmented Generation (RAG)]

**Card ID:** CARD-002

## Problem and context

When highly relevant data can be retrieved in chunks from a huge corpus (usually from a vector database using embeddings) and the queries require updated or specific data.

## How it works

Before any generation, queries retrieve relevant chunks of information (usually using embeddings) that are used for the generation.

## Use when

When relevant information can be retrieved and other non-relevant information can be easily avoided before generation by using information retrieval systems.

## Avoid when

Unreliable retrieval of relevant data, when data is too large or complicated to be retrieved before generation, or the entire dataset is small enough that it's perfectly okay to have all the data in one spot in the prompt (like prompt stuffing).

## Trade-offs

Significant trade-offs are due to the need to maintain the relevance, freshness, and size of the chunks of data retrieved using data pipelines and databases.

## Rejected alternative

Having all the relevant and non-relevant data in the prompt when this system is possible and the size of the data chunks demands this approach.

## What breaks first at 10×

Relevant chunks don't appear as the first sign of a problem. When important and highly relevant documents don't even make it before generation, either the full pipeline has to be updated OR this whole RAG approach might even have to be evaluated.

## More Info

RAG NeurIPS paper by Patrick Lewis et al: https://proceedings.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf
