# Issue tracker: Plane

The backlog for this repo is the **Skit** project (identifier `SKIT`) in the Plane Cloud workspace `oklch`, at `https://app.plane.so/oklch/`. Work items are named `SKIT-<n>`. GitHub Issues are not used for this repo; GitHub stays the home for code and PRs.

## Access

No official Plane CLI exists, so use the REST API: base `https://api.plane.so/api/v1/workspaces/oklch`, header `X-API-Key`. The key is `op://Homelab/Plane API/credential`. Scope it to one command and never echo it:

```sh
# on the homelab box (homelab ADR-0036); on the Mac use `op read` with the ambient token
PLANE_API_KEY="$(op-homelab read 'op://Homelab/Plane API/credential')" python3 plane_task.py
# Plane sits behind Cloudflare: send a non-default User-Agent (python-urllib's default gets error 1010)
```

Skit project id: `b207c470-53f0-43e6-af74-4cbae8ef3a95`. Below, `$P` = `/projects/<project id>` and `<id>` = a work item UUID.

## Conventions

- **Read a work item**: `GET /work-items/SKIT-<n>/` resolves the identifier to the full item, including its `id`. Comments: `GET $P/work-items/<id>/comments/`. Relations: `GET $P/work-items/<id>/relations/`.
- **List work items**: `GET $P/work-items/?per_page=100&expand=labels,state`. Results are cursor-paged: follow `next_cursor` while `next_page_results` is true. Filter labels and state groups client-side.
- **Search**: `GET /work-items/search/?search=<text>`.
- **Create a work item**: `POST $P/work-items/` with `name`, `description_html`, `priority` (`urgent`/`high`/`medium`/`low`/`none`), `labels` (label UUIDs) and, for a sub-item, `parent`.
- **Comment**: `POST $P/work-items/<id>/comments/` with `comment_html`.
- **Apply / remove labels**: `PATCH $P/work-items/<id>/` with the full new `labels` list. Label UUIDs come from `GET $P/labels/`.
- **Close**: comment, then `PATCH` `state` to the `Done` state (`Cancelled` for wontfix). State UUIDs come from `GET $P/states/`. States: Backlog, Todo, In Progress, Done, Cancelled.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_ PRs stay on GitHub. Put the `SKIT-<n>` identifier in the PR title or commit message.

## When a skill says "publish to the issue tracker"

Create a work item in the Skit project.

## When a skill says "fetch the relevant ticket"

`GET /work-items/SKIT-<n>/`, then its comments.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single work item with **child** work items as tickets.

- **Map**: a single work item labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body.
- **Child ticket**: a work item whose `parent` is the map. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: Plane's native relations. Add an edge with `POST $P/work-items/<child id>/relations/` and body `{"relation_type": "blocked_by", "issues": ["<blocker id>"]}`. Plane records the inverse `blocking` edge itself. A ticket is unblocked when every `blocked_by` item is in the Done or Cancelled state.
- **Frontier query**: list the map's children (`parent` = map id) that are not Done or Cancelled. Drop any with an open `blocked_by` item or an assignee. The lowest `sequence_id` wins.
- **Claim**: `PATCH` the item's `assignees` to your member id (`GET /members/`). This is the session's first write.
- **Resolve**: comment the answer, set the state to Done, then append a context pointer (gist + `SKIT-<n>`) to the map's Decisions-so-far.
