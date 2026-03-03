# Question Template Generator Script

## Overview

This script auto-generates JSON template files for all topics listed in the `selection.json` files for both English (en) and Thai (th) languages.

## Template Structure

Each generated template follows this JSON structure:

```json
{
    "language": "en",
    "type": "friends",
    "topicLabel": "🌶️ Inside Jokes",
    "topicPath": "inside_jokes",
    "spiceLevel": 1,
    "questions": [
        "template 1?",
        "template 2?",
        "template 3?"
    ]
}
```

### Field Descriptions

- **language**: Language code ("en" or "th")
- **type**: Question category ("friends", "families", "lovers", "specials")
- **topicLabel**: Display label from selection.json (includes emoji)
- **topicPath**: The file path identifier from selection.json
- **spiceLevel**: Extracted spice level (1, 2, 3, or null)
  - `1` = 🌶️ (basic/light topics)
  - `2` = 🌶️🌶️ (moderate depth)
  - `3` = 🌶️🌶️🌶️ (deep/personal topics)
  - `null` = Special topics without emoji
- **questions**: Array with placeholder question templates (ready to be filled in)

## File Organization

Templates are created at:
```
{language}/questions/{type}/{topicPath}.json
```

### Generated Summary

The script has successfully created **597 template files**:

- **English (en)**: 298 templates
  - Level 1 (🌶️): ~99 files
  - Level 2 (🌶️🌶️): ~99 files
  - Level 3 (🌶️🌶️🌶️): ~99 files
  - Special: 1 file

- **Thai (th)**: 299 templates
  - Level 1 (🌶️): ~99 files
  - Level 2 (🌶️🌶️): ~99 files
  - Level 3 (🌶️🌶️🌶️): ~99 files
  - Special: 1 file

**Distribution by spice level**:
- Level 1 (Light topics): 198 files
- Level 2 (Moderate depth): 198 files
- Level 3 (Deep/Personal): 195 files
- Special (No emoji): 2 files

## Usage

### Verify Missing Templates

List all missing template files:

```bash
python3 scripts/generate_question_templates.py verify
```

**Output**: Shows grouped list of missing files by language and type

**Example**:
```
📋 Found 0 missing template files:
✓ All templates exist! No missing files.
```

### Create Templates

Create all missing templates without overwriting existing ones:

```bash
python3 scripts/generate_question_templates.py create
```

**Output**: Shows count of created and skipped files

**Example**:
```
✓ Created 593 template files
⊘ Skipped 4 existing files (not overwritten)
```

## Key Features

✅ **Non-destructive**: Only creates templates for missing paths; never overwrites existing files

✅ **Bidirectional**: Works with both EN and TH selection files automatically

✅ **Spice Level Extraction**: Automatically extracts conversation depth level (1-3) from emoji

✅ **Well-structured**: Creates necessary directories automatically

✅ **Safe to rerun**: Running create multiple times is safe—existing files are preserved

✅ **Comprehensive**: Generates templates for all topics including the three spice levels (🌶️, 🌶️🌶️, 🌶️🌶️🌶️)

## Spice Level System

Spice levels represent conversation depth and intimacy:

| Level | Emoji | Questions Type | Examples |
|-------|-------|---|---|
| 1 | 🌶️ | Light, casual, fun | "Inside Jokes", "Favorite Foods", "Funny Relatives" |
| 2 | 🌶️🌶️ | Moderate depth, meaningful | "Turning Points", "Values Tested", "Family Pride" |
| 3 | 🌶️🌶️🌶️ | Deep, vulnerable, personal | "Hidden Struggles", "Love Fears", "Life Meaning" |
| null | (none) | Special categories | "Situationship" |

The script automatically extracts these levels from the emoji in the topic labels and stores them in the `spiceLevel` field for easy filtering and categorization.

## Data Sources

The script reads from:
- `en/selection.json` - English topics and labels
- `th/selection.json` - Thai topics and labels

## Next Steps

After templates are generated, you can:

1. Edit each template's `questions` array to add actual questions
2. Run the generate script again to verify all required templates exist
3. Process templates through your question generation pipeline

## Requirements

- Python 3.6+
- Access to `selection.json` files
- Write permissions to `questions/` directories
