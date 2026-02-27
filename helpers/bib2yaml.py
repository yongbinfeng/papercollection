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
        raw_category = entry.get(
            'category', entry.get('keywords', 'General Physics'))
        category_name = raw_category.split(',')[0].strip()

        title = entry.get('title', 'Untitled').replace(
            '{', '').replace('}', '').replace('"', "'")
        year = entry.get('year', '')

        # --- SMART COLLABORATION / AUTHOR LOGIC ---
        collaboration = entry.get('collaboration', '').replace(
            '{', '').replace('}', '').replace('"', "'").strip()
        raw_authors = entry.get('author', '').replace('{', '').replace(
            '}', '').replace('"', "'").replace('\n', ' ').strip()

        if collaboration:
            # Use the collaboration field. Add the word "Collaboration" if it isn't already there.
            if "collaboration" not in collaboration.lower():
                final_author = f"{collaboration} Collaboration"
            else:
                final_author = collaboration
        else:
            # Fallback to standard authors, and clean up "and others" to "et al."
            final_author = raw_authors.replace(' and others', ' et al.')

        # SMART URL HANDLING
        if 'eprint' in entry:
            url = f"https://arxiv.org/abs/{entry['eprint']}"
        elif 'doi' in entry:
            url = f"https://doi.org/{entry['doi']}"
        else:
            url = entry.get('url', '#')

        # --- BULLET POINT HANDLING ---
        notes = entry.get('note', entry.get('annote', ''))
        if notes:
            # Remove quotes but keep the \n newlines intact so bullet points survive
            notes = notes.replace('"', "'").strip()

        paper_data = {
            'title': title,
            'year': int(year) if year.isdigit() else year,
            'url': url
        }

        if final_author:
            paper_data['authors'] = final_author

        if notes:
            paper_data['notes'] = notes

        categories[category_name].append(paper_data)

    # 3. Print the manually formatted output
    if not categories:
        print("No entries found in the .bib file.")
        return

    for cat_name, papers in categories.items():
        suggested_filename = f"{cat_name.replace(' ', '_').lower()}.yml"

        print(f"\n" + "="*50)
        print(f"CATEGORY: {cat_name}")
        print(f"SUGGESTED FILE: data/{suggested_filename}")
        print("="*50)

        for paper in papers:
            print(f'- title: "{paper["title"]}"')
            print(f'  year: {paper["year"]}')
            if 'authors' in paper:
                print(f'  authors: "{paper["authors"]}"')
            print(f'  url: "{paper["url"]}"')

            # --- OUTPUT NOTES WITH MULTI-LINE SUPPORT ---
            if 'notes' in paper:
                if '\n' in paper["notes"]:
                    print(f'  notes: |')
                    for line in paper["notes"].split('\n'):
                        print(f'    {line.strip()}')
                else:
                    print(f'  notes: "{paper["notes"]}"')
            print()


if __name__ == '__main__':
    process_bib_to_console()
