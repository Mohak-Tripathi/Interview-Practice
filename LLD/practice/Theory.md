# LLD + Domain-Driven Design — Learning Summary
> Documented from first-principles discovery session · July 2026

---

## 1. The Core Realization: LLD is Not a New Paradigm

**Starting belief:** LLD (low-level design), design patterns, SOLID principles are a completely different world from the backend development done in the last four years.

**What was discovered:** They are the **same paradigm (OOP)**, same code, same language. The only thing that changed is **where the behavior lives**.

The variable that made them feel different was never the database. It was the **address of the business logic**.

---

## 2. The One Core Difference: Anemic vs Rich

This is the entire intellectual foundation. Everything else follows from it.

### Anemic Domain Model (last 4 years)
- Objects are **dumb data bags** — just fields, no rules, no behavior
- All business logic lives in the **fat service layer**
- The service reaches INTO the object, reads its state, decides, mutates it from the outside
- Named anti-pattern by Martin Fowler (2003): [AnemicDomainModel](https://martinfowler.com/bliki/AnemicDomainModel.html)

```python
# ANEMIC — service reaches in and decides everything
class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        self.id = spot_id
        self.type = spot_type
        self.is_occupied = False          # public, anyone can touch

class ParkingService:
    def park(self, spot, vehicle_type):
        if spot.is_occupied:              # service ASKS spot's state
            raise Exception("Occupied")
        if spot.type != vehicle_type:     # service DECIDES compatibility
            raise Exception("Wrong type")
        spot.is_occupied = True           # service reaches in and mutates
```

### Rich Domain Model (LLD / DDD way)
- Objects own their **state AND the rules** about that state
- Service layer becomes **thin** — it only sequences (load → tell → save)
- The object is **told** what to do, and it guards itself

```python
# RICH — the spot decides about itself
class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        self.id = spot_id
        self._type = spot_type            # hidden
        self._is_occupied = False         # hidden

    def can_fit(self, vehicle_type):      # spot answers its OWN question
        return not self._is_occupied and self._type == vehicle_type

    def occupy(self, vehicle_type):       # TELL it — it guards itself
        if not self.can_fit(vehicle_type):
            raise Exception("Cannot occupy")
        self._is_occupied = True          # only the spot touches its own state

    def release(self):
        self._is_occupied = False

class ParkingLot:
    def park(self, vehicle_type):
        spot = next((s for s in self._spots if s.can_fit(vehicle_type)), None)
        if not spot:
            raise Exception("No spot available")
        spot.occupy(vehicle_type)         # TELL — orchestrator does not decide
        return Ticket(spot, vehicle_type)
```

### The Migration Table — same rules, different address

| Rule | Anemic — lives in | Rich — lives in |
|---|---|---|
| "Is this spot free and compatible?" | `ParkingService.park` | `ParkingSpot.can_fit` |
| "Mark spot occupied" | service sets `spot.is_occupied = True` | `ParkingSpot.occupy` |
| "Is this ticket valid?" | `ParkingService.exit` | `Ticket.validate` |
| "How many hours parked?" | service does datetime math | `Ticket.parked_hours` |
| "Free the spot on exit" | service sets `spot.is_occupied = False` | `Ticket.close → spot.release()` |

**Nothing about the logic changed. Its address changed.**

---

## 3. Why the Fat Service Worked for 4 Years (and Why It Breaks in LLD)

### Why it worked: the framework did the heavy lifting

In Express/Rails/Node work:
- The **framework gave you the layers for free** (route → controller → service). You never *decided* to separate concerns — the framework handed you empty boxes and you filled them. That separation IS a design decision, made by the framework author.
- Objects stayed dumb because the **framework made anemic the path of least resistance**. ORM hands you a plain row; the easy thing is to put logic in the service.
- Behavior barely varied — every request hit the same code path with different data. The framework absorbed all variation as data, so you never felt the need for polymorphism.

**The framework was your SOLID. It did the architecture for you.**

### Why it breaks in LLD

LLD interviews deliberately do three things that break the MVC safety net:

1. **Remove the framework** — no route, no controller, no ORM. You must invent all boundaries.
2. **Remove the database** — storage is a dict in memory.
3. **Inject behavior variation** in the extensibility step — "now pricing differs by vehicle type" — and the moment behavior varies, the fat-service pattern produces an unmaintainable if/else.

The god-orchestrator that produces one giant service is exactly what the framework was preventing by giving you multiple layers. Without it, anemic collapses into a blob.

---

## 4. The Key Principle: Tell, Don't Ask

**Ask (wrong):** Service reads the object's state, makes a decision, then mutates the object.

```python
if spot.is_occupied:            # ASK
    raise Exception()
spot.is_occupied = True         # then mutate from outside
```

**Tell (right):** Service issues a command. The object guards itself.

```python
spot.occupy(vehicle_type)       # TELL — object decides if it can, then does it
```

**Rule:** Data-specific rules ("is this cell occupied?") → belong in the entity that owns that data. Workflow rules ("sequence these three steps") → belong in the orchestrator.

---

## 5. When Behavior Varies → Strategy Pattern (and why it appears)

The if/else-on-type is the smell:

```python
# SMELL — every new pricing rule is surgery on this method
def calculate_fee(self, vehicle_type, hours):
    if vehicle_type == VehicleType.MOTORCYCLE: return hours * 10
    if vehicle_type == VehicleType.CAR:        return hours * 20
    if vehicle_type == VehicleType.LARGE:      return hours * 30
```

The fix — replace the if/else with objects sharing an interface:

```python
class PricingStrategy:
    def price(self, hours): raise NotImplementedError

class FlatHourlyPricing(PricingStrategy):
    def __init__(self, rate): self._rate = rate
    def price(self, hours): return hours * self._rate

class WeekendSurgePricing(PricingStrategy):
    def __init__(self, rate, multiplier): ...
    def price(self, hours): return hours * self._rate * self._multiplier

# New rule = ADD a class. Never EDIT the ones that work.
```

**The insight:** Polymorphism, Strategy pattern, and Open/Closed Principle are NOT three things. They are one move — replace if/else-on-type with objects sharing an interface.

**The trigger:** A requirement *varied*. No variation, no pattern. Never force a pattern preemptively — the delivery framework says it explicitly: "name the pattern after the design fits, not before."

---

## 6. Domain-Driven Design (DDD) — What It Is and What to Use

**One-sentence definition:** DDD is the philosophy that in complex software, the business domain should be modeled directly in code as rich objects, and everything technical (database, HTTP, frameworks) should be pushed to the edges so it never contaminates the business logic.

### Tactical DDD — the four terms to own

| Term | What it is | Example |
|---|---|---|
| **Entity** | Object with identity + lifecycle + its own rules | `ParkingSpot`, `Ticket`, `User` |
| **Value Object** | Just a label/type, no identity, no lifecycle, immutable | `VehicleType` enum, `Money` |
| **Repository** | The ONLY thing that talks to storage | `UserRepository`, `TicketRepository` |
| **Application Service** | Thin orchestrator — sequences load/tell/save | `ParkingLot`, `UserService` |

### Strategic DDD — skip for now

Bounded contexts, aggregates, domain events, CQRS, ubiquitous language — real concepts, wrong time. Not tested in LLD interviews. Not needed for SDE2. Stop reading any DDD article the moment these words appear.

### Key articles

- **Martin Fowler — Anemic Domain Model:** https://martinfowler.com/bliki/AnemicDomainModel.html (the foundational text — you found this yourself)
- **Microsoft — Tactical DDD:** https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-ddd (the four patterns explained cleanly)

---

## 7. The Three-Layer Architecture — Both in Production and in LLD

The architecture is identical in both contexts. Only the bottom layer differs.

```
         ┌─────────────────────────┐
         │   Application Service   │  ← thin orchestrator
         │  (ParkingLot / Service) │    sequences: load → tell → save
         └────────┬────────────────┘
                  │ calls both
        ┌─────────┴──────────────┐
        │                        │
┌───────▼────────┐    ┌──────────▼──────┐
│  Domain Object │    │   Repository    │
│  (Rich Entity) │    │                 │
│                │    │  Interview:     │
│ owns state     │    │  dict / list    │
│ owns rules     │    │                 │
│ knows NO infra │    │  Production:    │
└────────────────┘    │  Prisma/Postgres│
                      └─────────────────┘
```

**Critical rule: the rich domain object never calls the repository. Ever.**

Three reasons:
1. **Testability** — if the object calls a repo, every unit test needs a fake DB. Rich objects must be testable with zero infrastructure.
2. **Transaction control** — the service must wrap a transaction around the full use case. If the object saves itself mid-method, that control is lost.
3. **Circular dependencies** — `User` importing `UserRepository` which returns `User` objects = a mess.

### The three-step dance (same in LLD and production)

```python
def update_password(self, username, new_password):
    user = self._repository.get_by(username)         # 1. LOAD (service → repo)
    updated = user.update_password(new_password)     # 2. TELL (pure logic in object)
    return self._repository.update(updated)          # 3. SAVE (service → repo)
```

Step 2 runs on Mars — no database, no framework, no dict. Pure. That's the testability claim.

### Test to apply to every line of code

> If a step **decides something about the domain** → it belongs in the rich object.
> If a step **moves data across a boundary** → it belongs in the service or repository.

---

## 8. Storage in LLD Interviews (No Database)

In an interview there is no Postgres. Storage is a Python dict.

**Level 1 — dict on the orchestrator (90% of problems)**

```python
class ParkingLot:
    def __init__(self, spots):
        self._spots = spots
        self._active_tickets: dict[str, Ticket] = {}   # this IS the database
```

Use for: parking lot, chess, elevator, vending machine, tic-tac-toe.

**Level 2 — dict behind a Repository class (extensibility signal)**

```python
class TicketRepository:
    def __init__(self):
        self._store: dict[str, Ticket] = {}

    def save(self, ticket): self._store[ticket.id] = ticket
    def find(self, ticket_id): return self._store[ticket_id]
```

Use for: Splitwise, hotel booking, Uber, Bookmyshow, library management — problems with multiple entity types where interviewer will ask "how would you scale this?"

**The extensibility answer, delivered at the right moment:**
> "Active tickets currently live in a dict as `InMemoryTicketRepository`. If we moved to production Postgres, only `TicketRepository` would change — `ParkingLot` and `Ticket` would not move a line."

That single sentence, at Step 5 of the delivery framework, is a senior-level signal.

---

## 9. The 2×2 That Kills the Confusion Forever

The database and the behavior-location are **two independent axes**. Not one.

|  | With DB (Postgres/Prisma) | In-memory only |
|---|---|---|
| **Anemic** (logic in service) | Your last 4 years (TerriSage, most CRUD) | LLD attempt if you keep the fat-service habit |
| **Rich** (logic in objects) | DDD in production (Repository + rich entities) | LLD interview ideal |

You were reading a vertical difference (anemic vs rich) as a horizontal one (DB vs no-DB). That was the entire knot.

---

## 10. How the ORM Hid All of This

When you write `prisma.ticket.create(...)` and `prisma.ticket.update(...)`:

- **Prisma was silently being your repository.** The object↔row translation, the load-by-id, the save-back — that entire middle layer exists in your apps right now, but Prisma wrote it, so you never wrote a class for it.
- **The ORM made anemic the default.** Prisma hands you a plain data object (a row). The path of least resistance was to put logic in the service. You didn't choose anemic — the tool chose it for you and hid the alternative.

**The payoff of doing it raw:** Once you've built the repository and the rich object by hand, you'll look back at Prisma and see the seams — "oh, `.create()` is a repository save, `.findUnique()` is a repository load, the row it hands me is an anemic model I could have made rich." That x-ray vision is what raw development gives you.

---

## 11. When Anemic is FINE (and Fowler's Caveat)

Fowler is polemical. He calls anemic an anti-pattern. He's right in the context of complex domains. He underweights this: for genuine CRUD with thin logic (most of TerriSage: create lead, update property, list orders), **anemic + ORM is the pragmatic right call** — simpler, faster, less object↔row translation cost. Whole industries ship this deliberately.

The mature position: **anemic is a choice you were making implicitly. Now you can make it consciously**, and reach for rich when the behavior justifies it.

**When rich objects earn their place:**
- Multiple entities interlink with non-trivial rules (parking exit: ticket validates itself, computes fee, releases a spot)
- Behavior varies by type (pricing strategies, vehicle types)
- Objects have lifecycle with state transitions (ticket: active → used)
- The extensibility question will be asked ("what if pricing changes?")

**When anemic is fine:**
- Simple CRUD: create, read, update, delete with minimal rules
- Each service owns a flat slice of the domain with little interlinking
- No behavior variation expected
- Speed of delivery matters more than long-term extensibility

---

## 12. The Personal Framework for Entity Detection (Step 2 of LLD)

Your data-ownership lens from backend experience applies directly. Restatements in DDD vocabulary:

**A. Does the system own this data?** → Entity (class)
**B. Does it just classify or label something?** → Value Object (enum)
**C. Does it change over time?** → Entity (has mutable state → has behavior)
**D. Who performs actions?** → Orchestrator / Application Service
**E. Is this relationship current-state or historical?** → determines runtime reference vs DB FK
**F. If the server crashed, would I need this back?** → DB table (but in LLD: just a dict)

**The smell test for enum vs entity:**
> "If I made a table for this, what would I store? Just `id, type`? Then it's an enum, not an entity."

**The runtime vs DB distinction:**
> The database models ALL OF TIME. The runtime object graph models THIS INSTANT.
> `ParkingSpot → many Tickets` (DB, historical). `ParkingSpot` holds one current `Ticket` reference (runtime, present).

---

## 13. The Reference File

**`anemic_vs_rich.py`** — complete Python translation of the Medium article (Matthias Schenk). Contains:
- DTOs (Data Transfer Objects) — what they are and why they exist
- Full anemic implementation (AnemicUser + fat AnemicUserService)
- Full rich implementation (RichUser with factory, validation, use-cases as methods + thin RichUserService)
- In-memory repositories for both
- Runnable demo that shows the core difference live:
  - Anemic: you can build an invalid user by bypassing the service. Nothing stops you.
  - Rich: you cannot build an invalid user. The object refuses at construction.

**Kotlin → Python idiom map from that file:**

| Kotlin | Python |
|---|---|
| `data class` | `@dataclass(frozen=True)` |
| `sealed interface` | ABC base + fixed subclasses |
| `require(cond) { "msg" }` | `if not cond: raise ValueError("msg")` |
| `companion object fun create()` | `@classmethod def create_from(cls, ...)` |
| `init { }` block | `__post_init__(self)` |
| `copy(field = newVal)` | `dataclasses.replace(obj, field=new_val)` |
| `object Validator` (singleton) | `class Validator` with `@staticmethod` |

---

## 14. What Comes Next

The theory is complete. The only remaining work is **reps**.

1. **Build parking lot end-to-end** from blank file, 45 min, no references:
   - Rich `ParkingSpot` and `Ticket` (state + behavior, no infra dependency)
   - Thin `ParkingLot` orchestrator with a dict for storage
   - Optional: a `TicketRepository` class wrapping the dict

2. **Review against the LLD rubric after every attempt:**
   - Did any business rule leak up into the service?
   - Did any infra concern leak down into the domain object?
   - Can `ParkingSpot` and `Ticket` be unit-tested with zero infrastructure?
   - What are the 3 questions an interviewer fires at the extensibility seams?

3. **The extensibility scenario to prep:**
   - "Spot assignment should now pick the *nearest* spot, then *cheapest* spot." Where does this change go? (Hint: a new strategy object. The orchestrator should not change.)
   - "Pricing now varies by vehicle type." Where does this change go? (Hint: `PricingStrategy` interface + implementations. `ParkingLot` should not change.)

---

*The one sentence that contains everything:*
**The service loads and saves. The object decides. The repository hides how loading and saving work.**