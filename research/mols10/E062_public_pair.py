"""Independent read of the public orthogonal pair in scheinerman/LatinSquares.jl/ortho10.txt."""
import re,json,sys
from pathlib import Path
from E061_transversal_route import verify_pair, common_transversals, maxpack
SOURCE='''
(1,1) (2,2) (3,3) (4,4) (5,5) (6,6) (7,7) (8,8) (9,9) (10,10)
(2,3) (9,4) (8,6) (5,8) (1,7) (10,1) (4,9) (3,10) (6,5) (7,2)
(7,9) (3,5) (9,1) (6,10) (8,4) (5,2) (2,8) (10,6) (4,7) (1,3)
(8,10) (4,1) (6,7) (1,2) (7,3) (3,8) (9,5) (2,9) (10,4) (5,6)
(9,2) (6,3) (1,5) (10,7) (4,8) (7,4) (3,6) (5,1) (2,10) (8,9)
(10,5) (1,6) (7,8) (8,3) (6,9) (4,10) (5,4) (9,7) (3,2) (2,1)
(4,6) (5,9) (2,4) (7,1) (9,10) (8,5) (10,3) (6,2) (1,8) (3,7)
(3,4) (8,7) (5,10) (2,5) (10,2) (1,9) (6,1) (4,3) (7,6) (9,8)
(5,7) (10,8) (4,2) (3,9) (2,6) (9,3) (1,10) (7,5) (8,1) (6,4)
(6,8) (7,10) (10,9) (9,6) (3,1) (2,7) (8,2) (1,4) (5,3) (4,5)
'''
rows=[[(int(x)-1,int(y)-1) for x,y in re.findall(r'\((\d+),\s*(\d+)\)',line)] for line in SOURCE.strip().splitlines()]
A=[[p[0] for p in row] for row in rows];B=[[p[1] for p in row] for row in rows]
verify_pair(A,B)
tr,nodes=common_transversals(A,B);pack=maxpack(tr,len(A))
print(json.dumps({'source':'scheinerman/LatinSquares.jl/ortho10.txt','common_transversals':len(tr),'max_disjoint':len(pack),'transversal_nodes':nodes,'sample_transversals':tr[:8],'max_pack_indices':pack},indent=2))
Path(__file__).with_name('E062_PUBLIC_PAIR_RESULT.json').write_text(json.dumps({'A':A,'B':B,'source':'scheinerman/LatinSquares.jl/ortho10.txt','transversals':tr,'max_disjoint_indices':pack},indent=2))