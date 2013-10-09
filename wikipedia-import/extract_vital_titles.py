#!/usr/bin/env python3

import argparse
import urllib.parse

import bs4
import sys

def walk_the_soup(soup, outfile):
    """Go through the page looking for links and section headings. Remember the
    section headings and use them as tags!"""
    for node in soup.find_all(['a', 'h2', 'h3']):
        if node.name == 'h2':
            h2 = None
            h3 = None
            children = node.findChildren('span')
            if children: 
                h2 = children[0].text
        if node.name == 'h3':
            children = node.findChildren('span')
            if children: 
                h3 = children[0].text
        elif node.name == 'a':
            target = node.get('href')
            if target and target.startswith("/wiki/") and ":" not in target:
                title = urllib.parse.unquote(target)[6:]
                title = title.replace("_", " ")
                tags = [h2]
                if h3:
                    tags.append(h3)
                print("|||".join([title] + tags), file=outfile)

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
        soup = bs4.BeautifulSoup(html)
        walk_the_soup(soup, outfile)

if __name__ == '__main__':
    main()
