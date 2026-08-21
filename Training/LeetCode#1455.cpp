class Solution {
public:
    int isPrefixOfWord(string sentence, string searchWord) {
        std::string current;
        int i = 1;
        for (char c : sentence) {
            if (c == ' ') {
                if (current == searchWord) {
                    return i;
                } else {
                    current.clear();
                    i++;
            } 
            } else {
            current.push_back(c);
            if (current == searchWord)
                return i;
            }
        }
        return -1;
    }
};
