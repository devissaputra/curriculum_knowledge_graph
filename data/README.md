# Data Documentation

## Included data
`sample.csv` contains only synthetic records created for smoke tests and demonstrations.

## Expected use
A synthetic curriculum graph is included; CSV import templates support course-specific mapping.

## Minimum schema
See the header of `sample.csv`. Production adapters should validate types, missing values, timestamp semantics, and learner/session boundaries before analysis.

## Do not commit
Personally identifiable information, raw student submissions, private LMS exports, proprietary course content, video/audio recordings, or licensed datasets that prohibit redistribution. Keep sensitive material outside Git and reference it through local paths or an approved secure store.

## Dataset card requirement
For any real experiment, record source, license/consent basis, population, collection period, exclusions, preprocessing, missingness, known biases, and permitted uses.
