#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: transform.py
# Author: Yuxin Wu


import sys
import os
import bs4
import magic

fname = sys.argv[1]
if not fname.endswith('.html'):
    if fname.endswith('.css'):
        f = open(fname, 'rb')
        css = f.read().decode('utf-8')
        css = css.replace('Roboto', 'Roboto, SF Mono, Monaco')
        with open(fname, 'wb') as f:
            f.write(css.encode('utf-8')) 
            sys.exit(0)
    elif fname.endswith('.json'):
        f = open(fname, 'rb')
        css = f.read().decode('utf-8')
        css = css.replace('${version}', os.environ['TFJS_VERSION'])
        with open(fname, 'wb') as f:
            f.write(css.encode('utf-8')) 
            sys.exit(0)
    else:
        sys.exit(0)

if 'gzip compressed' in magic.from_file(fname):
    import gzip
    f = gzip.open(fname)
else:
    f = open(fname, 'rb')
html = f.read().decode('utf-8')


def get_level():
    dirname = os.path.dirname(fname)
    cnt = 0
    while not os.path.isfile(os.path.join(dirname, 'api.css')):
        dirname = os.path.join(dirname, '..')
        cnt += 1
    return cnt


print("Processing {} ...".format(fname))
level = get_level()
soup = bs4.BeautifulSoup(html, 'lxml')


def remove(*args, **kwargs):
    rs = soup.findAll(*args, **kwargs)
    for r in rs:
        r.extract()


remove('header')
remove('footer')
remove('nav')
remove('div', { 'class': 'toc'})
remove('devsite-header')
remove('devsite-content-footer')
remove('script')

# point to the new css
allcss = soup.findAll('link', attrs={'rel': 'stylesheet'})
if allcss:
    for _css in allcss:
        print(_css['href'])
        if '/css/vendor/' in _css['href']:
            _css['href'] = 'https://js.tensorflow.org/css/vendor/' + _css['href'].split('/')[-1]
        elif '/css/' in _css['href']:
            _css['href'] = ''.join(['../'] * level) + _css['href'].split('/')[-1]
        else:
            _css.extract()


try:
    title_node = soup.findAll('h1', attrs={'class': 'devsite-page-title'})
    if title_node:
        title_node = title_node[0]

        # mark method
        method_node = soup.findAll('h2', attrs={'class': 'method'})
        if method_node:
            title_node.attrs['class'] = 'dash-class'
            title = title_node.getText().strip()
            body = method_node[0].parent
            children = body.children
            children = [x for x in children if x != '\n']
            for k in range(len(children) - 1):
                if children[k].name == 'h3' and children[k + 1].name == 'pre':
                    # is a method:
                    children[k].attrs['class'] = 'dash-method'
                    code = next(children[k].children)
                    code.string = title + '.' + code.text
                    #print("Find method ", children[k].getText())
        else:
            title_node.attrs['class'] = 'dash-function'
except Exception:
    print("Error parsing {}".format(fname))

# mathjax doesn't work currently
# jss = soup.findAll('script')
# for js in jss:
    # if 'MathJax' in js.get('src'):
        # js['src'] = '/'.join(['..'] * level) + js['src']
        # break

to_write = str(soup).encode('utf-8')
with open(fname, 'wb') as f:
    f.write(to_write)
