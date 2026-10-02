# Message Classifier — Credit/Debit Card Customer Support (US)

Classifies free-text customer support messages into structured fields and writes
them to a CSV. Built as Project 1 of a 13-week self-study plan (Week 4, Days 11–12).

---

## Domain

Messages customers send to the support team of a credit/debit card issuer in
the United States.

## Fields and allowed values

### category
- `lost_stolen_card`
- `charge_dispute`
- `account_locked`
- `account_reactivation`
- `general_inquiry`

### sentiment
Measures the customer's **TONE**, not how bad their situation is.

- `positive` — thanks, praise, or satisfaction with the service
- `neutral` — states the problem factually; may be worried or urgent, but is
  not angry at the company
- `negative` — frustrated, angry, sarcastic, complains about the company or the
  process, uses all caps or insults

A customer reporting a stolen card calmly is `neutral`, even though the
situation is bad.

### priority
- `high` — money is at risk right now, or the customer cannot access their funds
- `medium` — real problem, no immediate urgency
- `low` — informational question

### summary
One sentence, 15 words max.

## Data rule

Never full card numbers, SSNs or any other possible real private data.
Never include card digits at all, not even the last four — refer to it simply
as "the card".

## Labeling rules (tie-breakers)

These exist so that I label consistently across all rows, and so the model
gets the same criteria I use. Every one of them is also in the system prompt.

- No clear information to judge urgency → `priority = medium`, until further
  understanding of the problem
- Lost/stolen card mentioned at all → `category = lost_stolen_card`, regardless
  of what else the message asks
- Priority is set by the situation, not by whether the message is phrased as a
  question
- Feature requests and product complaints → `general_inquiry`
- `account_reactivation` is treated with `medium` priority to keep customers
  enrolled and satisfied
- `general_inquiry` → `low`, unless the customer also reports being unable to
  use their card or account right now

---

## Files

| File | What it does | Run frequency |
|---|---|---|
| `data_generator.py` | Generates 200 synthetic messages across 10 angles → `messages.csv` | Once |
| `classifier.py` | Defines `classify(text)` → dict with the four fields. Holds the system prompt. | Imported |
| `run_classifier.py` | Classifies all 200 → `results.csv` | Once per full run |
| `pick_rows.py` | Picks 10 random messages → blank `labels.csv` | Once |
| `run_eval_batch.py` | Classifies only the 20 labeled rows → `eval_results.csv` | Once per experiment |
| `run_evals.py` | Compares `labels.csv` vs `eval_results.csv`, prints accuracy + disagreements | Once per experiment |
| `cost.py` | One API call, reads `usage`, computes cost per message / 200 / 100,000 | On demand |

### Data files

| File | Contents |
|---|---|
| `messages.csv` | 200 synthetic customer messages, one column: `text` |
| `results.csv` | All 200 classified |
| `labels.csv` | 20 rows labeled by hand — the ground truth |
| `eval_results.csv` | The same 20 rows classified by the model |

## How to run

```
cd semana-04/clasificador

# full pipeline (200 messages, ~3 min, ~$0.15)
python3 run_classifier.py

# evaluation loop (20 messages, ~20 s, ~$0.015)
python3 run_eval_batch.py
python3 run_evals.py

# cost measurement (1 call)
python3 cost.py
```

Requires `ANTHROPIC_API_KEY` in the root `.env` of the repo.

---

## Results

Measured against 20 hand-labeled rows. `summary` is not evaluated: it is free
text and cannot be compared with an exact match — that needs model-based
grading, which is out of scope for now.

**Final (after 3 experiments):**

| Field | Score | Note |
|---|---|---|
| category | ~18/20 | |
| sentiment | ~18/20 | |
| priority | ~16–17/20 | noisiest field |

Reported with a range on purpose. Identical re-runs vary by ±1 on category and
sentiment and ±2 on priority. Quoting a single number would be misleading.

## Experiments

### Baseline (2026-10-01)
category 15/20 · sentiment 14/20 · priority 15/20
Model: `claude-haiku-4-5`

### Noise check — same prompt, re-run (2026-10-02)
category 15/20 · sentiment 14/20 · priority 17/20
→ priority varies ±2 between identical runs with no changes.
→ Any change below 2 points on priority is noise, not signal.

### Exp 1: explicit tie-breaker in system prompt (2026-10-02)
Changed: replaced "pick what the customer most needs resolved" with
"if a lost/stolen card is mentioned, category = lost_stolen_card".

category **18/20 (+3)** · sentiment 15/20 (noise) · priority 17/20 (0)

→ The 3 `lost_stolen_card` vs `account_locked` errors are gone. Real signal.
→ Lesson: the model was not wrong, it was missing a rule I had written in the
  README but never put in the prompt.

### Exp 2: define what sentiment measures (2026-10-02)
Changed: sentiment is now explicitly the customer's TONE, not the severity of
the situation. Added: "a customer reporting a stolen card calmly is neutral,
even though the situation itself is bad."

category 19/20 (+1, noise) · sentiment **17/20 (+3)** · priority 17/20 (0)

→ Before: all 5 sentiment errors were mine=neutral / model=negative.
  After: 3 errors, going in both directions. The systematic bias is gone; what
  is left are genuinely hard cases.
→ The model returned `positive` for the first time, on a message ending in
  "Thank you." By my own definition the model is right and my label is wrong.
  Found an error in my ground truth, not in the model.

### Exp 3: forbid card digits instead of giving a fillable example (2026-10-02)
Changed: "refer to a card as 'the card ending in XXXX'" → "do not include card
digits at all, refer to it simply as 'the card'".

category 18/20 · sentiment 18/20 · priority 16/20

→ All within noise, as expected: this rule does not affect the three measured
  fields. Fixed the data bug: summaries no longer leak digits or copy "XXXX"
  literally.
→ Second noise reading: category and sentiment also wobble ±1.

---

## Cost

Measured with `message.usage` on `claude-haiku-4-5` (2026-10-02).

| | input tokens | output tokens | cost |
|---|---|---|---|
| 1 message | 464 | ~53 | $0.00073 |
| 200 messages | 92,800 | ~10,600 | $0.15 |
| 100,000 messages | 46,400,000 | ~5,300,000 | **$73** |

Pricing used: $1 / MTok input, $5 / MTok output.

**Where the cost sits:**
- ~86% of input tokens are the system prompt, resent on every single call.
- Output is only 10% of the tokens but 37% of the cost, because output tokens
  cost 5x more. Almost all of it is the `summary` field.

**What $73 does not include:** my time, infrastructure, or the human who
reviews the ~10% of rows the classifier gets wrong.

## Optimizations identified, not implemented

| Lever | Why not now |
|---|---|
| Prompt caching | Haiku 4.5 requires a minimum of 4,096 cacheable tokens. The system prompt is ~400. Does not qualify. Would apply if the prompt grows (few-shot examples, injected documents). |
| Batch API | Correct fit — nobody is waiting on a classifier that runs over a CSV. Worth doing if volume justifies it. |
| Drop the `summary` field | Would cut ~1/3 of the cost for free, if the use case does not need it. |

At $73 per 100,000 these are not worth the engineering time yet. Documented so
the answer exists when a prospect asks "what if it's two million messages?".

---

## Open issues

- **`sentiment = positive` is effectively untested.** The 200 generated messages
  contain no genuinely positive ones — the generator ignored that instruction.
  Two of three sentiment values are actually being measured.
- **`priority` is almost a function of `category` in my own labels.** Every
  `lost_stolen_card` row I labeled `high`. If the two fields carry the same
  information, `priority` may not be earning its place.
- **`priority` is the noisiest field and the worst defined.** Those two facts
  are probably the same fact.
- **Pending decision: can the summary contain amounts?** Currently it does
  ("unauthorized charge of $47.99"). A single amount identifies nobody, but
  amount + merchant + date is transaction data and belongs under different
  access controls. Needs an explicit call before this touches real data.
- **Feature requests have no home in the taxonomy.** They currently land in
  `general_inquiry` by elimination. If they are frequent, they deserve their own
  category — in a real system they route to product, not support.