// #include <vector>
// #include <climits>

// class Solution {
// public:
//     long long totalCost(vector<int>& costs, int k, int candidates) {
//         vector<int> eligible; 
//         long long cost = 0;
//         while (k > 0){
//             int worker = INT_MAX;
//             if (costs.size() >= candidates*2) {
//                 for (int i = 0; i < candidates; i++){
//                     eligible.push_back(costs[i]);
//                 }
//                 for (int i = costs.size() - candidates; i < costs.size(); i++){
//                     eligible.push_back(costs[i]);
//                 }
//             } else {
//                 for (int x : costs){
//                     eligible.push_back(x);
//                 }
//             }

//             for (int x : eligible){
//                 worker = std::min(worker, x);
//             }

//             for (int i = 0; i < eligible.size(); i++){
//                 if (eligible[i] == worker){
//                     cost += worker;
//                     if (i < candidates){
//                         costs.erase(costs.begin() + i);
//                     } else {
//                         if (eligible.size() == costs.size()){
//                             costs.erase(costs.begin() + i);
//                         } else{ 
//                         costs.erase(costs.begin() + costs.size() - 2*candidates + i);
//                     }
//                     }
//                     break;
//                 }
//             }
//             k--;
//             eligible.clear();
//         }
//     return cost;
//     }
// };

#include <vector>
#include <queue>
#include <tuple>
using namespace std;

class Solution {
public:
    long long totalCost(vector<int>& costs, int k, int candidates) {
        int n = costs.size();

        // (cost, index, side)
        // side: 0 = left, 1 = right
        priority_queue<
            tuple<int, int, int>,
            vector<tuple<int, int, int>>,
            greater<tuple<int, int, int>>
        > pq;

        int left = 0;
        int right = n - 1;

        // Load left candidates
        for (int i = 0; i < candidates && left <= right; ++i) {
            pq.push({costs[left], left, 0});
            left++;
        }

        // Load right candidates
        for (int i = 0; i < candidates && left <= right; ++i) {
            pq.push({costs[right], right, 1});
            right--;
        }

        long long total = 0;

        for (int hired = 0; hired < k; ++hired) {
            auto [cost, index, side] = pq.top();
            pq.pop();

            total += cost;

            if (left <= right) {
                if (side == 0) {
                    pq.push({costs[left], left, 0});
                    left++;
                } else {
                    pq.push({costs[right], right, 1});
                    right--;
                }
            }
        }

        return total;
    }
};
