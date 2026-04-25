# DECKARD_BOUNDARY_PLAN_chatgpt_ingest.md

A boundary map for ingesting the user's ChatGPT chat archive into a queryable database that surfaces MTG-related prompts, outputs, designs, and "desires" — and feeds those into MTGSLIDER's database, the workspace memory layer, or system documentation.

Companion to [DECKARD_BOUNDARY_PLAN.md](DECKARD_BOUNDARY_PLAN.md) (the scholarship-triangulation plan). Same Deckard discipline: name where deterministic Python ends and where LLM judgement begins, name the gates between them, name what NOT to use AI for.

This plan does not prescribe implementation. Slice planning happens via `/plan-runciter-slice`.

---

## The shape of the input

OpenAI's user data export produces a `.zip` containing:
- `conversations.json` — the full chat history as a structured tree (message roles, timestamps, message content, parent IDs)
- `message_feedback.json` — thumbs-up/down history
- `model_comparisons.json` — A/B comparisons (only for users in eval programs)
- a few smaller files (user profile, shared links)

The user's chat archive may or may not currently exist locally. Step zero is locating it. If absent, the user can request a fresh export from chat.openai.com (Settings → Data Controls → Export Data).

---

## DETERMINISTIC TASKS

### D1. Archive intake
**Why deterministic:** Unzipping a file and reading JSON is mechanical.
**Artifact:** `cache/chatgpt_archive/<export_date>/conversations.json` (raw, never edited). Provenance: `imported_at`, `archive_export_date`, `source_filename`.

### D2. Conversation tree → flat message rows
**Why deterministic:** `conversations.json` is a tree of messages with parent_ids. Flattening to per-conversation linear threads, then to a `messages` table, is graph traversal — pure code.
**Artifact:** `chat_conversations` and `chat_messages` tables with `(conversation_id, message_id, parent_id, role, model, created_at, content_text, content_format)`.

### D3. Token-level metadata
**Why deterministic:** Word count, character count, language detection (via `langdetect` or `cld3`), URL extraction (regex), code-block extraction (markdown fence regex) — all algorithmic.
**Artifact:** columns on `chat_messages`: `word_count`, `lang`, `has_code`, `urls[]`.

### D4. Topic-keyword filter for MTG relevance
**Why deterministic:** A conservative first pass uses a hand-curated keyword list ("Magic the Gathering", "MTG", "Scryfall", "Commander", "Modern", "Standard", "Pioneer", card-name patterns like `\b[A-Z][a-z]+ Bolt\b`, format-keyword tokens). This is grep, not AI.
**Artifact:** `chat_messages.mtg_relevance_score` (0.0–1.0, deterministic from keyword density + regex hits) and `chat_messages.mtg_relevance_method='keyword'`.

### D5. Conversation-level provenance
**Why deterministic:** Title, first message timestamp, last message timestamp, model used, total tokens, message count — all are aggregations.
**Artifact:** `chat_conversations` columns: `title`, `started_at`, `last_active_at`, `model_used`, `message_count`, `mtg_relevance_score` (max of message scores).

### D6. Cross-references to MTGSLIDER cards
**Why deterministic:** If a chat message contains card names, fuzzy-match each to Scryfall (the existing `scryfall.named(..., fuzzy=True)` works for this) and store the (chat_message_id, scryfall_id) edge. The fuzzy match itself uses Scryfall's logic, not an LLM.
**Artifact:** `chat_message_card_refs` table with `(chat_message_id, scryfall_id, match_confidence, matched_text)`.

### D7. Federated entity exposure
**Why deterministic:** Per `CONTEXT_ENGINEERING.md`, this database (call it `chatgpt_archive.db`) gets its own `entities` table that the federated reader can query alongside Claudiens, EmeraldTablet, MTGSLIDER, etc.
**Artifact:** `entities` rows with `entity_type='chat_conversation'` or `'chat_design_idea'`, summary fields filled by D8/P3 below.

---

## PROBABILISTIC TASKS

### P1. Topic classification at the conversation level
**Why probabilistic:** "What was this 200-message conversation actually about?" is a summarisation + classification task that keyword filters get only partly right. The LLM can read the full thread and produce a structured `(primary_topic, secondary_topics[], summary, design_artifacts_mentioned[])`.
**Validation:** lands in `chat_conversations.llm_topic_classification` with `model_used`, `classified_at`, `review_status='unreviewed'`. The user spot-reviews high-relevance conversations; low-relevance (D4 score < 0.2) may stay unreviewed indefinitely without harm.

### P2. Design-idea extraction
**Why probabilistic:** "What concrete designs, prompts, schemas, or product ideas did the user propose in this conversation?" is exactly the kind of structured extraction LLMs do well and parsers do badly. The output is a list of typed objects: `(idea_type, summary, exemplar_quote, position_in_conversation)`.
**Validation:** `chat_design_ideas` table with full provenance (`source_message_id`, `extracted_by_model`, `extracted_at`, `confidence`, `review_status='unreviewed'`). **Promoted ideas can flow into MTGSLIDER's `PARKING_LOT.md` or `ROADMAP.md` only after human review.**

### P3. "Desires" extraction
**Why probabilistic:** "Desires" — the user's term for things they wished a system could do, asked an LLM to help with, or described as the future of a project — are hard to define and hard to extract with regex. An LLM with the conversation + a clear instruction ("identify statements of the form 'I wish', 'it would be nice if', 'we could', 'eventually I want', and similar") produces a useful first pass.
**Validation:** `chat_desires` table with `source_message_id`, `desire_text`, `extracted_at`, `model_used`, `review_status='unreviewed'`. **Desires are never promoted directly to ROADMAP.md** — they enter PARKING_LOT.md as candidate ideas first, where they go through normal scoping discipline.

### P4. Cross-conversation theme linking
**Why probabilistic:** "These three conversations from different months are all about the same MTG slideshow project" is fuzzy linking the LLM does better than `LIKE` queries.
**Validation:** `chat_conversation_themes` with `(theme_id, conversation_id, confidence, proposed_by='LLM', review_status='unreviewed')`.

### P5. Linking design ideas to existing MTGSLIDER state
**Why probabilistic:** "This idea from a March 2025 chat is the same thing I parked as 'topic intelligence reframe' in MTGSLIDER's PARKING_LOT" is a semantic match across two corpora. LLM-suggested, human-confirmed.
**Validation:** `chat_idea_mtgslider_links` with full provenance and a review gate.

---

## VALIDATION LAYERS

### V1. The "draft → reviewed" wall (same as primary plan)
LLM-extracted topics, design-ideas, desires, and links land as `unreviewed`. Nothing flows into MTGSLIDER's published artifacts without promotion.

### V2. The "raw conversation is sacrosanct" wall
The `cache/chatgpt_archive/<export_date>/conversations.json` is **never edited**. All derived data lives in the SQLite database; if the analysis is wrong, regenerate from the raw archive. This protects against LLM-induced corruption of the user's actual chat history.

### V3. The "MTG-relevance gate" wall
Only conversations or messages with `mtg_relevance_score > 0.2` (or another tunable threshold) get LLM topic classification (P1) or design-idea extraction (P2). Below the threshold, the LLM is not invoked. This bounds cost and prevents the LLM from wasting cycles on conversations about REAPER or Brautigan or the user's other projects.

### V4. The "private-content gate" wall
The user's chat history likely contains personal material (medical, legal, family, financial). The intake script must support a `--exclude-keywords` flag and a `chat_excluded_messages` table where messages matching certain regexes (e.g. SSN patterns, medical-term lists) are FLAGGED and EXCLUDED from LLM-passed corpora. This wall is OFF by default — the user must opt in to exclusion lists, since the cost of false-flagging legitimate content is real.

---

## BOUNDARY VIOLATIONS TO AVOID

### W1. WASTE — Asking an LLM to flatten the conversation tree
Don't. `conversations.json` has a documented schema. Tree traversal is 50 lines of Python. The LLM cannot improve on this.

### W2. WASTE — Asking an LLM to detect MTG relevance at the message level
Don't, at least not as the first pass. Keyword + regex is fast, free, and good enough to filter the corpus. The LLM gets invoked on what survives the filter.

### W3. RISK — Hardcoding which topics count as "MTG project ideas"
Don't write a regex for "design ideas". The user's design idiolect is project-specific and evolving. P2 needs LLM judgement; the gate is the unreviewed-status, not a regex.

### W4. DANGER — Auto-promoting extracted "desires" into ROADMAP.md
Don't. Desires found in chat may be aspirational, contradictory, abandoned, or already shipped. They MUST land in PARKING_LOT.md (where they survive contact with the planning protocol) and from there be promoted (or not) by the user.

### W5. DANGER — Sending the entire archive to an LLM in one call
Don't. The archive may contain personal material the user does not want shared with any model. Use V3 (relevance gate) to bound what gets sent. For very high-relevance conversations the user wants summarised in full, that's an explicit opt-in per-conversation, not a default.

### W6. WASTE — Re-extracting from the same conversation across sessions
Don't. Cache LLM extractions keyed by `(conversation_id, model_used, prompt_version)`. Re-runs only when a new model or new prompt is being tried.

---

## ARTIFACTS PRODUCED

| Boundary | Artifact | Producer | Promotion path |
|---|---|---|---|
| D1 | `cache/chatgpt_archive/<date>/` raw files | Python (unzip) | direct |
| D2 | `chat_conversations`, `chat_messages` rows | Python (parser) | direct |
| D3 | metadata columns on chat_messages | Python | direct |
| D4 | `mtg_relevance_score` | Python (keyword scorer) | direct |
| D6 | `chat_message_card_refs` | Python (Scryfall fuzzy) | direct |
| D7 | `entities` row per conversation/idea | seed_entities.py | direct |
| P1 | `chat_conversations.llm_topic_classification` | LLM | human review |
| P2 | `chat_design_ideas` rows | LLM | review → optionally promoted to MTGSLIDER `PARKING_LOT.md` entry |
| P3 | `chat_desires` rows | LLM | review → optionally promoted to MTGSLIDER `PARKING_LOT.md` |
| P4 | `chat_conversation_themes` | LLM | review |
| P5 | `chat_idea_mtgslider_links` | LLM | review |

---

## INTEGRATION WITH MTGSLIDER

The chat archive does NOT live inside MTGSLIDER. It lives at its own path (suggested: `C:\Dev\ChatGPTArchive\` to keep it personal and gitignored separately). MTGSLIDER does not depend on it.

What MTGSLIDER *can* do is read the chat archive's `entities` table via the federated reader (per `CONTEXT_ENGINEERING.md`), so during an MTGSLIDER session an LLM can pull "what did I say about this in chat" as a context source for slide writing or theme curation.

**The integration is read-only and federated, not embedded.** If the chat archive is deleted, MTGSLIDER continues to work.

---

## SUMMARY — THE BOUNDARY IN ONE SENTENCE

**Deterministic Python owns:** archive unpacking, conversation-tree flattening, metadata extraction, MTG-relevance keyword scoring, card-name fuzzy matching, federated entity exposure.

**LLMs own:** topic classification, design-idea extraction, desire extraction, cross-conversation theme linking, linking chat ideas to existing MTGSLIDER state — all with explicit review gates.

**The most important rule, repeated from the primary plan:** no LLM-extracted desire becomes an MTGSLIDER roadmap item without passing through PARKING_LOT.md and the planning-protocol scoping pass. Chat history is *suggestive*, not *prescriptive* — the user's past wishes do not bind the user's present priorities.
