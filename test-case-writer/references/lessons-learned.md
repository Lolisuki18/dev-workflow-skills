# Lessons Learned (recurring test gaps → rules)

Test scenarios this user's code repeatedly fails or forgets. During Step 2 (design), add a test case for every rule below that applies to the feature.

Format: `- [area] Always test X — why / how it usually breaks. (added YYYY-MM-DD, from <project>)`

## Rules

<!-- Add new bullets below. Examples of the intended style (delete or replace with real ones):
- [auth] Always test that user A cannot read/update/delete user B's resource (IDOR) — expect 403/404.
- [backend] Always test rollback: force the 2nd step of a multi-step write to fail and assert the 1st is not persisted.
- [frontend] Always test loading, empty-list and error states of every data-driven view.
-->

## How rules get added

Never edit this file on your own. When a test run exposes a defect that looks like a repeat habit, add under **Suggested new rules** in the test report a ready-to-paste bullet in the format above, and append it here only after the user says yes.
