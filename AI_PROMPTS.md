# AI_PROMPTS.md

## Problem Encountered
We were trying to translate the A* search logic and priority queue system from Java to Python as per the Princeton OOP specification. We needed to ensure that no "enhanced for loops" or `enumerate()` constructs were used because we are restricted to basic `for element in seq` and `for i in range` structures. We also needed an immutable architecture and guidance for our Viva Voce.

## Prompt
> "write me a code in python wihout enhanced for loops adn enumerate loop you can use for each loop and for range loop and expalin me through commpents what me and my friend should do to achieve full score"

## Modifications to AI Output
- We reviewed the code provided by the AI (ChatGPT/Gemini) to ensure the OOP design was solid and all methods properly wrapped behind class accessors.
- We double-checked that `getters` were used for things like `.manhattan()` and `.hamming()` rather than exposing fields directly to maintain encapsulation perfectly.
- We deliberately built separate files to ensure classes are logically partitioned (i.e. we didn't put both classes in a single massive file which violates the grading rubric).
- We actively removed Python abstractions that violate data structure purity and stuck precisely to Min-Heap arrays using `heapq`.
