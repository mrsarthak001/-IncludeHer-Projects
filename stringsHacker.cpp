#include <iostream>
#include <string>
using namespace std;

int main() {
	// Complete the program
    string s1,s2;
    cin>>s1>>s2;
    cout<<s1.size()<<" "<<s2.size()<<endl;
    cout<<s1+s2<<endl;
    cout<<s1[0]<<endl;
    
    char c1 = s1[0];
    char c2 = s2[0];
    s1[0]=c2;
    s2[0]=c1;
    cout<<s1<<" "<<s2;

    
    
  
    return 0;
}