# Engineering decisions

These are the decisions that materially changed the implementation. The list is selective; it is not a reconstructed design document.

## 1. Separate relevance from eligibility

**Problem:** A semantically similar job may still be impractical because of geography, language, seniority, or employment constraints.

**Decision:** Keep corpus constraints, semantic retrieval, seniority context, language notes, and material readiness as separate layers.

**Cost:** More policy code and more states for the UI.

**Reason:** A blended score is simpler to implement but harder for a user to challenge.

## 2. Use embeddings for retrieval, not as the explanation

**Problem:** Keyword matching misses equivalent work described with different language, while a vector score is too opaque to show as a verdict.

**Decision:** Use multilingual e5 similarity to retrieve and rank, then explain the result with profile evidence, gaps, and human-readable context.

**Cost:** The explanation layer must be maintained separately from the retrieval signal.

**Reason:** Retrieval quality and user trust are different problems.

## 3. Keep raw ranking numbers private

**Problem:** A numeric fit score looked authoritative even when it combined uncertain inputs.

**Decision:** Return a coarse tier, evidence, one practical gap, and a language note. Keep similarity, weights, and the internal band label on the server.

**Cost:** The UI cannot offer a familiar percentage match.

**Reason:** The removed precision was cosmetic, not useful.

## 4. Make application claims deterministic

**Problem:** An unrestricted generator can produce persuasive material that is difficult to trace back to the candidate.

**Decision:** Compose from structured, resume-safe evidence and run claim checks before the pack is marked ready.

**Cost:** Less stylistic variation and more explicit profile preparation.

**Reason:** In a career product, traceability is more valuable than novelty.

## 5. Store the prediction with the decision

**Problem:** An outcome recorded weeks later cannot validate the model unless the original prediction is preserved.

**Decision:** Capture a prediction snapshot when the user applies, skips, or chooses to improve first.

**Cost:** More event metadata and versioning responsibility.

**Reason:** It creates a real prediction/outcome pair instead of retrospective guesswork.

## 6. Preserve user-elected states

**Problem:** Ranking policy changes can remove a role that a user already shortlisted or applied to.

**Decision:** User-selected workflow states bypass later recommendation gates.

**Cost:** Historical lists may contain roles that the current ranker would not surface.

**Reason:** The user's history is not disposable model output.

## 7. Split corpus data from personal state

**Problem:** The job corpus and user records have different access patterns and risk profiles.

**Decision:** Ship a corpus-only SQLite snapshot to the API service and keep user state in Supabase Postgres with row-level security.

**Cost:** Two storage paths and an explicit snapshot release step.

**Reason:** Personal data never needs to enter the corpus artifact, and the corpus can be replaced without migrating user history.

## 8. Publish evidence, not private source

**Problem:** A private project is difficult for a recruiter to inspect, but publishing the source would expose personal records, implementation strategy, and reusable ranking logic.

**Decision:** Publish schemas, aggregate evaluations, architecture, infrastructure, and machine-checked sanitized artifacts.

**Cost:** The public repository is not runnable.

**Reason:** It gives an interviewer concrete material to question without turning the private application into a template.
