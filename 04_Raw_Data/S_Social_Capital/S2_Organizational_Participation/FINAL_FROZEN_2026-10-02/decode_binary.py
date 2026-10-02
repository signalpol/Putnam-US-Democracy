from pathlib import Path
import base64
for p in Path('.').glob('*.base64'):
 out=p.with_suffix('');out.write_bytes(base64.b64decode(p.read_bytes(),validate=True));print(out)
