#include <map>
#include <vector>
using namespace std;
// Brute force would be O(N^3), that is n prefixes, n deletions, and n frequency counting.
// We want to keep track of not only the frequency of nums[i], but also the frequency of 
// Each frequency, thats two maps.
// Once we have a prefix with a frequency distribution of:
//  1, 1, 1, 1, 1, 1, 1
//  k, k ,
class Solution {
public:
    int maxEqualFreq(vector<int>& nums) {
        map<int, int> freq; //This is the frequency of each number in nums
	map<int, int> countFreq; //This is the frequency of EACH frequency
    	int maxFreq = 0; 
	int distinctCount = 0;
	int prefixLength = 0;
	for (int x : nums) { // Build freq and countFreq
        int oldFreq = freq[x];
        if (oldFreq > 0) {
            countFreq[oldFreq]--;
        }
		freq[x]++; //increment value of key x in freq
		countFreq[freq[x]]++; //increment value of key freq[x] in countFreq

		maxFreq = max(maxFreq, freq[x]);
		if (freq[x] == 1){
			distinctCount++;
		}
	}
	
	for (int i = nums.size(); i > 0; i--){
		if (valid(countFreq, maxFreq, distinctCount, i)){
			return i;
		}
        int x = nums[i - 1];
        int oldFreq = freq[x];
        countFreq[oldFreq]--;
        freq[x]--;
        if (freq[x] > 0){
            countFreq[freq[x]]++;
        }
        if (countFreq[maxFreq] == 0){
            maxFreq--;
        }
        if (freq[x] == 0) {
            distinctCount--;
        }
        }
    return 0;
}
	bool valid(map<int, int>& countFreq, int maxFreq, int distinctCount, int prefixLength){
		if (countFreq[1] == prefixLength) {
			return true;
		} else if (countFreq[1] == 1 && countFreq[maxFreq] == distinctCount-1){
			return true;
		} else if (countFreq[maxFreq] == 1 && countFreq[maxFreq-1] == distinctCount-1){
			return true;
		} else {return false;}
	}
};
