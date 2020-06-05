import sys

import tython

if len(sys.argv) > 1:
    feed_in = sys.argv[1]
    if '--tree' in sys.argv:
        debug = True
    else:
        debug = False
    print(tython.parse(open(feed_in).read(), debug))
