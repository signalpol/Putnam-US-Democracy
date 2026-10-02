from pathlib import Path
import base64
for p in Path('.').glob('*.base64'):
 p.with_suffix('').write_bytes(base64.b64decode(p.read_bytes(),validate=True))
