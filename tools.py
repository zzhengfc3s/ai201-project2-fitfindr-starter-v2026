"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re
import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    loaded_listings = load_listings()

    if max_price is not None:
        loaded_listings = [listing for listing in loaded_listings if listing.get("price") <= max_price]

    if size is not None:
        pattern = re.compile(rf"\b{re.escape(size)}\b", re.IGNORECASE)
        loaded_listings = [listing for listing in loaded_listings if listing.get("size") and pattern.search(listing["size"])]

    description_keywords = set(re.findall(r'\w+', description.lower()))
    scored_listings = []

    for listing in loaded_listings:
        searchable_listings = [listing.get("title", ""),
                               listing.get("description", ""),
                               listing.get("category", ""),
                               listing.get("brand", "") or "",
                               " ".join(listing.get("style_tags", [])),
                               " ".join(listing.get("colors", [])),
                               ]
        listing_keywords = set(re.findall(r'\w+', " ".join(searchable_listings).lower()))

        score = len(description_keywords.intersection(listing_keywords))
        if score > 0:
            scored_listings.append((score, listing))

    scored_listings.sort(key=lambda x: x[0], reverse=True)

    return [listing for score, listing in scored_listings[:config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """

    wardrobe_items = wardrobe.get("items", [])

    new_item_description = (
        f"Short Description: {new_item.get('title', '')}\n"
        f"Long Description: {new_item.get('description', '')}\n"
        f"Category: {new_item.get('category', '')}\n"
        f"Colors: {', '.join(new_item.get('colors', []))}\n"
        f"Style Tags: {', '.join(new_item.get('style_tags', []))}"
        )

    if not wardrobe_items:
        prompt = (
            f"Suggest general styling ideas for this thrifted item:\n"
            f"{new_item_description}\n"
            f"Provide one or two outfit suggestions that would pair well with this item."
            )
    else:
        wardrobe_descriptions = []
        for item in wardrobe_items:
            item_description = (
                f"Short Description: {item.get('name', '')}\n"
                f"Category: {item.get('category', '')}\n"
                f"Colors: {', '.join(item.get('colors', []))}\n"
                f"Style Tags: {', '.join(item.get('style_tags', []))}\n"
                f"Notes (fits, style, etc.): {item.get('notes', '')}"
            )
            wardrobe_descriptions.append(item_description)

        wardrobe_summary = "\n".join(wardrobe_descriptions)

        prompt = (
            f"Given the following thrifted item:\n"
            f"{new_item_description}\n"
            f"And the user's wardrobe:\n"
            f"{wardrobe_summary}\n\n"
            f"Provide one or two outfit specific combinations that include the thrifted item and pieces from the wardrobe.\n"
            f"Name the thrifted item (short description) and the specific wardrobe pieces (short descriptions) in each outfit suggestion.\n"
            f"Be specific about why it works and how to style the outfit."
        )

    return generate(prompt)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "Error - No Fit Card Generated: Outfit suggestion is empty or whitespace."

    prompt = (
        f"Write a short and engaging caption for a social media post about a thrifted outfit.\n"
        f"Outfit Suggestion(s): {outfit}\n\n"
        f"Caption Rules:\n"
        f"- Pick only 1 outfit suggestion from above to write about.\n"
        f"- Keep it strictly to 2-4 sentences.\n"
        f"- Must mention the thrifted item: {new_item.get('title', '')} and its price {new_item.get('price', '')} and platform {new_item.get('platform', '')} once each.\n"
        f"- Be specific about the vibe.\n"
        f"- Make it sound like a real social media post, not a product description.\n"
        )
    
    return generate(prompt)