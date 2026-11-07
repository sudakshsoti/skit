# skit

Design skills for coding agents. This glossary names the ideas the skills share, so every skill, ticket and review uses the same word for the same thing.

## Language

**Tell**:
A visible sign that a design came from defaults rather than choices, such as gradient text or a pulsing status dot. Each tell has exactly one owner: a skill or the Critic.
_Avoid_: anti-pattern, slop pattern

**Move**:
A named kind of design change a user asks for, such as quieter, layout or typeset. Each move routes to exactly one owning skill.
_Avoid_: verb, command

**Project-local audit**:
An automatic check that runs on the project's own page and gives its findings to the Critic. Impeccable's detector is one example.
_Avoid_: detector scan

**Decisions record**:
The project's running list of design decisions, kept in `design/decisions.md` and written by `skit-design-grill`. Each line is either stated by the user or inferred and not yet confirmed.
_Avoid_: decisions file, decisions log

**About block**:
The short section at the top of the decisions record that says, in the user's own words, what the product is, who it's for and how it should feel.
_Avoid_: product context, product header

**Exception**:
A stated decision that allows one specific thing a tell or ban would otherwise flag, along with the reason. Inter as the brand font is an exception; Roboto in the same project is still flagged.
_Avoid_: ignore, override, allowlist
