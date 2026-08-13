# GenAI Architecture Advisor

A small, contract-driven application for exploring AI architecture choices against explicit requirements, constraints, and reusable architecture pattern cards.

## Current scope

The current version is an offline walking skeleton. It:

1. Reads and validates a structured JSON architecture profile.
2. Loads architecture pattern cards through a `Retriever` interface.
3. Uses `StuffEverythingRetriever` to place every card into the synthesis context.
4. Produces a contract-shaped recommendation through a deterministic `FakeSynthesizer`.
5. Validates the resulting JSON report.
6. Renders both JSON and Markdown output.

The fake synthesizer does not call an LLM and does not make a genuine architecture judgment. It proves that the application wiring, contracts, citations, and report rendering work deterministically.

## Design decisions
- The recommendations are limited to the supplied architecture cards.
- Input and output are protected by JSON Schema contracts.
- Constraint and card IDs provide evidence traceability.
- The synthesizer interface is provider-neutral.
- The retriever interface allows the current whole-context approach to be replaced later without redesigning the pipeline.
- Cost and quality measurements are reported as unmeasured rather than invented.

## Scaling boundary
The current retriever includes every card in the synthesis context. This is intentionally simple and inspectable for a five-card MVP.

If the card corpus grows by 10×, context size and the model's position-related ability to use every card are likely to degrade first. A live LLM path would also experience increased token usage, latency, and cost. The trigger for replacing `StuffEverythingRetriever` is when the full corpus no longer fits the context budget or fails defined latency, cost, or recommendation-quality targets.

## Not implemented yet
- Live LLM integration
- Embeddings or vector databases
- Selective retrieval
- Cost calculation
- API or user interface

## Quick start

Python 3.13 is currently tested.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python test.py profiles/example1.json
```

## Verification

```bash
python -m pytest
ruff check .
ruff format --check .
```
