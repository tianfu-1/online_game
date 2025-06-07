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

    print(f"Processing {len(html_files)} HTML files in '{directory}'...")

    canonical_regex = re.compile(r'<link\s+rel="canonical"\s+href="[^"]*"\s*/>', re.IGNORECASE)
    head_tag_regex = re.compile(r'(<head.*>)', re.IGNORECASE)

    for file_path in html_files:
        relative_path = file_path.replace('\\\\', '/')
        
        correct_url = f"{base_url}/{relative_path}"
        # For index.html files, the canonical should be the directory URL
        if os.path.basename(file_path) == 'index.html':
            dir_path = os.path.dirname(relative_path)
            if dir_path:
                correct_url = f"{base_url}/{dir_path}/"
            else:
                correct_url = f"{base_url}/"

        new_canonical_tag = f'<link rel="canonical" href="{correct_url}" />'

        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            f.seek(0)
            
            new_content, num_replacements = canonical_regex.subn(new_canonical_tag, content)

            if num_replacements > 0:
                f.write(new_content)
                f.truncate()
                print(f"  Updated canonical in: {file_path}")
            else:
                if head_tag_regex.search(content):
                    new_content_with_added_tag = head_tag_regex.sub(f'\\1\\n    {new_canonical_tag}', content, count=1)
                    f.write(new_content_with_added_tag)
                    f.truncate()
                    print(f"  Added canonical to:   {file_path}")
                else:
                    print(f"  Warning: No <head> tag found in {file_path}. Cannot add canonical tag.")


def generate_sitemap(base_url, all_html_files):
    """
    Generates a sitemap.xml file from the list of HTML files.
    """
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    urls = set()
    for file_path in all_html_files:
        url_path = file_path.replace('\\', '/')
        if os.path.basename(url_path) == 'index.html':
            # For index.html, use the directory path, e.g., .../onlinegames/
            dir_path = os.path.dirname(url_path)
            if dir_path:
                urls.add(f"{base_url}/{dir_path}/")
            else: # Root index.html
                urls.add(f"{base_url}/")
        else:
            urls.add(f"{base_url}/{url_path}")
    
    # Ensure the base url is in the sitemap
    urls.add(f"{base_url}/")

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n'
    for url in sorted(list(urls)):
        sitemap_content += f'  <url>\\n    <loc>{url}</loc>\\n  </url>\\n'
    sitemap_content += '</urlset>'

    sitemap_path = 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f"\nGenerated sitemap.xml with {len(urls)} URLs.")


def main():
    website_base_url = 'https://www.expertsaireview.com'
    directories_to_process = ['onlinegames', 'onlinegames/games']
    
    print("Starting canonical URL update process...")
    all_html_files = []
    for directory in directories_to_process:
        update_canonical_tags(website_base_url, directory)
        all_html_files.extend(glob.glob(os.path.join(directory, '*.html')))
    
    generate_sitemap(website_base_url, all_html_files)
    
    print("\n...Process finished.")

if __name__ == '__main__':
    main() 