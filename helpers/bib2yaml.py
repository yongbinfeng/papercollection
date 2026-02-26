import bibtexparser
from collections import defaultdict

# --- Configuration ---
BIB_FILE = 'papers.bib'


def process_bib_to_console():
    # 1. Load the BibTeX file
    try:
        with open(BIB_FILE, 'r', encoding='utf-8') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
    except FileNotFoundError:
        print(
            f"Error: Could not find '{BIB_FILE}'. Please ensure the file exists in the same folder.")
        return

    # Dictionary to hold papers grouped by category
    categories = defaultdict(list)

    # 2. Process each entry
    for entry in bib_database.entries:
        # Determine category (defaults to 'general_physics' if missing)
        raw_category = entry.get(
            'category', entry.get('keywords', 'General Physics'))
        category_name = raw_category.split(',')[0].strip()

        # Clean up title: Remove BibTeX {} and swap inner double quotes to single quotes to prevent breaking the YAML
        title = entry.get('title', 'Untitled').replace(
            '{', '').replace('}', '').replace('"', "'")
        year = entry.get('year', '')

        # Smart URL handling
        url = entry.get('url', '')
        if not url:
            if 'doi' in entry:
                url = f"https://doi.org/{entry['doi']}"
            elif 'eprint' in entry:
                url = f"https://arxiv.org/abs/{entry['eprint']}"
            else:
                url = "#"  # Fallback empty link

        # Look for a notes field and clean up any newlines
        notes = entry.get('note', entry.get('annote', ''))
        if notes:
            notes = notes.replace('\n', ' ').replace('"', "'")

        # Build the paper dictionary
        paper_data = {
            'title': title,
            'year': int(year) if year.isdigit() else year,
            'url': url
        }

        if notes:
            paper_data['notes'] = notes

        # Add to the appropriate category list
        categories[category_name].append(paper_data)

    # 3. Print the manually formatted output to the console
    if not categories:
        print("No entries found in the .bib file.")
        return

    for cat_name, papers in categories.items():
        # Create a suggested filename based on the category
        suggested_filename = f"{cat_name.replace(' ', '_').lower()}.yml"

        print(f"\n" + "="*50)
        print(f"CATEGORY: {cat_name}")
        print(f"SUGGESTED FILE: data/{suggested_filename}")
        print("="*50)

        # Manually format the YAML to force quotation marks
        for paper in papers:
            print(f'- title: "{paper["title"]}"')
            print(f'  year: {paper["year"]}')
            print(f'  url: "{paper["url"]}"')
            if 'notes' in paper:
                print(f'  notes: "{paper["notes"]}"')
            print()  # Add a blank line between papers for readability


if __name__ == '__main__':
    process_bib_to_console()
