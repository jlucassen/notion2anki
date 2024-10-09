# notion2anki

Now supports two formats!
- One-deep bullets are turned into cards
- Top level bullets are discarded if they have sub-bullets underneath and sub-bullets become bulleted notes

All notes must be clozes, with {{just brackets}}, cloze numbering is filled in automatically

The Notion page title is parsed as the deck title, and h3 headers are parsed as tags. All cards are tagged with "deck:tag" based on the most recent h3.

When importing into anki choose pipe field separators, cloze notes, the right deck, and set the tag field to be tags.