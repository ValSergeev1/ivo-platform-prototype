#!/usr/bin/env python3
"""Wrap src/*.html fragments in the shared shell. First line of each fragment:
<!--meta title="..." out="console/index.html" body="..." head="..."-->"""
import re,glob,os
ROOT=os.path.dirname(os.path.abspath(__file__))
def official_canonical(rel):
    leaf = rel.replace("\\", "/").lstrip("./")
    key = leaf.lower()
    if "apply" in key:
        return "https://ivoservgroup.com/partner-with-ivo/"
    if any(s in key for s in ("customer", "contractor", "console", "vendor", "onboarding", "portal")):
        return "https://ivoservgroup.com/portal/"
    return "https://ivoservgroup.com/"
T='''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive"><meta name="googlebot" content="noindex,nofollow">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#061d2a">
<title>{title} · IVO Platform prototype (sample data)</title>
<link rel="icon" href="{R}assets/img/favicon.png"><link rel="apple-touch-icon" href="{R}assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{R}assets/css/app.css">{head}
</head><body class="{body}">
<div class="proto-banner"><b>Prototype – sample data</b><span>V01 · fictional companies and people · nothing is sent or saved</span><a href="{R}index.html">All screens</a></div>
{content}
<script src="{R}assets/js/app.js"></script>
</body></html>
'''
for f in sorted(glob.glob(os.path.join(ROOT,'src','*.html'))):
    s=open(f).read()
    m=re.match(r'<!--meta (.*?)-->\n',s)
    meta=dict(re.findall(r'(\w+)="(.*?)"',m.group(1)))
    out=meta['out'];depth=out.count('/');R='../'*depth
    body=s[m.end():]
    body=re.sub(r'\{\{inc:(\w+)\}\}',lambda mm:open(os.path.join(ROOT,'src','inc',mm.group(1)+'.html')).read().strip(),body)
    body=body.replace('{R}',R)
    html=T.format(title=meta['title'],R=R,body=meta.get('body',''),head=meta.get('head','').replace('{R}',R),content=body,canon=official_canonical(out))
    p=os.path.join(ROOT,out);os.makedirs(os.path.dirname(p),exist_ok=True);open(p,'w').write(html)
    print('built',out)
