import base64,gzip,hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parent
m=json.loads((root/'RAW_ARCHIVE_MANIFEST.json').read_text())
parts=[]
for item in m['parts']:
 b=(root/item['file']).read_bytes()
 assert hashlib.sha256(b).hexdigest()==item['sha256']
 parts.append(b.strip())
raw=gzip.decompress(base64.b64decode(b''.join(parts)))
assert len(raw)==m['original_bytes'] and hashlib.sha256(raw).hexdigest()==m['original_sha256']
(root/m['original_file']).write_bytes(raw)
print('RAW RESTORED: exact original bytes and SHA256 verified')
