"""Cap construction from full Hill H112 and arbitrary SUBSET of second Hill B112.

ALL deletion patterns (2^112) covered in this conditional search. C free cap
with compatible edges. Objective max |C|-|deleted B|. >=13 => valid 237.
NOT a full r3(7) disproof if restricted search fails.
"""
import os,time,json
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from scipy.sparse import coo_matrix,vstack,csr_matrix
from scipy.optimize import milp,Bounds,LinearConstraint
start=time.monotonic()
S=[l.strip() for l in open('/mnt/data/capset_v5/witness236.txt') if len(l.strip())==7]
H=np.array(sorted(int(t[1:],3) for t in S if t[0]=='0'),dtype=np.int32)
B=np.array(sorted(int(t[1:],3) for t in S if t[0]=='1'),dtype=np.int32)
C0=np.array(sorted(int(t[1:],3) for t in S if t[0]=='2'),dtype=np.int32)
assert (len(H),len(B),len(C0))==(112,112,12)
N=729
D=np.array([[int(v) for v in np.base_repr(i,3).zfill(6)] for i in range(N)],dtype=np.int8)
W=3**np.arange(5,-1,-1)
third=((6-D[:,None,:]-D[None,:,:])%3)@W
p,q=np.triu_indices(N,k=1);k=third[p,q];mask=k>q
p=p[mask];q=q[mask];k=k[mask]
assert len(p)==88452
L=len(p);W2=112
# y_z = choose z in outside C; x_j=delete jth original B point.
rows=np.repeat(np.arange(L,dtype=np.int32),3)
cols=np.stack([p,q,k],axis=1).ravel().astype(np.int32)
edgeC=third[np.ix_(H,B)].ravel()
edgeB=np.tile(np.arange(112,dtype=np.int32),len(H))+N
R0=np.arange(L,L+len(edgeC),dtype=np.int32)
rr=np.concatenate([rows,np.repeat(R0,2)])
cc=np.concatenate([cols,np.stack([edgeC,edgeB],axis=1).ravel()])
v=np.concatenate([np.ones(len(cols)),np.tile(np.array([1.,-1.]),len(edgeC))])
M=coo_matrix((v,(rr,cc)),shape=(L+len(edgeC),N+W2)).tocsr()
ub=np.r_[np.full(L,2.,dtype=float),np.zeros(len(edgeC))]
base=np.zeros(N+W2)
base[C0]=1
assert np.max(M@base-ub)<=1e-9
print('CONTROL',json.dumps({'source_profit':int(base[:N].sum()-base[N:].sum()),'valid_236':True}),flush=True)
print('MODEL',json.dumps({'variables':N+W2,'rows':M.shape[0],'nnz':M.nnz,'C_lines':L,'cross_implications':len(edgeC),'build_s':round(time.monotonic()-start,3)}),flush=True)
c=np.r_[-np.ones(N),np.ones(W2)]
res=milp(c=c,integrality=np.ones(N+W2),bounds=Bounds(np.zeros(N+W2),np.ones(N+W2)),constraints=LinearConstraint(M,-np.inf,ub),options={'time_limit':5.,'disp':True,'mip_rel_gap':0.0})
out={'solver_status':int(res.status),'message':res.message,'elapsed_s':round(time.monotonic()-start,3),'dual_objective':None if res.mip_dual_bound is None else float(res.mip_dual_bound)}
if res.x is not None:
 C=np.flatnonzero(res.x[:N]>0.5)
 keepB=B[np.flatnonzero(res.x[N:]<0.5)]
 codes=[(0,int(i)) for i in H]+[(1,int(i)) for i in keepB]+[(2,int(i)) for i in C]
 tot=len(codes)
 X=set(codes)
 # Independent arithmetic checker: all 3APs in 7D, with 3 distinct points.
 S7=set((t,)+tuple(D[i]) for t,i in codes)
 assert len(S7)==tot
 for a in S7:
  for b in S7:
   if a<b:assert tuple((-a[j]-b[j])%3 for j in range(7)) not in S7
 out.update({'best_profit':len(C)-(112-len(keepB)),'total_selected':tot,'verified':True,'B_kept':len(keepB),'C':len(C)})
 if tot>=237:
  open('/mnt/data/capset_v5/CAP057_237_WITNESS.txt','w').write('n: 7\n'+'\n'.join(str(t)+np.base_repr(i,3).zfill(6) for t,i in codes)+'\n')
else:out.update({'best_profit':None,'verified':False})
print('RESULT',json.dumps(out),flush=True)
open('/mnt/data/capset_v5/hill_trade_result.json','w').write(json.dumps(out,indent=2)+'\n')
