#include <bits/stdc++.h>
using namespace std;
using Clock=chrono::steady_clock;
struct Mat{array<unsigned char,100> x;};
vector<Mat> read(const string &p){ifstream f(p,ios::binary);if(!f)throw runtime_error("cannot open "+p);vector<Mat> out;Mat m;while(f.read((char*)m.x.data(),100))out.push_back(m);return out;}
int main(int argc,char**argv){
 if(argc<4){cerr<<"usage A2.bin B2.bin result_idx.json\n";return 2;}
 auto A=read(argv[1]),B=read(argv[2]);auto t0=Clock::now();
 vector<pair<int,int>> found;unsigned seen[100]={0};unsigned gen=0;
 uint64_t combos=0;int maxsave=50000;uint64_t allhits=0;
 for(int i=0;i<(int)A.size();i++)for(int j=0;j<(int)B.size();j++){
  ++combos;++gen;bool ok=true;auto&a=A[i].x;auto&b=B[j].x;
  for(int p=0;p<100;p++){
   int z=a[p]*10+b[p];
   if(seen[z]==gen){ok=false;break;}
   seen[z]=gen;
  }
  if(ok){allhits++;if((int)found.size()<maxsave)found.push_back({i,j});}
 }
 double sec=chrono::duration<double>(Clock::now()-t0).count();
 ofstream out(argv[3]);out<<"{\"status\":\"EXACT_CROSS_SCAN\",\"A_variants\":"<<A.size()<<",\"B_variants\":"<<B.size()<<",\"candidates\":"<<combos<<",\"orthogonal_hits\":"<<allhits<<",\"saved_hits\":[";
 for(int k=0;k<(int)found.size();k++){if(k)out<<",";out<<"["<<found[k].first<<","<<found[k].second<<"]";}
 out<<"],\"hits_truncated\":"<<(allhits>found.size()?"true":"false")<<",\"seconds\":"<<setprecision(5)<<sec<<"}\n";
 cerr<<"FINISHED candidates="<<combos<<" hits="<<allhits<<" saved="<<found.size()<<" secs="<<sec<<"\n";
}