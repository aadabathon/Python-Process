/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */

 void binary_tree_dfs(vector<vector<int>>& res, TreeNode* base, int depth){
    if (base == nullptr) {
        return;
    }

    if (depth == res.size()) {
        res.push_back({});
    }

    if (depth % 2 == 0) {
    res[depth].push_back(base->val);
    } else {
    // res[depth].insert(res[depth].begin(), base->val); std::vector<T>.insert() is much cleaner here.
    res[depth].push_back(0);
    for (int i = res[depth].size()-1; i > 0; i--) {
        res[depth][i] = res[depth][i-1];
    }
    res[depth][0] = (base->val);
    }
    binary_tree_dfs(res, base->left, depth+1);
    binary_tree_dfs(res, base->right, depth+1);

 }
class Solution {
public:
    vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
        int d = 0;
        vector<vector<int>> result;
        binary_tree_dfs(result, root, d);
        return result;
    }
};

// This one is pretty simple
