# Lessons Learned (recurring mistakes → rules)

Personal "second brain": mistakes that keep showing up in this user's code. Check EVERY item below during the deep scan, in addition to the stack checklists. Each rule is one line, concrete and checkable.

Format: `- [area] Rule — what to grep/inspect for. (added YYYY-MM-DD, from <project or audit>)`

## Rules

<!-- Add new bullets below. Examples of the intended style (delete or replace with real ones):
- [backend] Multi-step writes must run in one transaction — look for 2+ repository save/update calls in one service method without a transaction annotation/block.
- [security] Every "get/update/delete by id" checks ownership (IDOR) — compare resource.ownerId with the authenticated user in the handler or query.
- [frontend] Every async view has loading, empty and error states — look for data fetching with no `isLoading`/empty branch.
-->

## How rules get added

The auditor never edits this file on its own. At the end of a report, if a finding looks like a repeat habit (same mistake in 2+ places, or the user says "I always forget this"), list it under **Suggested new rules** as a ready-to-paste bullet in the format above. Append it here only after the user says yes.
