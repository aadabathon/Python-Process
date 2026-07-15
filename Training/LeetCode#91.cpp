class Solution {
public:
    int numDecodings(string s) {
        int n = s.size();
        vector<int> dp(n + 1, 0);

        dp[n] = 1;

        for (int i = n - 1; i >= 0; i--) {
            if (s[i] == '0') {
                dp[i] = 0;
                continue;
            }

            dp[i] = dp[i + 1];

            if (i + 1 < n) {
                int twoDigit = (s[i] - '0') * 10 + (s[i + 1] - '0');

                if (twoDigit >= 10 && twoDigit <= 26) {
                    dp[i] += dp[i + 2];
                }
            }
        }

        return dp[0];
    }
};

// class Solution {
// public:
//     int numDecodings(string s) {
//         int n = s.size();

//         int nextNext = 1; // dp[i + 2]
//         int next = 0;     // dp[i + 1]

//         for (int i = n - 1; i >= 0; i--) {
//             int curr = 0;

//             if (s[i] != '0') {
//                 curr = nextNext;

//                 if (i + 1 < n) {
//                     int twoDigit = (s[i] - '0') * 10 + (s[i + 1] - '0');

//                     if (twoDigit >= 10 && twoDigit <= 26) {
//                         curr += next;
//                     }
//                 }
//             }

//             next = nextNext;
//             nextNext = curr;
//         }

//         return nextNext;
//     }
// };

// class Solution {
// public:
//     int numDecodings(string s) {
//         vector<int> memo(s.size(), -1);
//         return dfs(s, 0, memo);
//     }

//     int dfs(string& s, int i, vector<int>& memo) {
//         if (i == s.size()) return 1;     // successfully decoded all chars
//         if (s[i] == '0') return 0;       // cannot decode leading zero

//         if (memo[i] != -1) return memo[i];

//         int ways = dfs(s, i + 1, memo);  // take one digit

//         if (i + 1 < s.size()) {
//             int twoDigit = (s[i] - '0') * 10 + (s[i + 1] - '0');

//             if (twoDigit >= 10 && twoDigit <= 26) {
//                 ways += dfs(s, i + 2, memo);  // take two digits
//             }
//         }

//         memo[i] = ways;
//         return ways;
//     }
// };