#!/usr/bin/env python3

import argparse
import urllib.parse

import bs4

def dump_links(html, outfile):
    soup = bs4.BeautifulSoup(html)
    for link in soup.find_all('a'):
        target = link.get('href')
        if target and target.startswith("/wiki/") and ":" not in target:
            title = urllib.parse.unquote(target)[6:]
            title = title.replace("_", " ")
            print(title, file=outfile)

def get_argparser():
    """Build the argument parser for main."""
    parser = argparse.ArgumentParser(description='WikiExtractor')
    parser.add_argument('--infn', type=str, required=True)
    parser.add_argument('--outfn', type=str, required=True)
    return parser

def main():
    parser = get_argparser()
    args = parser.parse_args()

    with open(args.infn) as infile, open(args.outfn, "w") as outfile:
        html = infile.read()
        dump_links(html, outfile)

if __name__ == '__main__':
    main()
