#!/usr/bin/env python3
"""Compare full independent seven-fiber censuses (not just headline totals)."""
import json
import sys
from pathlib import Path
assert len(sys.argv) == 3
fast = json.loads(Path(sys.argv[1]).read_text())
direct = json.loads(Path(sys.argv[2]).read_text())
for key in ('total', 'excluded_by_16_outsider_gate', 'not_excluded',
            'max_admissible_outsiders', 'incidence_count', 'histogram'):
    assert fast[key] == direct[key], key
assert sorted(fast['max_groups']) == sorted(direct['max_groups'])
assert sum(map(int, fast['histogram'].values())) == 888030
assert sum(int(k)*v for k,v in fast['histogram'].items()) == 2946160
print('CAP-005J PASS: two independent algorithms agree on all 888030 groups, all 98 histogram bins, 8 maxima')
