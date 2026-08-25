int countOnes(int num) {
        int count = 0;

        while (num != 0) {
            if (num % 2 == 1) {
                count++;
            }
            num = num >> 1;
        }
        return count;
    }

class Solution {
public:
    int maximumRows(vector<vector<int>>& matrix, int numSelect) {
        int m = matrix[0].size();
        int n = matrix.size();
        int max_row = 0;    
        int count = 0;
        // int combinations = (factorial(size)) / (factorial(size - numSelect) * factorial(numSelect)); 
        vector<int> rowMask(n, 0);
        
        for (int i = 0; i < matrix.size(); i++) {
            for (int j = 0; j < matrix[0].size(); j++) {
                rowMask[i] |= (matrix[i][j] << j);
            }
        }

        for (int mask = 0; mask < (1 << m); mask++) {
            int foo = countOnes(mask);
            if (foo != numSelect) {
                continue;
            }
            for (int x : rowMask) {
                if ((x & mask) == x) {
                    count++;
            }
            }
            max_row = max(max_row, count);
            count = 0;
        }
        return max_row;
    }
};



//So first step read the question, done
//second, what is the brute force implementation look like: 
// We are trying to maximize covered rows, where covered looks like all 0s, or 1s in selected columns, naturally i think you would want to select columns with the most number of 1s
// However im sure there are edge cases in where this does not produce the right result.
// the brute force implementation would be to loop over every configuration of numSelect selected columns over the matrix, then keep track of the maximum and return the value
// So it will be choose(size, numSelect) combinations, then I'll have to calculate the number of covered rows, and return that maximum after the loop
// What is challenging is going to be 
// note: choose(n, k) = (n! / ((n-k)! * k!)), so thats what we will loop over. well actually this is the brute force implementation, its definitely not optimal.
// idrc tho but how would i cover the whole space... ok covering the whole space would just really be start a 0, 1, then 0,2 ... then 2,3 2,4 2,5 3,4 3,5 etc. this would be rlly tricky if numselect wasnt 2 tho, ill ask chatgpt about something for that, cuz its good to know, but in reality the best way to solve this is:
// for every matrix[0].size() bit mask with numselect 1s, we count how many rows it covers, and update maximum. 
// ALL THE ONES IN ROW MASK HAVE TO BE ANDED WITH selectMASK, otherwise it doesnt matter... hm
