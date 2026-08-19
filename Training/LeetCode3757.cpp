class Solution {
public:
    static constexpr int MOD = 1'000'000'007;

    int countEffective(vector<int>& nums) {
        int n = nums.size();

        int all = 0;
        for (int x : nums) {
            all |= x;
        }

        // Only bits actually present in the total OR matter.
        vector<int> bits;
        for (int b = 0; b < 20; ++b) {
            if (all & (1 << b)) {
                bits.push_back(b);
            }
        }

        int m = bits.size();
        int M = 1 << m;

        // cnt[mask] = number of nums whose relevant-bit mask is exactly mask.
        vector<int> cnt(M, 0);

        for (int x : nums) {
            int mask = 0;
            for (int j = 0; j < m; ++j) {
                if (x & (1 << bits[j])) {
                    mask |= (1 << j);
                }
            }
            cnt[mask]++;
        }

        // subsetCnt[mask] = number of elements whose bit-mask is a subset of mask.
        vector<int> subsetCnt = cnt;

        for (int b = 0; b < m; ++b) {
            for (int mask = 0; mask < M; ++mask) {
                if (mask & (1 << b)) {
                    subsetCnt[mask] += subsetCnt[mask ^ (1 << b)];
                }
            }
        }

        vector<long long> pow2(n + 1);
        pow2[0] = 1;
        for (int i = 1; i <= n; ++i) {
            pow2[i] = pow2[i - 1] * 2 % MOD;
        }

        /*
         * Inclusion-exclusion.
         *
         * Pick a nonempty set S of bits that we want to disappear.
         * Every element containing at least one bit in S MUST be removed.
         *
         * Elements containing none of S can either be removed or kept.
         *
         * Let allowedMask = complement of S.
         * subsetCnt[allowedMask] = # elements containing none of S.
         *
         * Therefore there are
         *     2 ^ subsetCnt[allowedMask]
         * removal subsequences that eliminate every bit in S.
         */

        long long ans = 0;
        int full = M - 1;

        for (int s = 1; s < M; ++s) {
            int allowedMask = full ^ s;

            long long ways = pow2[subsetCnt[allowedMask]];

            if (__builtin_popcount((unsigned)s) & 1) {
                ans += ways;
            } else {
                ans -= ways;
            }

            ans %= MOD;
        }

        if (ans < 0) ans += MOD;
        return (int)ans;
    }
};
