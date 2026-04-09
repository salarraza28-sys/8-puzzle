# AI_PROMPTS.md

## Problem Encountered
We are implementing the A* search logic and priority queue system in Python, following the Princeton OOP specification. We also needed an immutable architecture and guidance for our Viva Voce.

## Prompt
We asked the AI to explain a clear Proof of Concept (POC) for the 8-puzzle solver project using the A* algorithm in Python, including how the classes should be structured and how the priority queue works.

## Modifications to AI Output
- We refined the explanation to better understand the overall flow of the A* algorithm before coding.
- We ensured the class design (Board and Solver) was clearly separated and aligned with OOP principles.
- We focused on understanding how the priority queue (Min-Heap) manages nodes based on cost.
- We simplified the explanation so it could be easily presented during Viva Voce.
- We double-checked that `getters` were used for things like `.manhattan()` and `.hamming()` rather than exposing fields directly to maintain encapsulation perfectly.
- We deliberately built separate files to ensure classes are logically partitioned (i.e. we didn't put both classes in a single massive file which violates the grading rubric).
- We actively removed Python abstractions that violate data structure purity and stuck precisely to Min-Heap arrays using `heapq`.
