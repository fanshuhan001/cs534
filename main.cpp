#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
 
using namespace std;

 
struct Employee
{
    string id;
    string name;
    string bio;
    string mid;
};

string Trim(string& str)
{
	//str.find_first_not_of(" \t\r\n"),在字符串str中从索引0开始，返回首次不匹配"\t\r\n"的位置
	str.erase(0,str.find_first_not_of(" \t\r\n"));
	str.erase(str.find_last_not_of(" \t\r\n") + 1);
	return str;
}
 
typedef unordered_map<string, Employee> strmap;
strmap employeemap;

int main()
{
	ifstream fin("Employee.csv"); //打开文件流操作
	string line; 
    ofstream outFile;
    outFile.open("EmployeeIndex.csv", ios::app);
	Employee aEmployee;
	
	while (getline(fin, line))   //整行读取，换行符“\n”区分，遇到文件尾标志eof终止读取
	{
		istringstream sin(line); 
		vector<string> fields;
		string field;
		while (getline(sin, field, ',')) 
		{
			fields.push_back(field);
		}
		aEmployee.id = Trim(fields[0]); 
		aEmployee.name = Trim(fields[1]); 
        aEmployee.bio = Trim(fields[2]); 
        aEmployee.mid = Trim(fields[3]); 

        std::pair<std::string, Employee> amap (aEmployee.id,aEmployee);
        employeemap.insert(amap);

        strmap::hasher fn = employeemap.hash_function();
        int index = fn(aEmployee.id);
        outFile << index << endl; //write index into target file
	}
    
	char flag = 'r';
	char model = 'l';
	int m = 0;
	while (flag != 's') 
	{
		cout << "input 's' to stop\n";
		if (model == 'L' || model == 'l')
		{
			
			if (m == 0) { cout << "now you are in lookup mode, you can switch to Create index mode by input L/l\n"; m = 1; }
			std::string input;
			std::cout << " please input an employee's id to search.\n ID?:\t";
			getline(std::cin, input);
			strmap::const_iterator got = employeemap.find(input);

			if (got == employeemap.end())
				std::cout << "not found"<<endl;
			else
				std::cout << got->second.id << "\t" << got->second.name << "\t" << got->second.bio << "\t" << got->second.mid << endl;
		}
		if (model == 'C' || model == 'c')
		{
			if (m == 1) { cout << "now you are in Create index mode , you can switch to lookup modeby input C/c\n"; m = 0; }
			string input;
			std::cout << "now you are in index creation mode, please input an employee's info to create index for him/her.\n";
			cout << "id: ";
			getline(std::cin, input);
			aEmployee.id = input;
			cout << "name: ";
			getline(std::cin, input);
			aEmployee.name = input;
			cout << "bio: ";
			getline(std::cin, input);
			aEmployee.bio = input;
			cout << "managerID: " << endl;
			getline(std::cin, input);
			aEmployee.mid = input;

			std::pair<std::string, Employee> amap(aEmployee.id, aEmployee);
			employeemap.insert(amap);

			strmap::hasher fn = employeemap.hash_function();
			int index = fn(aEmployee.id);
			outFile << index << endl; //write index into target file
		}
		char temp = model;
		if (model == 's') {break; }
		cout << "please input an command."<< endl;
		model = cin.get();
		cin.ignore(numeric_limits<std::streamsize>::max(), '\n');
		if (model != 's' && model != 'c'&& model != 'C'&& model != 'l'&& model != 'L') { model = temp; }
	}

    outFile.close();
	return EXIT_SUCCESS;
}
