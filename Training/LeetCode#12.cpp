#include <cmath>

class Solution {
public:
    string intToRoman(int num) {
        std::string roman = "";
        std::map<int, std::string> int_to_roman;
        int barry;
        int_to_roman[1]= "I";
        int_to_roman[4]= "IV";
        int_to_roman[5]= "V";
        int_to_roman[9]= "IX";
        int_to_roman[10]= "X";
        int_to_roman[40]= "XL";
        int_to_roman[50]= "L";
        int_to_roman[90]= "XC";
        int_to_roman[100]= "C";
        int_to_roman[400]= "CD";
        int_to_roman[500]= "D";
        int_to_roman[900]=  "CM";
        int_to_roman[1000]= "M";
        for (int i = 0; i < 4; i++){
            barry = num / static_cast<int>(std::pow(10, (3-i))) % 10;
            while (barry > 0) {
                if (barry == 9) {
                    roman.append(int_to_roman[barry * std::pow(10, (3-i))]);
                    barry -= 9;
                }
                if (barry > 5 || barry == 5) {
                    roman.append(int_to_roman[5 * std::pow(10, (3-i))]);
                    barry -= 5;
                }
                if (barry == 4) {
                    roman.append(int_to_roman[barry * std::pow(10, (3-i))]);
                    barry -= 4;
                }
                if (barry < 4 && barry > 0) {
                    roman.append(int_to_roman[std::pow(10, (3-i))]);
                    barry -= 1;
                }
            }
        }
        return roman;
    }
};
