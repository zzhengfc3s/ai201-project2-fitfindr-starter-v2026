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

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '90s track jacket in size M'

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

3 model calls this session, 1095 prompt + 478 output tokens
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[(2, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None,'platform': 'depop'}), (2, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}), (2, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}), (2, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}), (1, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}), (1, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition':'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'})]
```

```
$ python -c 'from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))'

Here are two outfit combinations using the **Vintage Levi's 501 Jeans — Medium Wash** and pieces from your wardrobe:

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
The medium wash of the vintage 501s acts as a great contrast to an all-black upper half, making the denim pop while leaning into your grunge and vintage style tags. Layer the **black cropped zip hoodie** underneath the **vintage black denim jacket**—the contrast between the cropped zip-up and the slightly cropped jacket creates cool dimension. Pair the whole look with the **black combat boots** tucked slightly or resting over the hems of the jeans for a tough, grounded finish, and carry the **black crossbody bag** to keep the accessories sleek and minimal.
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
```
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
```

- *What I changed:*
Nothing was changed, these testing steps looks like it can be automated mechanically.

**Moment 2**

- *What I asked for:*
No results found. Please try a different query.

Here is the message an app shows me when my search returns nothing. I know nothing about how the app works. Tell me what I would try next after reading it. If the honest answer is that I'd have no idea what to try, say that. Don't rewrite the message for me.

- *What came back:*
```
After reading it, you'd try a different search, but you'd be guessing. The message tells you what happened (nothing matched) and gives you one instruction ("try a different query"), but nothing about *what kind* of different.

Here's what you'd likely do, in order:

1. **Retype the same thing, maybe fixing a typo.** The first instinct is to suspect your own spelling.
2. **Try fewer or simpler words.** If you searched "blue running shoes size 10," you'd probably drop it to "running shoes."
3. **Try a synonym.** "Sneakers" instead of "running shoes."

Past that, you'd have no idea. The message doesn't say whether the app searches titles only or everything, whether it wants exact matches, whether filters are silently narrowing your results, or whether the thing you want just isn't there. So you can't tell whether to change your wording, loosen a setting, or give up. And "No results found" doesn't distinguish between "your search was wrong" and "this content doesn't exist," so you may keep trying variations long after there's anything to find.

So the honest answer: you'd have a vague sense to try simpler or different words, but no real direction. "Try a different query" is the app telling you to guess again.
```

- *What I changed:*

I implemented a nested if statement to output/save different messages to session depending which filter is too strict. The old implmentation just checked if the search_results were empty and output a generic try different query message.

**Unit 4 Moment 1**

- *What I asked for:*
* No results found. Try adjusting your query keywords.
* No results found. Try adjusting your query keywords.
* ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.

Here are three error messages from an app I'm using. For each one, tell me what I would try next as a user who can't see the code. If a message leaves me with nothing to try, say so. Don't rewrite them for me.

- *What came back:*
```
**1. "No results found. Try adjusting your query keywords."**
You have something to try. Use fewer or more general words, check spelling, swap in synonyms, and remove any filters or date ranges you may have set. If the search is scoped to a folder, project, or category, widen it. The message is vague about *why* nothing matched, but it at least points you at the one thing you control, which is the query.

**2. "No results found. Try adjusting your query keywords."** (same message again)
Same steps apply, but the repeat tells you something. If you've already loosened the query and still get this, the problem is probably not your wording. Either the thing you want isn't in the data, or the search itself isn't working and is reporting "nothing" instead of "error." A good test is to search for something you know exists. If that also returns nothing, stop rewording and treat it as a broken search. Beyond that, your only move is to contact support or the developer, since the message gives you no way to tell "no match" apart from "search failed."

**3. "ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com."**
This one is written for the developer, not for you. Unless you're the person who runs the app, you can't see a `.env` file and can't fix the key. What you can do is report it: tell whoever maintains the app that the Gemini API key is being rejected. If you *are* the person who set the app up, the message is actually quite actionable: check the key in `.env` and generate a new one if needed. If you aren't, you have nothing to try beyond waiting and reporting it, and retrying won't help because a rejected key will keep failing.

One connection worth noting: the third error could be the cause of the first two. If the app uses that model to run searches and the key is bad, it might show "no results" instead of surfacing the real error. That's a guess, but it's a reason to report all three together.
```

- *What I changed:*

Added a try - exception block around my code. Now the error says "Model Service Unavailable. Please try again later."

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
| 1. matching query completes | 4/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 2. impossible query stops early | 5/5 |  PASS | PASS  |  PASS | PASS  | PASS  | MET |
| 3. selected item is in fit card | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 4. fit card includes price and platform | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |
| 5. price filter | 5/5 | PASS | PASS | PASS | PASS | PASS | MET |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

Criterion 1:
```
**Try 5**

- stopped early: no
- selected_item: Y2K Baby Tee — Butterfly Print ($18.0, depop)
- search_results: 10

Outfit suggestion:

```
Here are two outfit combinations featuring the **Y2K Baby Tee — Butterfly Print** paired with items from your existing wardrobe:

### Outfit 1: The Y2K Streetwear Contrast
* **Thrifted Item:** Y2K Baby Tee — Butterfly Print
* **Wardrobe Pieces:** 
  * Baggy straight-leg jeans, dark wash
  * Chunky white sneakers
  * Black crossbody bag

**Why it works & how to style it:**
This outfit plays on the classic early-2000s silhouette by pairing a tightly fitted, cropped baby tee with voluminous, low-to-mid silhouette bottoms (since the jeans are high-waisted, they will sit nicely right at the hem of the baby tee, highlighting the waist). The white in the graphic and the pink/purple butterfly tones pop against the dark indigo wash of the denim. Tie the look together with the chunky white sneakers to lean into that retro streetwear aesthetic, and sling the black crossbody bag over your shoulder for an effortless, everyday look.

---

### Outfit 2: Edgy Casual (90s/Y2K Fusion)
* **Thrifted Item:** Y2K Baby Tee — Butterfly Print
* **Wardrobe Pieces:** 
  * Vintage black denim jacket
  * Wide-leg khaki trousers
  * Black combat boots

**Why it works & how to style it:**
If you want to tone down the sweetness of the butterfly graphic and the pink/purple pastels, pairing the tee with rugged black pieces creates a great balance of feminine and edgy styles. The cropped baby tee looks great tucked into or sitting just above the waistband of the wide-leg khaki trousers, creating an intentional contrast between the fitted top and relaxed, earthy bottoms. Layer the slightly cropped vintage black denim jacket on top, and finish the outfit with black combat boots to ground the look with a touch of grunge.
```

Fit card:

```
Channeling major Y2K streetwear energy with this cute butterfly baby tee I scored on Depop for just $18! Pairing it with baggy dark-wash jeans and chunky kicks gives that effortless, nostalgic contrast I live for. Honestly, thrift finds like this just hit different. ✨🦋
```

Trace:

```
[1] parsed_query
      in:  vintage graphic tee under $30
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] mcp_search_listings
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[3] branch_no_results
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 30.0}
[4] outfit_suggestion
      in:  {'selected_item': "{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute ear…
      out: Here are two outfit combinations featuring the **Y2K Baby Tee — Butterfly Print** paired with items from your …
[5] session_fit_card
      in:  {'outfit_suggestion': 'Here are two outfit combinations featuring the **Y2K Baby Tee — Butterfly Print** paire…
      out: Channeling major Y2K streetwear energy with this cute butterfly baby tee I scored on Depop for just $18! Pairi…
```
```

Criterion 2:
```
**Try 5**

- stopped early: yes — No results found. Try adjusting your query keywords.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] parsed_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] mcp_search_listings
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
```
```

Criterion 3:
```
**Try 5**

- stopped early: no
- selected_item: 90s Leather Bomber — Black ($75.0, depop)
- search_results: 4

Outfit suggestion:

```
Here are two distinct outfit suggestions for styling your 90s leather bomber jacket, leaning into its vintage, slightly grunge aesthetic:

### Look 1: Model-Off-Duty Minimalist (90s Casual)
*This look plays on proportions by pairing the boxy, oversized nature of the bomber with slimmer silhouettes underneath, creating an effortless, everyday vibe.*

*   **Top:** A fitted, white ribbed crewneck baby tee or a simple black-and-white striped long-sleeve top.
*   **Bottoms:** Mid-to-high-rise straight-leg medium-wash jeans with a slightly relaxed fit. 
*   **Footwear:** Classic black leather loafers or retro sneakers (like Adidas Sambas or Onitsuka Tigers).
*   **Accessories:** A minimalist black shoulder bag, thin silver hoop earrings, and oval sunglasses.

### Look 2: Grungy Contrast (Edgy & Feminine)
*This look contrasts the tough, rugged character of the genuine leather with softer, more delicate textures for a balanced, high-fashion grunge feel.*

*   **Base:** A slip dress in a midi length (either in black, emerald green, or a subtle floral print) to play up that authentic 90s contrast. 
*   **Footwear:** Chunky black combat boots (like Doc Martens) to anchor the outfit and tie in the edgy vibe of the jacket.
*   **Accessories:** Layered silver chain necklaces, a distressed crossbody bag, and maybe sheer black tights if the weather is cool.
```

Fit card:

```
Channeling total model-off-duty energy with this thrifted 90s Leather Bomber in black, scored for just $75.0 on Depop! Pairing its oversized, vintage grunge vibe with a simple baby tee and straight-leg denim keeps the look effortlessly cool. Run, don't walk, to my shop to grab this piece before it’s gone!
```

Trace:

```
[1] parsed_query
      in:  bomber jacket
      out: {'description': 'bomber jacket', 'size': None, 'max_price': None}
[2] mcp_search_listings
      in:  {'description': 'bomber jacket', 'size': None, 'max_price': None}
      out: 4 items: 90s Leather Bomber — Black, 90s Track Jacket — Navy/White Stripe, Denim Jacket — Light Wash, Cropped … +1 more
[3] branch_no_results
      in:  {'description': 'bomber jacket', 'size': None, 'max_price': None}
[4] outfit_suggestion
      in:  {'selected_item': "{'id': 'lst_022', 'title': '90s Leather Bomber — Black', 'description': 'Genuine leather bo…
      out: Here are two distinct outfit suggestions for styling your 90s leather bomber jacket, leaning into its vintage,…
[5] session_fit_card
      in:  {'outfit_suggestion': 'Here are two distinct outfit suggestions for styling your 90s leather bomber jacket, le…
      out: Channeling total model-off-duty energy with this thrifted 90s Leather Bomber in black, scored for just $75.0 o…
```
```

Criterion 4:
```
**Try 5**

- stopped early: no
- selected_item: Platform Sneakers — White Chunky Sole ($48.0, poshmark)
- search_results: 3

Outfit suggestion:

```
Here are two distinct outfit suggestions that lean into the late 90s / early 2000s energy of these platform sneakers, while embracing the natural yellowing of the sole as part of that authentic vintage charm:

### Look 1: The Off-Duty Pop Star (Y2K Streetwear)
*Channel the late-90s music video aesthetic—think sporty, comfortable, but high-impact.*

* **Bottoms:** Low-rise baggy cargo pants in olive green, khaki, or camouflage. 
* **Top:** A fitted, ribbed baby tee in white or black with a retro graphic (or a pastel color like baby blue or light pink). 
* **Outerwear:** An oversized nylon windbreaker or a cropped zip-up hoodie left slightly unzipped.
* **Accessories:** A small nylon shoulder bag (baguette style), tinted frameless sunglasses, and a chunky claw clip holding a messy updo.

### Look 2: Sporty Retro Casual (Skater / Campus Vibe)
*A more everyday, wearable look that highlights the chunky silhouette of the sneakers.*

* **Bottoms:** Distressed light-wash denim jorts (denim shorts ending just at the knee) or a pleated white tennis skirt with athletic socks pulled up to mid-calf.
* **Top:** An oversized vintage band tee or a color-blocked jersey styled with a relaxed fit.
* **Layering:** If it’s chilly, add an oversized denim jacket or a varsity jacket.
* **Accessories:** A canvas tote bag, a baseball cap, and some simple silver hoop earrings. 

**Styling Tip for the Yellowed Soles:** Lean into the vintage look! Pair these with distressed fabrics, vintage washes, and retro logos rather than pristine, ultra-modern minimalist pieces so the yellowing looks intentional and lived-in.
```

Fit card:

```
Stepping straight out of a 2000s music video in my dream off-duty pop star era! I scored these white chunky sole platform sneakers on Poshmark for just $48.0, and that naturally yellowed vintage look makes them feel so authentic. Paired with low-rise cargo pants and a baby tee, this Y2K streetwear fit is the ultimate throwback.
```

Trace:

```
[1] parsed_query
      in:  platform sneakers
      out: {'description': 'platform sneakers', 'size': None, 'max_price': None}
[2] mcp_search_listings
      in:  {'description': 'platform sneakers', 'size': None, 'max_price': None}
      out: 3 items: Platform Sneakers — White Chunky Sole, Platform Mary Janes — Black Patent, Low-Top Canvas Sneakers — Off-White
[3] branch_no_results
      in:  {'description': 'platform sneakers', 'size': None, 'max_price': None}
[4] outfit_suggestion
      in:  {'selected_item': "{'id': 'lst_019', 'title': 'Platform Sneakers — White Chunky Sole', 'description': 'White c…
      out: Here are two distinct outfit suggestions that lean into the late 90s / early 2000s energy of these platform sn…
[5] session_fit_card
      in:  {'outfit_suggestion': 'Here are two distinct outfit suggestions that lean into the late 90s / early 2000s ener…
      out: Stepping straight out of a 2000s music video in my dream off-duty pop star era! I scored these white chunky so…
```
```

Criterion 5:
```
**Try 5**

- stopped early: no
- selected_item: High-Waisted Denim Shorts — Cutoff ($24.0, poshmark)
- search_results: 10

Outfit suggestion:

```
Here are two versatile styling suggestions for these classic DIY Levi’s 501 cutoff shorts, ranging from casual daytime to effortless evening wear:

### 1. The Casual 90s Vintage Look (Daytime / Errands)
*Emphasize the vintage, effortless vibe of the shorts with classic basics and comfortable accessories.*

*   **Top:** A tucked-in, slightly oversized plain white ribbed tank top or a vintage graphic t-shirt. 
*   **Footwear:** Classic canvas low-top sneakers (like Converse or Vans) or retro leather trainers.
*   **Layers:** An unbuttoned, lightweight oversized linen shirt worn open as a light layer.
*   **Accessories:** A brown leather belt, a canvas tote bag, and retro oval sunglasses.

### 2. Elevated Summer Chic (Sunset Drinks / Casual Dinner)
*Dress up the raw-hem denim by pairing it with structured pieces and feminine textures.*

*   **Top:** A sleek black or olive green bodysuit, or a cropped black linen blouse with puff sleeves.
*   **Footwear:** Strappy leather flat sandals or comfortable leather mules.
*   **Layers:** A lightweight gold chain necklace and simple hoop earrings to add a touch of polish.
*   **Accessories:** A woven straw or rattan crossbody bag and a hair claw clip for an easy updo.
```

Fit card:

```
Scored these high-waisted denim shorts—cutoff for just $24 on Poshmark, and they are officially my whole personality this season! I paired them with a sleek black bodysuit, strappy sandals, and a claw clip for the ultimate sunset drinks look. Raw hem denim has never felt so effortlessly chic. ✨
```

Trace:

```
[1] parsed_query
      in:  vintage denim under $30
      out: {'description': 'vintage denim', 'size': None, 'max_price': 30.0}
[2] mcp_search_listings
      in:  {'description': 'vintage denim', 'size': None, 'max_price': 30.0}
      out: 10 items: High-Waisted Denim Shorts — Cutoff, Straight Leg Black Jeans — Faded, Denim Vest — Medium Wash, Studded … +7 more
[3] branch_no_results
      in:  {'description': 'vintage denim', 'size': None, 'max_price': 30.0}
[4] outfit_suggestion
      in:  {'selected_item': '{\'id\': \'lst_016\', \'title\': \'High-Waisted Denim Shorts — Cutoff\', \'description\': "…
      out: Here are two versatile styling suggestions for these classic DIY Levi’s 501 cutoff shorts, ranging from casual…
[5] session_fit_card
      in:  {'outfit_suggestion': 'Here are two versatile styling suggestions for these classic DIY Levi’s 501 cutoff shor…
      out: Scored these high-waisted denim shorts—cutoff for just $24 on Poshmark, and they are officially my whole perso…
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
$ python app.py ask '90s track jacket in size M'

[1] parsed_query
      in:  90s track jacket in size M
      out: {'description': '90s track jacket', 'size': 'M', 'max_price': None}
[2] mcp_search_listings
      in:  {'description': '90s track jacket', 'size': 'M', 'max_price': None}
      out: 4 items: 90s Track Jacket — Navy/White Stripe, 90s Leather Bomber — Black, 90s Silk Slip Dress — Floral, Midi Length … +1 more
[3] branch_no_results
      in:  {'description': '90s track jacket', 'size': 'M', 'max_price': None}
[4] outfit_suggestion
      in:  {'selected_item': "{'id': 'lst_004', 'title': '90s Track Jacket — Navy/White Stripe', 'description': 'Authenti…
      out: Here are two outfit combinations featuring the **90s Track Jacket — Navy/White Stripe** and pieces from your w…
[5] session_fit_card
      in:  {'outfit_suggestion': 'Here are two outfit combinations featuring the **90s Track Jacket — Navy/White Stripe**…
      out: Scored this vintage 90s Track Jacket — Navy/White Stripe on Poshmark for just $45.0, and it instantly unlocked…

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

0 model calls this session, 3 served from cache
```

**Empty search**

```
$ python app.py ask '...' --trace
            
[1] parsed_query
      in:  ...
      out: {'description': '', 'size': None, 'max_price': None}
[2] mcp_search_listings
      in:  {'description': '', 'size': None, 'max_price': None}
      out: [] (empty)

  No results found. Try adjusting your query keywords.

0 model calls this session, 1 served from cache
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

Changed 3 search_listings call to MCP call tool("search_listings", ...),
No change to the behavior.

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
