# Ethics, safety, and misuse risks

## Intended use

Curriculum Knowledge Graph is meant for research, prototyping, and educational design work. It should help people inspect a learning-related signal or decision, not make consequential decisions on their behalf.

## Human oversight

A person should be able to see what evidence produced an output, question it, and override it. If the system cannot explain a recommendation well enough for meaningful review, the recommendation should not be used in a high-stakes setting.

## Privacy

Collect only the data the study actually needs. Remove direct identifiers, document retention periods, restrict access to raw traces, and avoid storing free text, audio, video, or other sensitive material unless it is essential to the research question.

## Fairness

Overall accuracy can hide uneven errors. When it is lawful and ethically appropriate, inspect false alarms, missed support, calibration, and recommendation quality across relevant groups and contexts. Do not treat a single fairness metric as proof that a system is fair.

## Educational risk

A technically correct output can still lead to a poor learning experience. Watch for labels that become self-fulfilling, excessive nudging, over-support that removes productive struggle, or analytics that reward surveillance rather than learning.

## Uses excluded from this prototype

- autonomous grading, admissions, or disciplinary decisions
- employment decisions
- psychological or medical diagnosis
- covert monitoring or surveillance
- any deployment where affected people cannot understand or challenge the output

## Before a real-user study or deployment

Document consent or another lawful basis, data governance, access controls, subgroup evaluation, calibration where probabilities are used, human escalation paths, and clear rollback criteria.
