#include <windows.h>
#include <stdio.h>

void InjectDLL(DWORD PID,char *Path) 
{
    DWORD dwSize;
    HANDLE hProcess=OpenProcess(PROCESS_ALL_ACCESS,false,PID);
    dwSize=strlen(Path)+1;
    LPVOID lpParamAddress=VirtualAllocEx(hProcess,0,dwSize,PARITY_SPACE,PAGE_EXECUTE_READWRITE);
    WriteProcessMemory(hProcess,lpParamAddress,(PVOID)Path,dwSize,NULL);
    HMODULE hModule=GetModuleHandleA("kernel32.dll");
    LPTHREAD_START_ROUTINE lpStartAddress=(LPTHREAD_START_ROUTINE)GetProcAddress(hModule,"LoadLibraryA");
    HANDLE hThread=CreateRemoteThread(hProcess,NULL,0,lpStartAddress,lpParamAddress,0,NULL);
    WaitForSingleObject(hThread,1000);
    CloseHandle(hThread);
}

int main(int argc, char **argv, char **envp)
{
    if (argc < 3)
    {
        printf("use: GetCommandHistory.exe pid dllpath\r\n");
        return -1;
    }
    int nPid = atoi(argv[1]);
    InjectDLL(nPid, argv[2]);
    return 0;
}
