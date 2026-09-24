# Analytic system card

## System

Curriculum Knowledge Graph

## Purpose

Directed curriculum graph for prerequisite reachability, isolated concept checks, and inspectable learning paths.

## Current maturity

Working research prototype. The bundled example checks the software path with synthetic inputs. It does not establish validity for real learners, instructors, courses, or workplaces.

## Inputs

See `../data/README.md` for the current synthetic schema and the documentation expected before real data are connected.

## Outputs

The current code produces reachable prerequisite descendants and isolated concept flags. These outputs are research signals and should be interpreted with the educational context that produced them.

## Evidence needed before real use

Sample graph edges for expert review, report precision and coverage, and test whether suggested prerequisite paths match established curriculum sequencing. Cycles and disconnected components should be inspected explicitly.

## Main limitation

The graph only knows relationships that are explicitly entered. It does not infer prerequisites from text, estimate mastery, or prove that a path is pedagogically optimal.

## Human oversight

A person must review any output before it can affect a learner, instructor, applicant, or employee.
