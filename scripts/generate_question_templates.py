#!/usr/bin/env python3
"""
Script to auto-generate JSON template files for questions.

Functionality:
- create: Creates all missing templates without overwriting existing ones
- verify: Lists all missing JSON question template files
- check: Lists all question files with less than specified question count (default: 5)

Template structure:
{
    "language": "en" or "th",
    "type": "friends" / "lovers" / "families" / "specials",
    "topicLabel": "label with emoji...",
    "topicPath": "path...",
    "spiceLevel": 1, 2, 3, or null,
    "questions": ["template 1?", "template 2?", "template 3?"]
}

Usage:
    python3 generate_question_templates.py create
    python3 generate_question_templates.py verify
    python3 generate_question_templates.py check [min_count]
        - min_count: minimum number of questions (default: 5)
"""

import json
import os
import sys
from pathlib import Path


def extract_spice_level(label):
    """Extract spice level (1-3) from the emoji in label."""
    if not label:
        return None
    
    # Count the number of 🌶️ emojis at the start of the label
    spice_count = 0
    for char in label:
        if char == "🌶":
            spice_count += 1
        elif char != "️":  # Skip the variation selector
            break
    
    return spice_count if spice_count > 0 else None


def load_selection_file(language):
    """Load the selection.json file for a given language."""
    selection_path = Path(__file__).parent.parent / "contents" / language / "selection.json"
    
    if not selection_path.exists():
        print(f"Error: {selection_path} not found")
        return None
    
    with open(selection_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_template(language, type_name, topic_label, topic_path, spice_level):
    """Generate a template JSON object for a question topic."""
    return {
        "language": language,
        "type": type_name,
        "topicLabel": topic_label,
        "topicPath": topic_path,
        "spiceLevel": spice_level,
        "questions": [
            "template 1?",
            "template 2?",
            "template 3?"
        ]
    }


def get_template_path(language, type_name, topic_path):
    """Get the expected file path for a template."""
    base_path = Path(__file__).parent.parent / "contents" / language / "questions" / type_name
    return base_path / f"{topic_path}.json"


def collect_all_topics():
    """Collect all topics from both language selection files."""
    topics = []
    
    for language in ["en", "th"]:
        selection = load_selection_file(language)
        if not selection:
            continue
        
        for type_group in selection.get("types", []):
            type_name = type_group.get("type", "")
            for topic in type_group.get("topics", []):
                topic_label = topic.get("label", "")
                topic_path = topic.get("path", "")
                spice_level = extract_spice_level(topic_label)
                
                topics.append({
                    "language": language,
                    "type": type_name,
                    "label": topic_label,
                    "path": topic_path,
                    "spice_level": spice_level
                })
    
    return topics


def verify_templates():
    """List all missing template files."""
    topics = collect_all_topics()
    missing = []
    
    for topic in topics:
        template_path = get_template_path(
            topic["language"],
            topic["type"],
            topic["path"]
        )
        
        if not template_path.exists():
            missing.append({
                "language": topic["language"],
                "type": topic["type"],
                "label": topic["label"],
                "path": template_path
            })
    
    return missing


def create_templates():
    """Create all missing template files."""
    topics = collect_all_topics()
    created = []
    skipped = []
    
    for topic in topics:
        template_path = get_template_path(
            topic["language"],
            topic["type"],
            topic["path"]
        )
        
        # Create directory if it doesn't exist
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file already exists
        if template_path.exists():
            skipped.append(str(template_path))
            continue
        
        # Generate and write template
        template = generate_template(
            topic["language"],
            topic["type"],
            topic["label"],
            topic["path"],
            topic["spice_level"]
        )
        
        with open(template_path, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=4, ensure_ascii=False)
            f.write("\n")  # Add newline at end of file
        
        created.append(str(template_path))
    
    return created, skipped


def check_incomplete_questions(min_count=5):
    """Check for question files with less than min_count questions."""
    incomplete = []
    base_path = Path(__file__).parent.parent / "contents"
    
    # Scan all question files
    for qfile in sorted(base_path.glob("*/questions/**/*.json")):
        try:
            with open(qfile, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Only check actual question files (not selection.json)
            if "questions" in data:
                question_count = len(data.get("questions", []))
                
                if question_count < min_count:
                    incomplete.append({
                        "file": str(qfile),
                        "language": data.get("language"),
                        "type": data.get("type"),
                        "label": data.get("topicLabel"),
                        "path": data.get("topicPath"),
                        "count": question_count
                    })
        except (json.JSONDecodeError, IOError):
            # Skip files that can't be read
            continue
    
    return incomplete


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python3 generate_question_templates.py [create|verify|check]")
        print()
        print("Commands:")
        print("  create          - Create all missing template files")
        print("  verify          - List all missing template files")
        print("  check [count]   - List files with less than [count] questions (default: 5)")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "verify":
        missing = verify_templates()
        
        if not missing:
            print("✓ All templates exist! No missing files.")
            return
        
        print(f"📋 Found {len(missing)} missing template files:\n")
        
        # Group by language
        by_language = {}
        for item in missing:
            lang = item["language"]
            if lang not in by_language:
                by_language[lang] = []
            by_language[lang].append(item)
        
        for language in sorted(by_language.keys()):
            items = by_language[language]
            print(f"\n{language.upper()} ({len(items)} missing):")
            print("-" * 80)
            
            # Group by type
            by_type = {}
            for item in items:
                type_name = item["type"]
                if type_name not in by_type:
                    by_type[type_name] = []
                by_type[type_name].append(item)
            
            for type_name in sorted(by_type.keys()):
                type_items = by_type[type_name]
                print(f"\n  {type_name} ({len(type_items)}):")
                for item in sorted(type_items, key=lambda x: x["path"]):
                    print(f"    • {item['path']}")
    
    elif command == "check":
        # Get minimum count from argument, default to 5
        min_count = 5
        if len(sys.argv) > 2:
            try:
                min_count = int(sys.argv[2])
            except ValueError:
                print(f"Error: '{sys.argv[2]}' is not a valid number")
                sys.exit(1)
        
        incomplete = check_incomplete_questions(min_count)
        
        if not incomplete:
            return
        
        # Get project root for relative path calculation
        project_root = Path(__file__).parent.parent
        
        # Print just the paths from project root
        for item in incomplete:
            file_path = Path(item["file"])
            relative_path = file_path.relative_to(project_root)
            print(str(relative_path))
    
    elif command == "create":
        created, skipped = create_templates()
        
        print(f"✓ Created {len(created)} template files")
        if skipped:
            print(f"⊘ Skipped {len(skipped)} existing files (not overwritten)")
        
        if created:
            print("\nCreated files:")
            for path in sorted(created):
                print(f"  ✓ {path}")
        
        if skipped:
            print("\nSkipped (already exist):")
            for path in sorted(skipped)[:10]:  # Show first 10
                print(f"  ⊘ {path}")
            if len(skipped) > 10:
                print(f"  ... and {len(skipped) - 10} more")
    
    else:
        print(f"Unknown command: {command}")
        print("Usage: python3 generate_question_templates.py [create|verify|check]")
        sys.exit(1)


if __name__ == "__main__":
    main()
