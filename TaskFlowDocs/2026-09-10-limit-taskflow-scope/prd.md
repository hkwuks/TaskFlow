# Limit TaskFlow to development requests
> Task version: v1
> Status: checking

## Goal

Prevent TaskFlow from creating Todo items and task documents for ordinary non-development requests.

## Requirements

- Automatically use TaskFlow only for requests that modify a repository or deliver a development artifact, including features, bug fixes, refactors, tests, configuration/build/CI changes, and release preparation.
- Do not use TaskFlow for explanation, translation, status queries, read-only research, review, or diagnosis when no implementation is requested.
- If a later request asks to implement a change discovered during diagnosis/research/review, start TaskFlow at that implementation request.
- An explicit request to use `$taskflow` opts the work into TaskFlow even when it is planning or research.
- Apply the boundary before Todo intake or task-document creation.

## Acceptance Criteria

- Skill discovery metadata states the development-only boundary.
- The Skill checks applicability before Todo intake.
- README and artifact guidance agree with the same boundary.
- A focused smoke assertion guards both the exclusion and explicit-invocation override.

## Scope

- In scope: project Skill, its artifact reference, README files, and focused smoke checks.
- Out of scope: installed caches, user configuration, Hook-based prompt classification, and deletion of mistaken historical task files.

## Version History

- v1 — approved development-request boundary.
