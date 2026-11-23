# Lessons Learned (recurring mistakes → rules)

Personal "second brain": mistakes that keep showing up in this user's code. Check EVERY item below during the deep scan, in addition to the stack checklists. Each rule is one line, concrete and checkable.

Format: `- [area] Rule — what to grep/inspect for. (added YYYY-MM-DD, from <project or audit>)`

## Rules

- [backend] Multi-step writes must run in one transaction — look for 2+ repository save/update/delete calls in one service method without a transaction annotation/block. (added 2026-11-23, user-listed habit)
- [security] Every "get/update/delete by id" checks ownership (IDOR) — compare the resource's owner id with the authenticated user in the handler or query; a route with only an id param and no user filter is a finding. (added 2026-11-23, user-listed habit)
- [frontend] Every async view has loading, empty and error states — look for data fetching with no pending/loading branch, no empty-list branch, or no error branch. (added 2026-11-23, user-listed habit)

<!-- Add new bullets above this line. -->

## How rules get added

The auditor never edits this file on its own. At the end of a report, if a finding looks like a repeat habit (same mistake in 2+ places, or the user says "I always forget this"), list it under **Suggested new rules** as a ready-to-paste bullet in the format above. Append it here only after the user says yes.
