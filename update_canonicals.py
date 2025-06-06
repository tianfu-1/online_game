import os
import glob
import re

def update_canonical_tags(base_url, directory):
    """
    Updates or adds the canonical link tag in HTML files within a given directory.
    If a canonical tag exists, it's updated. If not, a new one is added inside the <head>.
    """
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    html_files = glob.glob(os.path.join(directory, '*.html'))
    if not html_files:
        print(f"No HTML files found in '{directory}'.")
        return

    print(f"Found {len(html_files)} HTML files to process...")

    canonical_regex = re.compile(r'<link\s+rel="canonical"\s+href="[^"]*"\s*/>', re.IGNORECASE)
    head_tag_regex = re.compile(r'<head>', re.IGNORECASE)

    for file_path in html_files:
        relative_path = os.path.join(directory, os.path.basename(file_path)).replace('\\\\', '/')
        correct_url = f"{base_url}/{relative_path}"
        new_canonical_tag = f'<link rel="canonical" href="{correct_url}" />'

        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            # Move cursor back to the beginning to overwrite the file
            f.seek(0)
            
            new_content, num_replacements = canonical_regex.subn(new_canonical_tag, content)

            if num_replacements > 0:
                f.write(new_content)
                f.truncate()
                print(f"Updated canonical URL in: {file_path}")
            else:
                # If no canonical tag was found, add it after the <head> tag
                if head_tag_regex.search(content):
                    # Add the canonical tag right after the opening <head> tag
                    new_content_with_added_tag = head_tag_regex.sub(f'<head>\\n    {new_canonical_tag}', content, count=1)
                    f.write(new_content_with_added_tag)
                    f.truncate()
                    print(f"Added canonical URL to:   {file_path}")
                else:
                    print(f"Warning: No <head> tag found in {file_path}. Cannot add canonical tag.")


def main():
    website_base_url = 'https://www.expertsaireview.com'
    games_directory = 'onlinegames/games'
    
    print("Starting canonical URL update process...")
    update_canonical_tags(website_base_url, games_directory)
    print("...Process finished.")

if __name__ == '__main__':
    main() 