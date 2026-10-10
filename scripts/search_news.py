"""Search Google News RSS for each country between two dates and write candidates.json.

Run by .github/workflows/search.yml. Inputs come from the START and END
environment variables (YYYY-MM-DD, inclusive). Standard library only.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

ISTANBUL = timezone(timedelta(hours=3))
MAX_DAYS = 14
PER_COUNTRY = 40
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

COUNTRIES = [
    {'id': 'sa', 'name': 'Saudi Arabia', 'short': 'Saudi Arabia', 'capital': 'Riyadh', 'q': '"Saudi Arabia" OR Saudi'},
    {'id': 'ae', 'name': 'United Arab Emirates', 'short': 'UAE', 'capital': 'Abu Dhabi', 'q': 'UAE OR "United Arab Emirates" OR Dubai'},
    {'id': 'qa', 'name': 'Qatar', 'short': 'Qatar', 'capital': 'Doha', 'q': 'Qatar'},
    {'id': 'kw', 'name': 'Kuwait', 'short': 'Kuwait', 'capital': 'Kuwait City', 'q': 'Kuwait'},
    {'id': 'bh', 'name': 'Bahrain', 'short': 'Bahrain', 'capital': 'Manama', 'q': 'Bahrain'},
    {'id': 'om', 'name': 'Oman', 'short': 'Oman', 'capital': 'Muscat', 'q': 'Oman'},
    {'id': 'iq', 'name': 'Iraq', 'short': 'Iraq', 'capital': 'Baghdad', 'q': 'Iraq'},
]
# Each country is searched once plainly and once with a business focus.
FOCUS = ['', '(economy OR business OR trade OR investment OR logistics OR fintech)']

# First match wins, so the order matters.
CATEGORIES = [
    ('emergency', r'attack|missile|drone|strike|killed|explosion|blast|houthi|intercept|evacuat|injur|earthquake|flood|sirens?\b|war\b|militant'),
    ('turkey', r'turkey|turkish|türkiye|ankara|erdogan|istanbul'),
    ('payments', r'payment|fintech|wallet|visa\b|mastercard|remittance|digital bank|neobank|crypto'),
    ('tax', r'\btax|\bvat\b|incentive|customs dut|tariff|zakat'),
    ('logistics', r'shipping|\bports?\b|logistic|freight|cargo|container|hormuz|maritime|supply chain|rail'),
    ('ecommerce', r'e-commerce|ecommerce|retail|online shopping|amazon|\bnoon\b|talabat|marketplace|consumer spending'),
    ('economy', r'econom|gdp|\boil\b|opec|invest|stock|market|inflation|\bbank|bond|budget|pmi|\btrade|billion|million|growth|fund|ipo'),
]
ROUNDUP = r'live updates|live:|need to know|roundup|round-up|briefing|what we know'


def parse_day(s, name):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', s or ''):
        sys.exit(f'{name} must look like YYYY-MM-DD, got {s!r}')
    return date.fromisoformat(s)


def fetch_rss(query, start, end):
    q = f'({query}) after:{start.isoformat()} before:{(end + timedelta(days=1)).isoformat()}'
    url = 'https://news.google.com/rss/search?' + urllib.parse.urlencode(
        {'q': q, 'hl': 'en-US', 'gl': 'US', 'ceid': 'US:en'})
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (gulf-morning-brief)'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return ET.fromstring(r.read())
        except Exception as e:  # network hiccup or rate limit: back off and retry
            print(f'  retry {attempt + 1} for {query!r}: {e}', file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    print(f'  giving up on {query!r}', file=sys.stderr)
    return None


def categorize(title):
    low = title.lower()
    for key, pattern in CATEGORIES:
        if re.search(pattern, low):
            return key
    return 'politics'


def norm(title):
    return re.sub(r'[^a-z0-9]+', ' ', title.lower()).strip()


def collect(start, end):
    stories, seen = [], set()
    for c in COUNTRIES:
        found = []
        for focus in FOCUS:
            root = fetch_rss(f'({c["q"]}) {focus}' if focus else c['q'], start, end)
            time.sleep(1.5)
            if root is None:
                continue
            for item in root.iter('item'):
                title = (item.findtext('title') or '').strip()
                link = (item.findtext('link') or '').strip()
                source = (item.findtext('source') or '').strip()
                try:
                    day = parsedate_to_datetime(item.findtext('pubDate')).astimezone(ISTANBUL).date()
                except Exception:
                    continue
                if not (title and link.startswith('http') and start <= day <= end):
                    continue
                if source and title.endswith(' - ' + source):
                    title = title[: -len(source) - 3].rstrip()
                key = norm(title)
                if key in seen:
                    continue
                seen.add(key)
                found.append({'c': c['id'], 't': title, 'u': link, 's': source or 'Unknown source',
                              'd': day.isoformat(), 'k': categorize(title)})
        found.sort(key=lambda s: s['d'], reverse=True)
        found = found[:PER_COUNTRY]
        for i, s in enumerate(found):
            s['id'] = f'{c["id"]}-{i + 1}'
            s['n'] = i
            if re.search(ROUNDUP, s['t'].lower()):
                s['r'] = True
        print(f'{c["name"]}: {len(found)} stories')
        stories.extend(found)
    return stories


def label(start, end):
    if start == end:
        return f'{MONTHS[end.month - 1]} {end.day}, {end.year}'
    if start.year != end.year:
        return f'{MONTHS[start.month - 1]} {start.day}, {start.year} – {MONTHS[end.month - 1]} {end.day}, {end.year}'
    if start.month != end.month:
        return f'{MONTHS[start.month - 1]} {start.day} – {MONTHS[end.month - 1]} {end.day}, {end.year}'
    return f'{MONTHS[end.month - 1]} {start.day}–{end.day}, {end.year}'


def main():
    start = parse_day(os.environ.get('START'), 'START')
    end = parse_day(os.environ.get('END'), 'END')
    if start > end:
        sys.exit('START must not be after END')
    days = (end - start).days + 1
    if days > MAX_DAYS:
        sys.exit(f'Range is {days} days; the limit is {MAX_DAYS}')

    stories = collect(start, end)
    now = datetime.now(ISTANBUL)
    out = {
        'edition': {
            'date': end.isoformat(),
            'start': start.isoformat(),
            'label': label(start, end),
            'titleDate': f'{MONTHS[end.month - 1]} {end.day}, {end.year}',
            'windowLabel': f'{days}-day window' if days > 1 else '1-day window',
            'scanned': now.strftime('%H:%M') + ' Istanbul',
            'updated': f'{now.day} {now.strftime("%b %Y, %H:%M")} Istanbul',
            'generatedAt': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        },
        'countries': [{k: c[k] for k in ('id', 'name', 'short', 'capital')} for c in COUNTRIES],
        'stories': stories,
        'selected': [],
        'footer': [
            f'Covers {label(start, end)}. Stories were gathered automatically from Google News search, English-language results only.',
            'Headline links open the story through Google News, which forwards to the publisher.',
        ],
    }
    with open('candidates.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'Wrote candidates.json with {len(stories)} stories')


if __name__ == '__main__':
    main()
