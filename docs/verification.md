# Verification

The public artifacts are sanitized summaries of private development reports. They are useful only when their definitions and limits remain visible.

## Evidence chain

| Public artifact | Private source type | What was removed |
|---|---|---|
| Ingestion snapshot | Corpus and source reports | Job rows, source URLs, company-specific configuration |
| Migration verification | Live migration report | Credentials, project identifiers, record contents |
| Pack-ready scorecard | Fixed harness results | Job descriptions, profile details, generated material |
| Regression sentinel | Repeated material checks | Baseline files and private paths |
| Security review | Pre-user API review | Repository paths, secrets, tokens, exploit detail |
| Fit payload schema | Public API contract | Ranking weights and internal score fields |

## Automated public checks

The verifier in scripts/verify_public_artifacts.py runs without third-party packages. It:

1. parses every JSON artifact;
2. recomputes the migration total from table counts;
3. validates adapter, evaluation, score, and regression arithmetic;
4. checks required fields in the public fit schema;
5. verifies that relative Markdown links resolve;
6. rejects unbalanced fenced code blocks.

The check does not prove the private source reports are true. It proves that the public claims remain internally consistent with the artifacts committed beside them.

## Material-score interpretation

The 3.98, 4.27, and 5.00 values are internal fixed-rubric averages on the six cells that cleared the readiness gate. They are not external reviews or recruiter response rates.

The stronger result is the shape of the evaluation:

- four different synthetic profiles;
- five role families;
- strong, stretch, and weak-fit cases;
- a separate readiness decision;
- one failing pack-ready cell retained as a named limitation.

## Migration total

The live migration report lists:

- 1 profile;
- 50 skill rows;
- 1,943 jobs;
- 1,943 job-state rows;
- 0 outcome rows;
- 2,023 action rows;
- 6,709 rejection-event rows.

Those rows sum to **12,669**. The verifier recomputes this value from the public artifact.

## Limits

- The ingestion figures describe one recorded snapshot, not current corpus size.
- Company counts depend on the normalisation state at that snapshot.
- Internal rubric scores are useful for comparing revisions, not for claiming universal writing quality.
- Byte-identical output proves repeatability, not correctness.
- The security review was a pre-user pass, not a penetration test or compliance certification.
- No customer count, revenue, placement, interview-rate, or public-production claim is made here.
