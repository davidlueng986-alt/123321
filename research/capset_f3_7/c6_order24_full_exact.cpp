// CAP-004G: exact finite exhaustion of ALL order-24-invariant 7D caps.
// Input from c6_order24_full_exact_data.py, verified by Python arithmetic.
// NO claim of a global r_3(7) upper bound. C++17, no solver or GPU.
#include <algorithm>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

constexpr int N = 45, V = 11434;
using Bits = std::bitset<V>;
struct Mask { uint64_t bits; int weight; };

int main(int argc, char **argv) {
    if (argc != 2) {
        std::cerr << "Usage: c6_order24_full_exact INPUT_DATA\n";
        return 2;
    }
    auto start = std::chrono::steady_clock::now();
    std::ifstream f(argv[1]);
    int n = 0;
    if (!(f >> n) || n != V) return 2;
    std::vector<Mask> valid(n);
    for (auto &p : valid)
        if (!(f >> p.bits >> p.weight)) return 2;
    uint64_t shadow[N][N];
    for (auto &row : shadow)
        for (auto &v : row)
            if (!(f >> v)) return 2;

    std::sort(valid.begin(), valid.end(), [](Mask a, Mask b) {
        return a.weight != b.weight ? a.weight > b.weight : a.bits < b.bits;
    });
    Bits containing[N], at_least[113], at_most[113];
    for (int k = 0; k < n; ++k) {
        auto [mask, weight] = valid[k];
        if (weight < 0 || weight > 112 || (mask >> N)) return 2;
        while (mask) {
            int i = __builtin_ctzll(mask);
            containing[i].set(k);
            mask &= mask - 1;
        }
        for (int t = 1; t <= weight; ++t) at_least[t].set(k);
        for (int t = weight; t <= 112; ++t) at_most[t].set(k);
    }

    // Every permutation of three first-coordinate slices is affine over F3.
    // Thus a hypothetical >=237 cap may be assumed wA>=wB>=wC.
    // For each unordered (A,B), only wA+2*wB>=237 can succeed.
    // All feasible C masks are tested simultaneously by exact bitset logic.
    uint64_t inspected = 0, eligible = 0;
    for (size_t ia = 0; ia < valid.size(); ++ia) {
        auto [ma, wa] = valid[ia];
        uint64_t blocked_by_orbit[N] = {};
        uint64_t x = ma;
        while (x) {
            int i = __builtin_ctzll(x);
            x &= x - 1;
            for (int j = 0; j < N; ++j)
                blocked_by_orbit[j] |= shadow[i][j];
        }
        for (size_t ib = ia; ib < valid.size(); ++ib) {
            auto [mb, wb] = valid[ib];
            ++inspected;
            if (wa + 2 * wb < 237) break;  // all later wb are smaller.
            ++eligible;
            int needed = 237 - wa - wb;
            if (needed < 1 || needed > wb || wb > 112) return 3;
            Bits possible = at_least[needed] & at_most[wb];
            uint64_t blocked = 0, y = mb;
            while (y) {
                int j = __builtin_ctzll(y);
                y &= y - 1;
                blocked |= blocked_by_orbit[j];
            }
            // For every orbit blocked by cross-slice lines, remove all
            // third-slice valid masks that contain that orbit.
            while (blocked && possible.any()) {
                int k = __builtin_ctzll(blocked);
                blocked &= blocked - 1;
                possible &= ~containing[k];
            }
            if (possible.any()) {
                for (int k = 0; k < n; ++k) if (possible.test(k)) {
                    auto [mc, wc] = valid[k];
                    std::cout << "{\"status\":\"POSSIBLE_237_NEEDS_INDEPENDENT_CHECK\","
                              << "\"masks\":[" << ma << "," << mb << "," << mc << "],"
                              << "\"sizes\":[" << wa << "," << wb << "," << wc << "]}\n";
                    return 1;
                }
                return 3;
            }
        }
    }
    // These counts make the finite exhaustion reproducible and auditable.
    if (inspected != 3436063 || eligible != 3424629) return 3;
    auto elapsed = std::chrono::duration<double>(
        std::chrono::steady_clock::now() - start).count();
    std::cout << "{\"status\":\"NO_237_ORDER24_INVARIANT\","
              << "\"valid_masks\":" << n << ","
              << "\"unordered_pairs_total\":65373895,"
              << "\"inspected_pairs\":" << inspected << ","
              << "\"eligible_pairs\":" << eligible << ","
              << "\"seconds\":" << elapsed << "}\n";
    return 0;
}
