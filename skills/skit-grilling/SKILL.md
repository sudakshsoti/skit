---
name: skit-grilling
description: "Use to stress-test a plan, decision, or idea by interviewing the user in rounds until nothing is left assumed, or when the user says 'grill me'. Asks through the harness's question tool when it has one. For visual or behavioural interface decisions, or 'grill me on the design', use skit-design-grill."
---

# Grilling

Interview the user until the two of you share one picture of the thing. Be relentless: an assumption you never say out loud is the costliest kind, because nobody sees it until it ships.

## The tree and the frontier

Treat the topic as a **decision tree**: each decision opens the decisions that depend on it. The **frontier** is every decision whose prerequisites are already settled, so you can ask it now without guessing at an answer you haven't heard.

Work in **rounds**:

1. Compute the frontier.
2. Ask every frontier question in one round. Each question carries your recommended answer, worded so that "yes" accepts it.
3. Wait for the answers.
4. Fold the answers in. Settled decisions push the frontier outward, and a surprising answer can reopen a branch you thought was closed.
5. Repeat.

A question that depends on another question still open in the same round waits for a later round.

## Facts are yours, decisions are theirs

When a question needs a fact (what the code does, what a file says, what a tool supports), look it up yourself, with a subagent if the lookup is long. Never ask the user for something you can find. Only the questions downstream of a pending lookup wait for it; ask the rest of the frontier now.

Decisions belong to the user. Put each one to them, even when you are confident, and wait.

## Asking

**Default: the question tool.** When the harness has a structured question tool (`AskUserQuestion` in Claude Code, or its equivalent elsewhere), ask every question through it:

- One question per frontier decision, 2 to 4 options each. Put your recommendation first and end its label with "(Recommended)". The tool adds a free-text "Other" option itself.
- The user may see only the dialog, not your earlier messages. Write each question so it stands alone: name the thing being decided and the fact that makes it matter.
- The tool takes up to 4 questions per call. For a bigger round, make several calls one after another, then fold all the answers in before recomputing the frontier.
- Read answers literally. An "Other" answer can change the question itself, for example "give me options for each one". Follow what it says rather than mapping it onto your nearest option.
- A question with no natural options (a name the user must supply, a free description) goes in plain text in the same turn.

**Fallback: numbered text.** When there is no question tool, write the round as text and stop:

```
❓ **Q1** - **<title>**: <the question, with any choices spelled out>

➡️ <your recommended answer>

---

❓ **Q2** - ...
```

## Done

The grill is done when the frontier is empty: every branch visited, nothing silently assumed. Then summarise the shared understanding (the decisions, what was ruled out, and what happens next) and ask the user to confirm it. Do not start acting on the plan until they do.
