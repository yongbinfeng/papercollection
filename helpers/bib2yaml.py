import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from collections import defaultdict

# --- Configuration ---
BIB_FILE = 'papers.bib'


def process_bib_to_console():
    try:
        with open(BIB_FILE, 'r', encoding='utf-8') as bibtex_file:
            # Set up the parser to automatically convert LaTeX characters to Unicode
            parser = BibTexParser()
            parser.customization = convert_to_unicode
            bib_database = bibtexparser.load(bibtex_file, parser=parser)
    except FileNotFoundError:
        print(
            f"Error: Could not find '{BIB_FILE}'. Please ensure the file exists in the same folder.")
        return

    categories = defaultdict(list)

    for entry in bib_database.entries:
        raw_category = entry.get(
            'category', entry.get('keywords', 'General Physics'))
        category_name = raw_category.split(',')[0].strip()

        title = entry.get('title', 'Untitled').replace(
            '{', '').replace('}', '').replace('"', "'")
        year = entry.get('year', '')

        collaboration = entry.get('collaboration', '').replace(
            '{', '').replace('}', '').replace('"', "'").strip()
        raw_authors = entry.get('author', '').replace('{', '').replace(
            '}', '').replace('"', "'").replace('\n', ' ').strip()

        # Extract comprehensive publication / journal information
        journal_name = entry.get('journal', '').replace(
            '{', '').replace('}', '').replace('"', "'").strip()
        booktitle = entry.get('booktitle', '').replace(
            '{', '').replace('}', '').replace('"', "'").strip()
        volume = entry.get('volume', '').strip()

        pages = entry.get('pages', '').replace('--', '-').strip()
        if not pages:
            # Use electronic identifier (eid) or issue number if pages are missing
            pages = entry.get('eid', entry.get('number', '')).strip()

        eprint = entry.get('eprint', '').strip()
        archive_prefix = entry.get('archiveprefix', 'arXiv').strip()
        primary_class = entry.get('primaryclass', '').strip()

        # Format as JHEP style: <i>Journal</i> <b>Volume</b> (Year) Pages
        pub_str = ""
        if journal_name:
            pub_str += f"<i>{journal_name}</i>"
            if volume:
                pub_str += f" <b>{volume}</b>"
            if year:
                pub_str += f" ({year})"
            if pages:
                pub_str += f" {pages}"
        elif booktitle:
            pub_str += f"<i>{booktitle}</i>"
            if year:
                pub_str += f" ({year})"
            if pages:
                pub_str += f" {pages}"
        elif eprint:
            pub_str += f"{archive_prefix}:{eprint}"
            if primary_class:
                pub_str += f" [{primary_class}]"

        if collaboration:
            if "collaboration" not in collaboration.lower():
                final_author = f"{collaboration} Collaboration"
            else:
                final_author = collaboration
        else:
            # Format author list to have First Name first, Last Name second
            author_list = raw_authors.split(' and ')
            formatted_list = []
            for a in author_list:
                a = a.strip()
                if a.lower() == 'others':
                    formatted_list.append('et al.')
                elif ',' in a:
                    # "Last, First" format -> convert to "First Last"
                    parts = a.split(',', 1)
                    if len(parts) == 2:
                        first_name = parts[1].strip()
                        last_name = parts[0].strip()
                        formatted_list.append(f"{first_name} {last_name}")
                    else:
                        formatted_list.append(a)
                else:
                    # Assume "First Last" format already
                    formatted_list.append(a)

            # Rejoin the formatted authors
            if formatted_list and formatted_list[-1] == 'et al.':
                final_author = ', '.join(formatted_list[:-1]) + ' et al.'
            else:
                final_author = ', '.join(formatted_list)

            final_author = final_author.replace('\\', '\\\\')

        if 'eprint' in entry:
            url = f"https://arxiv.org/abs/{entry['eprint']}"
        elif 'doi' in entry:
            url = f"https://doi.org/{entry['doi']}"
        else:
            url = entry.get('url', '#')

        notes = entry.get('note', entry.get('annote', ''))
        if notes:
            notes = notes.replace('"', "'").strip()

        paper_data = {
            'title': title,
            'year': int(year) if year.isdigit() else year,
            'url': url
        }

        if final_author:
            paper_data['authors'] = final_author

        if pub_str:
            paper_data['journal'] = pub_str

        if notes:
            paper_data['notes'] = notes

        categories[category_name].append(paper_data)

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
            if 'journal' in paper:
                print(f"  journal: '{paper['journal']}'")
            print(f'  url: "{paper["url"]}"')

            # --- BULLETPROOF NOTES OUTPUT ---
            # Using the pipe (|) makes YAML ignore all backslashes and quotes
            if 'notes' in paper:
                print(f'  notes: |')
                for line in paper["notes"].split('\n'):
                    print(f'    {line.strip()}')
            print()


if __name__ == '__main__':
    process_bib_to_console()
