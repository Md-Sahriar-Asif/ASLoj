#include<iostream>
using namespace std;
int main()
{
    int num1, num2;
    char op;
    cout << "enetr first number: ";
    cin >> num1;
    cout << "enetr an operator: ";
    cin >> op;
    cout << "enetr second number: ";
    cin >> num2;
    int result;
    if(op == '+'){
        result = num1+num2;
    }
    else if(op == '-'){
         result = num1-num2;
    }
    else if(op == '/'){
         result = num1/num2;
    }
    else if(op == '*'){
         result = num1*num2;
    }
    else{
        cout << "invalid operator.";
    }
    cout << "your result: " << result << endl;
    return 0;
}