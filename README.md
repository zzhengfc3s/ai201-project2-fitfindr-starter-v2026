# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.
>
> Starter runs during breakout room.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

The user can query the agent with descriptions or keywords of outfit pieces they're interested in.
The agent will search the listings database and suggest 1-2 outfits based on the user's query and user's wardrobe.
From the suggested outfits, the agent will create a social media style post using one of the suggested outfit.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
Search the listings data for items matching the input's description, and optional size and a max price filter if available.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
'description' (string)
'size' (string) or (None)
'max_price' (float) or (None)
- **Returns:**
A list of matching listing dicts, best match first, each with 'title', 'description', 'category', 'style_tags', 'size', 'price', 'color', 'brand', 'platform'.
- **When it has nothing:**
Returns an empty list. not None, and not an exception.

### `suggest_outfit`

- **What it does:**
Suggest one or two outfits from the user's wardrobe with the new item.
- **Inputs:**
'new_item' (dictionary)
'wardrobe' (dictionary - with 'items' list) ('items' dict contains: id, name, category, colors, style_tags, notes)
- **Returns:**
A non-empty string with outfit suggestions.
- **When it has nothing:**
Returns an empty string. not None, and not an exception.

### `create_fit_card`

- **What it does:**
Write a short caption about the new outfit and the vibe that the user can post on social media.
- **Inputs:**
'outfit' (string)
'new_item' (dictionary)
- **Returns:**
A non-empty string of couple sentences that includes the item, price, and platform.
- **When it has nothing:**
If outfit is empty, returns a fail message instead of calling the model.
---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

If 'search_listing' returns an empty list, put the message 'STOP Session' in the session and stop. Otherwise take the first result and go to suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
Asking the model

**What moves through the session:** <!-- which fields, in what order -->
- description
- search_result
- wardrobe
- new_item
- outfit
- fit_card
---

## Stretch Feature: A second branch
Based on Milestone 3, criterion 2, my initial branching rule was wrong so I adjusted the tool spec from previous commit and adjusted the branching rules.

**Branch rule:**

If 'suggest_outfit' returns an empty string, put the message 'STOP Session' in the session and stop. Otherwise continue to 'create_fit_card'.

**Where it lives:** `agent.py::run_agent`
---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '90s track jacket in size M'

'
  Found:    90s Track Jacket — Navy/White Stripe — $45.0 on poshmark

  Outfit:   Here are two outfit combinations featuring the **90s Track Jacket — Navy/White Stripe** and pieces from your wardrobe:

### Outfit 1: The Ultimate 90s Streetwear Look
* **Top:** White ribbed tank top
* **Bottoms:** Baggy straight-leg jeans, dark wash
* **Shoes:** Chunky white sneakers
* **Accessories:** Black crossbody bag

**Why it works:** 
This look leans entirely into the vintage, athletic streetwear vibe of the track jacket. Layering the navy jacket zipped halfway over the fitted white tank creates a great contrast in proportions against the baggy, high-waisted dark wash jeans. 

**How to style it:**
Wear the track jacket slightly unzipped to show off the white tank underneath, which ties in with the white stripes on the sleeves and the chunky white sneakers. Let the jeans pool slightly over your sneakers for an authentic 90s slouch. Finish the look with the black crossbody bag worn across the chest for hands-free utility.

***

### Outfit 2: Sporty Meets Minimalist Prep
* **Bottoms:** Wide-leg khaki trousers
* **Accessories:** Brown leather belt
* **Shoes:** Chunky white sneakers
* *(Optional layering piece: White ribbed tank top tucked underneath)*

**Why it works:**
Mixing athletic pieces with tailored separates is a classic high-low styling trick. The navy track jacket brings a sporty edge, while the wide-leg khaki trousers and brown belt ground the outfit with a clean, minimal earth-tone base. 

**How to style it:**
Tuck a fitted top (like your white ribbed tank) into the khaki trousers, secure it with the brown leather belt, and wear the track jacket fully unzipped as an outer layer. Pair with the chunky white sneakers to keep the overall silhouette modern, relaxed, and effortlessly cool.

  Fit card: Scored this vintage 90s Track Jacket — Navy/White Stripe on Poshmark for just $45.0, and it instantly unlocked the ultimate sporty-meets-minimalist prep vibe! I paired it with wide-leg khakis and chunky sneakers for an effortless high-low mix that feels so fresh. Sustainable style has never looked this cool. ✨

3 model calls this session, 1095 prompt + 478 output tokens'
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

'[(2, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None,'platform': 'depop'}), (2, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}), (2, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}), (2, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}), (1, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}), (1, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition':'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'})]'
```

```
$ python -c 'from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))'

'Here are two outfit combinations using the **Vintage Levi's 501 Jeans — Medium Wash** and pieces from your wardrobe:

### Outfit 1: The Casual Streetwear Staple
* **Thrifted Item:** Vintage Levi's 501 Jeans — Medium Wash
* **Wardrobe Pieces:** 
  * White ribbed tank top
  * Oversized grey crewneck sweatshirt (layered)
  * Chunky white sneakers
  * Black crossbody bag
  * Brown leather belt

**Why it works & How to style it:**
This outfit balances fitted and oversized proportions for an effortless, everyday streetwear look. Start by tucking the **white ribbed tank top** into the **Vintage Levi's 501 Jeans** and cinching the waist with the **brown leather belt** to add a warm contrast to the blue denim. Throw the **oversized grey crewneck sweatshirt** over your shoulders or wear it on top for that cozy, relaxed vibe. Finish the fit with the **chunky white sneakers** to tie in the bright white of the tank, and sling the **black crossbody bag** across your chest to keep your essentials handy.

---

### Outfit 2: Edgy Vintage Contrast
* **Thrifted Item:** Vintage Levi's 501 Jeans — Medium Wash
* **Wardrobe Pieces:** 
  * Black cropped zip hoodie
  * Vintage black denim jacket
  * Black combat boots
  * Black crossbody bag

**Why it works & How to style it:**
The medium wash of the vintage 501s acts as a great contrast to an all-black upper half, making the denim pop while leaning into your grunge and vintage style tags. Layer the **black cropped zip hoodie** underneath the **vintage black denim jacket**—the contrast between the cropped zip-up and the slightly cropped jacket creates cool dimension. Pair the whole look with the **black combat boots** tucked slightly or resting over the hems of the jeans for a tough, grounded finish, and carry the **black crossbody bag** to keep the accessories sleek and minimal.'
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Nothing beats finding the holy grail of denim while scrolling on Depop late at night! These Vintage Levi's 501 Jeans in a medium wash were only $38.0, and they give off the ultimate effortless 90s off-duty vibe. I paired them with my go-to white sneakers for a look that's cool, comfy, and completely secondhand.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
Here are five acceptance criteria for a multi-tool agent. For each one, tell me exactly how you would test it using only what the sentence says. Don't suggest improvements — just tell me what you'd do.

- *What came back:*
Each test below uses only what the criterion states. Where the sentence leaves something undefined, I note the assumption I'd make.

1. Matching query completes all three tool calls and returns a fit card (4 of 5)

Pick one query that matches at least one listing.
Run the agent 5 times with that query.
For each run, check the tool-call log for all three calls (search_listing, suggest_outfit, create_fit_card) and check that a fit card is returned.
A run passes only if all three calls happened and a fit card came back.
The criterion passes if at least 4 of the 5 runs pass.

2. Non-matching query stops before suggest_outfit and names what to change (5 of 5)

Pick one query that matches no listings.
Run the agent 5 times with that query.
For each run, check two things: suggest_outfit was never called, and the returned message names something to change (for example, the price ceiling or a keyword).
A run passes only if both hold.
The criterion passes only if all 5 runs pass.

3. Selected item is passed to the next two tool calls (5 of 5)

Pick one query that matches at least one listing.
Run the agent 5 times.
For each run, record the item the agent selected from the search results, then inspect the inputs of suggest_outfit and create_fit_card in the tool-call log.
A run passes only if both calls received that same selected item.
The criterion passes only if all 5 runs pass.

4. Valid caption includes price and platform (5 of 5)

Run create_fit_card 5 times with a matching query's selected item, where the item has a known price and platform.
Keep only outputs that are valid, meaning the caption is a non-empty string and not a fail message. (Assumption: if a run produces an invalid caption, it doesn't count toward the 5, so I'd rerun until I have 5 valid captions.)
For each valid caption, check that the item's price and platform both appear in the text.
The criterion passes only if all 5 valid captions contain both.

5. Price-ceiling query returns only items at or under the max price (5 of 5)

Pick one query with a stated max price, ideally one where the listings include items above and below that price.
Run search_listing 5 times with that query.
For each run, check every returned item's price against the max price.
A run passes only if every item's price is less than or equal to the max.
The criterion passes only if all 5 runs pass.

- *What I changed:*
Nothing was changed, these testing steps looks like it can be automated mechanically.

**Moment 2**

- *What I asked for:*
No results found. Please try a different query.

Here is the message an app shows me when my search returns nothing. I know nothing about how the app works. Tell me what I would try next after reading it. If the honest answer is that I'd have no idea what to try, say that. Don't rewrite the message for me.

- *What came back:*
After reading it, you'd try a different search, but you'd be guessing. The message tells you what happened (nothing matched) and gives you one instruction ("try a different query"), but nothing about *what kind* of different.

Here's what you'd likely do, in order:

1. **Retype the same thing, maybe fixing a typo.** The first instinct is to suspect your own spelling.
2. **Try fewer or simpler words.** If you searched "blue running shoes size 10," you'd probably drop it to "running shoes."
3. **Try a synonym.** "Sneakers" instead of "running shoes."

Past that, you'd have no idea. The message doesn't say whether the app searches titles only or everything, whether it wants exact matches, whether filters are silently narrowing your results, or whether the thing you want just isn't there. So you can't tell whether to change your wording, loosen a setting, or give up. And "No results found" doesn't distinguish between "your search was wrong" and "this content doesn't exist," so you may keep trying variations long after there's anything to find.

So the honest answer: you'd have a vague sense to try simpler or different words, but no real direction. "Try a different query" is the app telling you to guess again.

- *What I changed:*

I implemented a nested if statement to output/save different messages to session depending which filter is too strict. The old implmentation just checked if the search_results were empty and output a generic try different query message.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
