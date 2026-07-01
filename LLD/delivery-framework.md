# LLD Delivery Framework
*Hello Interview — "Low-Level Design in a Hurry," condensed.*
*Doubles as study reference + self-review rubric. ~35 min total. You lose points on pacing, not knowledge.*

**This folder:** `delivery-framework.md` (you, pacing + rubric) · `.cursor/rules/design-principles.mdc` (agent, OOP/SOLID coaching + post-review)

---

## Pacing card

```
0:00   Requirements    → spec + out-of-scope list
5:00   Entities        → nouns + ownership arrows (orchestrator first)
8:00   Class design    → state + behavior per class, each tied to a requirement
20:00  Implementation  → core methods; happy path, then edge cases
28:00  Trace scenario  → verify tick-by-tick, out loud
30:00  Extensibility   → point to clean boundaries, stay high-level
35:00  Done
```
*If the interviewer pulls you off this, follow them, then guide back.*

---

## 1 · Requirements (~5 min)
Turn the one-line prompt into a confirmed spec. Probe four themes: **primary capabilities**, **rules / completion conditions**, **error handling**, **scope boundaries**. Write a numbered requirements list + an explicit *out of scope* list. Confirm before moving on.

- ✅ **Followed:** 4–6 concrete requirements; out-of-scope stated; confirmed with interviewer.
- ❌ **Lost points:** jumped to classes/code with no spec; requirements vague; scope never bounded.

## 2 · Entities & Relationships (~3 min)
Pull the meaningful nouns. Filter: *owns changing state or enforces rules* → entity; *just data on something else* → field. Map ownership: name the **orchestrator**, mark who owns durable state, draw has-a / uses / contains. Plain boxes and arrows — no UML.

- ✅ **Followed:** orchestrator named; ownership explicit; no micro-object sprawl.
- ❌ **Lost points:** everything a field (or everything an entity); no orchestrator; modeled every word in the prompt.

## 3 · Class Design (~10–15 min)
Top-down, orchestrator first. Per class derive from requirements — **State** (what it must remember) and **Behavior** (methods, each mapping to a requirement).
**Tell, Don't Ask:** rules live with the entity that owns the state. Data rules ("is this cell occupied?") → owning entity. Workflow rules ("can this run right now?") → orchestrator.

- ✅ **Followed:** every field/method traces to a requirement; small focused APIs; rules co-located with the state they touch.
- ❌ **Lost points:** getters everywhere with logic in the caller; god-orchestrator holding all state; methods with no requirement behind them; bloat.

## 4 · Implementation (~10 min)
Ask first: pseudo-code or full code in a language? Implement the *interesting* methods — the ones showing how classes cooperate and how state transitions. **Happy path first**, then enumerate edge cases (invalid input, illegal state, out-of-range). Patterns only when they earn their place — forcing one is a more common failure than omitting one.

- ✅ **Followed:** happy path clean; edge cases enumerated; logic sits in the right class.
- ❌ **Lost points:** drowned in edge cases before structure was clear; pattern shoehorned in; logic leaked into the wrong class.

## 5 · Verify + Extensibility (~5 min)
Trace one concrete, non-trivial scenario tick-by-tick — initial state, each operation, each state change. Fix any bug on the spot (positive signal). Then handle the interviewer's "what if…" by pointing to where your existing boundaries make the change cheap — don't rewrite.

- ✅ **Followed:** verified own logic in a trace; caught/fixed bugs live; extension answered by pointing at existing seams.
- ❌ **Lost points:** skipped verification; extension forces a redesign or a pile of special cases.

---

## 6 · Design Principles Review (~after implementation)

*Learn by doing — don't memorize pattern names. Apply concepts when requirements demand them; the agent coaches during design and reviews after.*

### Mindset
- **KISS, DRY, YAGNI, Separation of Concerns, Law of Demeter** — start simple; abstract only when variation or duplication forces it.
- **OOP shows in the design:** encapsulation (hide state, expose behavior), abstraction (interfaces for variation), polymorphism (no type-switching), composition over inheritance.
- **SOLID** — don't recite; use when it clarifies a choice (SRP for focused classes, OCP for extension seams, etc.).
- **Patterns:** 0–2 per problem is normal. Name the pattern *after* the design fits, not before.

### When to reach for what (quick map)
| Requirement signal | Natural direction |
|---|---|
| Multiple interchangeable behaviors | Interface + polymorphism (Strategy) |
| Caller shouldn't pick concrete class | Factory |
| Many optional fields / messy construction | Builder |
| Layer behaviors at runtime | Decorator |
| One simple entry over complex internals | Facade |
| Behavior depends on state + transitions | State machine |
| Many listeners on one event | Observer |

### Self-review rubric (add to step-by-step ✅/❌)
- ✅ **Encapsulation:** fields private; rules on the owning class; no logic leaking to orchestrator.
- ✅ **Right abstraction:** interface only where requirements vary; no switch-on-type where polymorphism is obvious.
- ✅ **Composition:** no deep inheritance trees; interfaces preferred.
- ✅ **Appropriate complexity:** no pattern stuffing; no god-class; every class traces to a requirement.
- ❌ **Lost points:** forced Factory/Strategy with one implementation; public mutable state; orchestrator enforces entity rules; missing obvious interface when requirements say "support multiple X."

### Post-session Design Review (agent delivers)
1. **Score X/10** with one-line justification.
2. **Strengths** — what was correctly applied.
3. **Gaps** — bare-minimum misses only (obvious interface missed, encapsulation broken, etc.).
4. **Over-engineering** — patterns/classes that don't earn their place.
5. **Top 3 interviewer follow-ups** on weak seams.

*Cursor rule `.cursor/rules/design-principles.mdc` (in this folder) automates coaching during LLD work and this review after implementation.*

---

*Self-review use: after a blind attempt, score each step ✅/❌ against the "Followed / Lost points" lines in sections 1–5, then run section 6 Design Principles Review, then list the 3 questions an interviewer would ask about the design's weak seams.*