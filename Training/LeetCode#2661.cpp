#include <map>
#include <vector>
using namespace std;

class Solution {
public:
    int firstCompleteIndex(vector<int>& arr, vector<vector<int>>& mat) {
        int m = mat.size();       // rows
        int n = mat[0].size();    // columns

        map<int, pair<int, int>> pos;

        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                pos[mat[r][c]] = {r, c};
            }
        }

        vector<int> row_count(m, 0);
        vector<int> col_count(n, 0);

        for (int i = 0; i < arr.size(); i++) {
            auto [r, c] = pos[arr[i]];

            row_count[r]++;
            col_count[c]++;

            if (row_count[r] == n || col_count[c] == m) {
                return i;
            }
        }

        return -1;
    }
};
