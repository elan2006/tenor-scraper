import requests
import pprint
import argparse
import sys
import os

def download(url, filename, directory):
    data = requests.get(url).content
    with open(f"{directory}/{filename}", 'wb') as f:
        f.write(data)

def main():
    parser = argparse.ArgumentParser(description="Downloads GIFs from Tenor")
    parser.add_argument("query", help="Search Tenor GIFs")
    parser.add_argument("--key", type = str, help="Tenor API Key")
    parser.add_argument("--limit", type = int, help="Limit for the number of GIFs to download")
    parser.add_argument("--directory",type=str, help="Directory to store the GIFs")
    args = parser.parse_args()
    query = args.query
    if args.directory is not None:
        directory = args.directory
    else:
        directory = "."

    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist. Exitting...", file=sys.stderr)
        sys.exit(1)

    if args.key is not None:
        api_key = args.key
    else:
        api_key = "LIVDSRZULELA"
        
    if args.limit is not None:
        limit = args.limit
    else:
        limit = 100
    api_string = f"https://g.tenor.com/v1/random?q={query}&key={api_key}&limit={limit}"
    r = requests.get(api_string)

    if r.status_code == 401:
        print("Response code 401. Check your API key.", file=sys.stderr)
        sys.exit(1)

    result = r.json()['results']
    n_gifs = len(result)
    for i in range(n_gifs):
        url = result[i]['media'][0]['gif']['url']
        split = url.split("/")    
        filename = split[len(split)-1]
        print(f"{i+1}: {url}")
        download(url,filename, directory)
        # pprint.pprint(result[i])

if __name__ == "__main__":
    main()
