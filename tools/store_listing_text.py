"""Review and submit text-only updates using existing Store credentials."""
import copy
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

PRODUCTS = {'snakk': ('9P42NBXD8W36', 'Skrivi.Skrivi'), 'lytt': ('9P1QJRTS5W3K', 'Skrivi.SkriviLytt')}
BASE = 'https://manage.devcenter.microsoft.com/v1.0/my/'

def packages_match(left, right):
    def normalized(packages):
        # Store PUT omits targetPlatform on unchanged packages; retain all other checks.
        return [{k: v for k, v in p.items() if k != 'targetPlatform'} for p in packages]
    return normalized(left) == normalized(right)

def main():
    product = os.environ['PRODUCT']
    mode = os.environ['MODE']
    app_id, identity = PRODUCTS[product]
    tenant = os.environ['AZURE_AD_TENANT_ID']
    body = urllib.parse.urlencode({'grant_type': 'client_credentials', 'client_id': os.environ['AZURE_AD_APPLICATION_CLIENT_ID'], 'client_secret': os.environ['AZURE_AD_APPLICATION_SECRET'], 'resource': 'https://manage.devcenter.microsoft.com'}).encode()
    with urllib.request.urlopen(urllib.request.Request(f'https://login.microsoftonline.com/{tenant}/oauth2/token', data=body), timeout=60) as response:
        token = json.load(response)['access_token']
    print(f'::add-mask::{token}')

    def api(path, method='GET', data=None):
        request = urllib.request.Request(BASE + path, method=method, headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, data=json.dumps(data, ensure_ascii=False).encode() if data is not None else None)
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
            return json.loads(payload) if payload else {}

    path = f'applications/{app_id}'
    app = api(path)
    assert app['packageIdentityName'] == identity
    assert app['publisherName'] == 'CN=EF3D997F-87B2-4AD0-B65B-877EE1632E65'
    pending = app.get('pendingApplicationSubmission') or {}
    published = app.get('lastPublishedApplicationSubmission') or {}
    print(json.dumps({'product': product, 'primaryName': app['primaryName'], 'published': published.get('id'), 'pending': pending.get('id')}))
    if mode == 'status':
        sid = pending.get('id') or published.get('id')
        print(json.dumps(api(f'{path}/submissions/{sid}/status')))
        return
    current = api(f'{path}/submissions/{published["id"]}')
    if mode == 'inspect':
        print(json.dumps(current['listings'], ensure_ascii=False, indent=2))
        if pending.get('id'):
            draft = api(f'{path}/submissions/{pending["id"]}')
            print(json.dumps({'publishedPackages': current['applicationPackages'], 'draftPackages': draft['applicationPackages']}, ensure_ascii=False))
        return
    assert mode == 'submit'
    edits = json.loads(Path(f'store/listing/{product}-text.json').read_text(encoding='utf-8'))
    if pending.get('id'):
        # Resume only these two drafts created and saved by the authorized text update.
        known_drafts = {'snakk': '1152921505701939985', 'lytt': '1152921505701939877'}
        assert pending['id'] == known_drafts[product], 'Unrecognized draft: leave it untouched.'
        sid = pending['id']
        saved = api(f'{path}/submissions/{sid}')
        assert saved['status'] == 'PendingCommit', 'Submission is already processing.'
        for lang, fields in edits.items():
            for key, value in fields.items():
                assert saved['listings'][lang]['baseListing'][key] == value
        assert packages_match(saved['applicationPackages'], current['applicationPackages'])
        print(json.dumps({'submission': sid, 'textVerified': True, 'packagesUnchanged': True}), flush=True)
        print(json.dumps(api(f'{path}/submissions/{sid}/commit', 'POST')))
        print(json.dumps(api(f'{path}/submissions/{sid}/status')))
        return
    draft = api(f'{path}/submissions', 'POST')
    sid = draft['id']
    print('Created text-only submission:', sid, flush=True)
    original = copy.deepcopy(draft)
    for lang, fields in edits.items():
        listing = draft['listings'][lang]['baseListing']
        for key, value in fields.items():
            assert key in ('title', 'description', 'shortDescription', 'features')
            listing[key] = value
    # All package, image, pricing and publication settings stay as copied by Microsoft.
    restore = copy.deepcopy(draft)
    for lang, fields in edits.items():
        for key in fields:
            old = original['listings'][lang]['baseListing']
            if key in old: restore['listings'][lang]['baseListing'][key] = old[key]
            else: restore['listings'][lang]['baseListing'].pop(key, None)
    assert restore == original, 'Unexpected non-text change'
    api(f'{path}/submissions/{sid}', 'PUT', draft)
    saved = api(f'{path}/submissions/{sid}')
    for lang, fields in edits.items():
        for key, value in fields.items():
            assert saved['listings'][lang]['baseListing'][key] == value, f'{lang} {key} did not save'
    assert packages_match(saved['applicationPackages'], original['applicationPackages']), 'Packages unexpectedly changed'
    print(json.dumps({'submission': sid, 'locales': list(edits), 'packagesUnchanged': True}))
    print(json.dumps(api(f'{path}/submissions/{sid}/commit', 'POST')))
    print(json.dumps(api(f'{path}/submissions/{sid}/status')))

if __name__ == '__main__':
    main()
