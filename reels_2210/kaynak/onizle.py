import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sahneler import REELS
import kit
r = REELS[sys.argv[1]]()
open(f'{r["ad"]}.html','w').write(r['html'])
z = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv)>2 else r['vurgu']
kit.onizle(f'{r["ad"]}.html', [x+500 for x in z], f'on_{r["ad"]}.jpg', flow=r['flow'])
print('ok', r['ad'])
