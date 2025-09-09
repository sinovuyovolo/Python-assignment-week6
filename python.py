import requests
import os
import hashlib
from urllib.parse import urlparse
from pathlib import Path

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename if filename else "downloaded_image.jpg"

def get_file_hash(content):
    return hashlib.md5(content).hexdigest()

def file_already_exists(content, folder):
    content_hash = get_file_hash(content)
    for existing_file in os.listdir(folder):
        existing_path = os.path.join(folder, existing_file)
        with open(existing_path, 'rb') as f:
            if get_file_hash(f.read()) == content_hash:
                return existing_file
    return None

def is_image_content(response):
    content_type = response.headers.get('Content-Type', '')
    return content_type.startswith('image/')

def fetch_image(url, folder="Fetched_Images"):
    try:
        os.makedirs(folder, exist_ok=True)
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if not is_image_content(response):
            print(f"The URL does not point to an image: {url}")
            return

        filename = get_filename_from_url(url)
        filepath = os.path.join(folder, filename)

        # Prevent duplicates
        duplicate = file_already_exists(response.content, folder)
        if duplicate:
            print(f"Duplicate image detected. Already saved as: {duplicate}")
            return

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"Successfully fetched: {filename}")
        print(f"Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"Connection error for URL {url}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    urls_input = input("Please enter image URL(s) (comma-separated if multiple): ").strip()
    urls = [u.strip() for u in urls_input.split(',') if u.strip()]

    if not urls:
        print("No URLs entered. Exiting.")
        return

    for url in urls:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
