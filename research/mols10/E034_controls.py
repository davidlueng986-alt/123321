from E034_direct_completion import completion,validate
for n in (4,5):
 if n==4:
  def mul(a,b):
   v=0
   for k in range(2):
    if (b>>k)&1:v^=a<<k
   if v&8:v^=0b1100 # x^3 = x(x^2+x+1)
   if v&4:v^=0b111
   return v
  plus=lambda a,b:a^b
 else:
  mul=lambda a,b:a*b%n
  plus=lambda a,b:(a+b)%n
 S=[[[plus(r,mul(a,c)) for c in range(n)] for r in range(n)] for a in (1,2,3)]
 validate(S)
 for k in (1,2):
  z=completion(tuple(range(k)),secs=10,S_override=S)
  print('positive control',n,k,z['status'],z['vars'],z['constraints'],z['nodes'],flush=True)
  if z['status']=='SAT':validate(z['solution'])
