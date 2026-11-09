# Memory dreaming for LLM agents: synthesis

*Written 2026-10-30, in maintainer mode. Built from the 20 source notes in `research/dreaming/sources/`. Lines marked **(inference)** are my own reading, not something a source states.*

---

## 1. What "dreaming" means

**Dreaming** (also called "sleep", "sleep-time compute", "background reflection" or "offline consolidation") is memory work an agent does **between** conversations rather than **during** them. It has three parts:

- **Inputs:** the agent's current memory plus the raw record of recent sessions.
- **Job:** clean up the memory and learn from the sessions.
- **Output:** a revised memory, ready before the next conversation starts.

The term took hold in 2025–2026:
- Letta's *sleep-time compute* (sources 01–03).
- Anthropic's *Dreams* for Claude Managed Agents, announced May 2026 (06–08).
- Research systems: Auto-Dreamer and MemDream (16, 17).
- Third-party write-ups of a Claude Code "Auto Dream" feature. These are unofficial and not in the Claude Code docs (10, 11).

Every source gives the same reason for it:

> Agents write to their memory incrementally, while they work. Those writes are local and hurried, so over many sessions memory "accumulates duplicates, contradictions, and stale entries" (Anthropic, source 06). In-session memory management also slows the conversation and gets "messy over time" (Letta, source 01).

The fix is to **split capture from consolidation**:
- Capture happens fast and in the moment.
- Consolidation happens slowly, offline, with a global view across sessions.

Anthropic puts it as "memory captures what an agent learns while it works; dreaming refines that memory between sessions" (source 07). Auto-Dreamer: "decouple fast per-session memory acquisition from slow cross-session consolidation" (source 16).

### The neuroscience analogy (only where it helps)

Auto-Dreamer cites **complementary learning systems** theory. The brain uses a fast learner (hippocampus) that records episodes, and a slow learner (neocortex) that gradually pulls general structure out of them. Sleep is when the fast system "replays" episodes to the slow one.

Two design rules follow from the analogy **(inference)**:
1. **Keep the episodes.** The hippocampal record isn't destroyed by consolidation. Zep stores episodes "non-lossily" (source 14), MemGPT keeps evicted messages in recall storage (source 04), and in Sage the session notes play this role.
2. **Consolidation is gradual and selective.** It extracts what recurs, not everything. MemDream's finding that repeated dreaming erodes rare facts (source 17) is the machine version of over-generalizing.

---

## 2. The building blocks

### Memory tiers
MemGPT's hierarchy (source 04) is the common reference point:

| Tier | MemGPT name | What it is | Who reads it |
|---|---|---|---|
| Core | system instructions + working context | small, always in the prompt | every turn |
| Recall | recall storage | the full raw history, searchable | on demand |
| Archival | archival storage | long-term facts and documents | on demand |

LangMem uses a different split (source 15):
- **Semantic** memory (facts), stored either as **profiles** (one current-state document) or **collections** (many records).
- **Episodic** memory (experiences).
- **Procedural** memory (how to behave: the prompt itself).

### What a dream pass actually does
Pooled across sources, the operations are:

| Operation | What it means | Seen in |
|---|---|---|
| **Dedupe / merge** | combine entries that say the same thing | Anthropic Dreams, Zep entity resolution, Mem0 UPDATE, Claude Code auto-dream (claimed) |
| **Resolve contradictions** | the newer value supersedes; the old one is invalidated, not erased | Zep (`t_invalid`), Mem0g (mark invalid), Anthropic ("replaced with the latest value") |
| **Decay / forget** | demote or remove stale entries | MemDream soft decay (×0.2, restorable), Generative Agents recency decay |
| **Promote** | short-term to long-term; fragment to file | Letta (raw → "learned context"), TiMem (observations → persona) |
| **Extract patterns / insights** | write higher-level statements, citing their evidence | Generative Agents reflections, Anthropic ("surface new insights", cross-agent patterns) |
| **Compress / rewrite** | shorten files and keep them high-signal | Letta, Auto-Dreamer (12× smaller bank), Claude Code (`MEMORY.md` ≤ 200 lines) |
| **Index / link** | maintain the index, links and aliases | A-MEM links, Zep communities, Claude Code `MEMORY.md` index |
| **Normalize** | e.g. relative dates → absolute | Claude Code auto-dream (claimed) |
| **Precompute** | answer likely future needs ahead of time | Sleep-time compute paper (source 02) |
| **Self-probe** | test the memory with likely queries, repair what fails | MemDream (source 17) |

### Triggers

| Trigger | Example | Notes |
|---|---|---|
| Step count / every N turns | Letta Code ("after a set number of completed agent steps") | Simple. Frequency trades cost against freshness. |
| Context compaction | Letta Code | Dream when the window is squeezed anyway. |
| Accumulated importance | Generative Agents (sum of importance > 150) | Heavy experiences trigger reflection sooner. |
| Time **and** activity | Claude Code auto-dream, claimed (≥ 24 h **and** > 5 sessions) | Avoids dreaming over nothing and dreaming too often. |
| Schedule | Anthropic Dreams ("users set how often agents dream") | Predictable. Runs whether or not anything changed. |
| Size threshold | Claude Code `MEMORY.md` limit warning; MemGPT 70% pressure warning | Cheap, and tied directly to the cost being controlled. |
| Manual | `/dream` (claimed); Letta "reorganize memory" requests | Highest control, lowest automation. |

### Inputs and outputs
- **Inputs** are nearly always (a) the current memory and (b) a bounded batch of recent raw sessions. Anthropic allows 1–100 sessions and advises starting small. Auto-Dreamer works on a **selected region** of memory at a time.
- **Outputs** come in three styles:
  - **In-place edits:** Letta sleep-time agents, Mem0.
  - **A new copy to review and swap in:** Anthropic Dreams ("the input store is never modified").
  - **Versioned in-place edits with history:** Letta MemFS on git, Anthropic memory versions.

---

## 3. Taxonomy of approaches

1. **In-context self-editing (the baseline, not dreaming).** The agent edits its own memory mid-conversation through tools (MemGPT). Everything happens on the "hot path".
2. **Write-time reconciliation.** Each new memory is checked against similar old ones at the moment it's written: Mem0's ADD/UPDATE/DELETE/NOOP, A-MEM's link-and-evolve, Zep's edge invalidation. It's consolidation, but local and online.
3. **Threshold-triggered reflection.** Synthesis runs when enough has happened: Generative Agents' reflection trees with cited evidence.
4. **Continuous background agents.** A second agent shares memory with the conversational one and rewrites it asynchronously, often: Letta sleep-time agents, LangMem background reflection.
5. **Batch offline dreams.** A scheduled or triggered job reads a batch of transcripts plus the memory, produces a consolidated memory, and is optionally reviewed before applying: Anthropic Dreams, Letta Code dreaming, Claude Code auto-dream (claimed).
6. **Hierarchical / temporal consolidation.** Memory is organized in levels by time or abstraction, and material moves up the levels: TiMem's temporal tree, Zep communities.
7. **Learned or self-probing consolidators (research).** The consolidation policy is trained or self-tested: Auto-Dreamer (RL-trained), MemDream (probe → diagnose → repair).

### Comparison

| Approach | Trigger | What it rewrites | Pros | Cons | Complexity |
|---|---|---|---|---|---|
| 1. In-context self-editing (MemGPT) | Every turn, model's choice | Working-context block; archival entries | Immediate; no extra infrastructure | Slows and clutters the conversation; messy over time; no global view | Low |
| 2. Write-time reconciliation (Mem0, A-MEM, Zep) | Every new memory | Neighboring entries / graph edges | Store stays consistent continuously; closed op set is auditable | Local view only; per-write LLM cost; usually needs embeddings or a graph DB | Medium–high |
| 3. Threshold reflection (Generative Agents) | Summed importance > threshold | Adds reflections (higher-level notes with citations) | Produces insight, not just tidiness; cites evidence | Hallucinated embellishment risk; reflections can stack abstractions on errors | Medium |
| 4. Continuous background agent (Letta sleep-time, LangMem) | Every N steps / idle | Core memory blocks, in place | Conversation stays fast; memory keeps improving | Frequent rewrites → drift; harder to review; token cost | Medium |
| 5. Batch offline dream (Anthropic Dreams, Letta Code, auto-dream) | Schedule, time + activity, size, manual | Whole store or a region → new copy or versioned commit | Global view across sessions; reviewable; cheap to revert | Lag until the next dream; a bad dream rewrites a lot at once | Low–medium |
| 6. Hierarchical consolidation (TiMem, Zep communities) | Per level: session, period, etc. | Higher-level summaries | Matches how people remember; short top level | Needs clear level rules; summaries go stale | Medium |
| 7. Learned / self-probing (Auto-Dreamer, MemDream) | Offline cycles | Selected regions; graph repair | Best benchmark results; finds gaps before they bite | Needs training data, GPUs, a benchmark; over-consolidation with many cycles | High |

---

## 4. Risks and failure modes

| Risk | What happens | Evidence | Mitigations seen |
|---|---|---|---|
| **Hallucinated memories** | The consolidator writes a "fact" that never happened | Generative Agents: embellishments, world-knowledge bleed, ~1.3% hallucinated (05) | Insights must cite source records (05); go back to source transcripts (16) |
| **Authority collapse** | An inference becomes a fact; a one-off remark becomes a standing rule; the source's limits are dropped | 48 of 49 consolidator setups showed it; authority labels cut unauthorized actions from 16.9% to 0% (19) | Persist *what kind of claim* each memory is, alongside its content |
| **Drift / compounding error** | Each rewrite paraphrases the last rewrite, and meaning walks away | MemDream: rare-fact retention −12–13% over 20 cycles; F1 fell from 5 to 8 rounds (17) | Rebuild from source episodes rather than the previous summary (16); limit frequency; soft-delete |
| **Loss of important detail** | Compression drops the rare but crucial item | Full context still beats Mem0 on raw accuracy (12); MemDream rare-fact loss (17) | Keep raw episodes (04, 14); "maximize recall, then precision" (09); soft decay instead of deletion (17) |
| **Wrong contradiction resolution** | "Newest wins" overwrites something still true | Zep "consistently prioritizes new information" (14) | Invalidate, don't delete (12, 14); flag rather than resolve when unsure **(inference)** |
| **Poisoning persistence** | Injected or wrong content gets consolidated into durable memory | Security survey (20); secondary coverage of Claude dreaming | Provenance, versioning, rollback (20); human review for high-stakes memory (06, 07) |
| **Privacy spread** | Sensitive details get copied into more files and summaries | Anthropic adds *redact* for versions (08); Dreams aren't ZDR or HIPAA eligible (06) | Fewer copies; pointer-not-copy; redaction **(inference: applies to Sage)** |
| **Cost** | Dreams scale with transcript count and length | Anthropic: cost "roughly linear" in sessions (06); Letta: frequency vs. tokens (01) | Small batches; only sessions since the last dream; region-scoped passes |
| **Runaway rewriting** | Every dream changes everything; reviews become impossible | Implied by Anthropic's copy-then-review design (06) and Letta's backup-before-reorganize (03) | One reviewable unit per dream; diff-size budget; "files that don't need changes are left untouched" (11, claimed) |

**Common safety pattern across the vendor systems (inference from 03, 06, 08, 20):**
- Raw logs are immutable.
- The dream writes to a copy or a versioned commit.
- There's a review step, optional or mandatory depending on stakes.
- Rollback is one step.
- Every change carries provenance: which run made it, from which sessions.

---

## 5. Evaluation: how people measure it

- **Retrieval / QA benchmarks:** LoCoMo (Mem0, A-MEM, MemDream, TiMem), LongMemEval (Zep, TiMem), DMR (MemGPT, Zep), MemoryAgentBench (MemDream). Metrics are LLM-as-judge accuracy (Mem0's J), F1 and BLEU.
- **Task success:** Auto-Dreamer +7 points on ScienceWorld; Harvey's ~6× completion rate with Anthropic dreaming (vendor-reported); Generative Agents' human believability ratings (TrueSkill).
- **Efficiency:** tokens per query (Mem0 >90% fewer), memory size (Auto-Dreamer 12× smaller, TiMem 52% shorter recall), latency (Zep ~90% lower), and sleep-time compute's 5× less test-time compute.
- **Safety:** unauthorized-action rate (19), hallucination rate (05), rare-fact retention across cycles (17).
- **Contradiction rate** appears only implicitly (as the problem dreams fix). No source I read reports it as a standalone metric.

**For a single-user, file-based system like Sage, none of these benchmarks apply directly (inference).** The practical equivalents are:
- **Startup token weight:** the attention-budget cost.
- **Counts of known decay signals:** stale threads, expired tags, undated profile items, unpromoted mentions, unresolved links.
- **Memory misses:** times the client had to remind Sage of something it should have known.
- **Review outcomes:** accepted, edited or reverted dream changes.

---

## 6. Takeaways that carry over to Sage (inference)

1. **Separate capture from consolidation.** In-session capture is already good: feedback is saved the moment it lands, and the session note is written. The heavy rewriting can move offline.
2. **Never touch the episodes.** `sessions/*.md` is the recall tier and stays read-only to any dream.
3. **One reviewable unit per dream.** Git already gives Sage what Anthropic built memory versions for.
4. **Keep the kind of each claim.** The client's words, Sage's observations and the client's rules stay distinct and in their own places. A dream never raises an item's authority.
5. **Flag, don't resolve, contradictions about the person.** A new statement may be a bad day, not a new truth.
6. **Rebuild summaries from the sessions, not from the previous summary.**
7. **Dream on "time and activity", not nightly.** Over-dreaming erodes rare facts.
8. **Self-probe with the next greeting.** The next session start is the most predictable "query" Sage will face.
