class Solution{
    public:
    bool validateBinaryTreeNodes(
    int n,
    vector<int>& leftChild,
    vector<int>& rightChild
) {
    vector<int> parent(n, -1);

    // 1. Assign parents.
    //    If a node gets assigned twice, it has two parents -> invalid.
    for (int i = 0; i < n; i++) {
        int children[2] = {leftChild[i], rightChild[i]};

        for (int child : children) {
            if (child == -1) continue;

            if (parent[child] != -1)
                return false;

            parent[child] = i;
        }
    }

    // 2. Find the unique root.
    int root = -1;

    for (int i = 0; i < n; i++) {
        if (parent[i] == -1) {
            if (root != -1)
                return false;  // second root

            root = i;
        }
    }

    if (root == -1)
        return false;

    // 3. Traverse from root.
    vector<bool> visited(n, false);
    queue<int> q;

    q.push(root);
    int count = 0;

    while (!q.empty()) {
        int node = q.front();
        q.pop();

        if (visited[node])
            return false;  // cycle / repeated visit

        visited[node] = true;
        count++;

        if (leftChild[node] != -1)
            q.push(leftChild[node]);

        if (rightChild[node] != -1)
            q.push(rightChild[node]);
    }

    // 4. Every node must belong to this one tree.
    return count == n;
}};
