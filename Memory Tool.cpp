// Memory Tool.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <stdlib.h>
#include <Windows.h>
#include <time.h>
using namespace std;

DWORD WINAPI DumpHandler(LPVOID lpParam) {
	time_t timer;
	system("winpmem_2.0.1 -o output_test1.aff4");
	//cout << "winpmem_2.0.1 -o output" << time(&timer) << ".aff4";
	return 0;
}

DWORD WINAPI Analyser(LPVOID lpParam) {
	cout << "Thread 2 reporting in!" << "\n";

	return 0;
}

int _tmain(int argc, _TCHAR* argv[])
{
	DWORD dwThreads[2];
	HANDLE hThreads[2];

	hThreads[0] = CreateThread(NULL, 0, DumpHandler, NULL, 0, &dwThreads[0]);
	hThreads[1] = CreateThread(NULL, 0, Analyser, NULL, 0, &dwThreads[1]);

	for (int i = 0; i < 2; i++) {
		if (hThreads[i] == NULL) {
			cout << "Error creating thread " << i << "\n";
		}
	}

	WaitForMultipleObjects(2, hThreads, TRUE, INFINITE);

	CloseHandle(hThreads[0]);
	CloseHandle(hThreads[1]);

	return 0;
}

