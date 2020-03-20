
// MourseButtonDlg.cpp : 实现文件
//

#include "stdafx.h"
#include "MourseButton.h"
#include "MourseButtonDlg.h"
#include "afxdialogex.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

#define GAT_F1 WM_USER+1
#define GAT_F2 WM_USER+2
#define GAT_F3 WM_USER+3
#define GAT_F4 WM_USER+4
#define GAT_F5 WM_USER+5

// 用于应用程序“关于”菜单项的 CAboutDlg 对话框

class CAboutDlg : public CDialogEx
{
public:
	CAboutDlg();

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_ABOUTBOX };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV 支持

// 实现
protected:
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialogEx(IDD_ABOUTBOX)
{
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialogEx::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialogEx)

END_MESSAGE_MAP()


// CMourseButtonDlg 对话框



CMourseButtonDlg::CMourseButtonDlg(CWnd* pParent /*=NULL*/)
	: CDialogEx(IDD_MOURSEBUTTON_DIALOG, pParent)
    , m_cbWhile(FALSE)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CMourseButtonDlg::DoDataExchange(CDataExchange* pDX)
{
    CDialogEx::DoDataExchange(pDX);
    DDX_Control(pDX, BT_RECORD, m_edtInfo);
    DDX_Check(pDX, CB_WHILE, m_cbWhile);
}

BEGIN_MESSAGE_MAP(CMourseButtonDlg, CDialogEx)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()

    ON_MESSAGE(WM_HOTKEY, OnHotKey)
    ON_BN_CLICKED(BT_RECORD, &CMourseButtonDlg::OnBnClickedRecord)
    ON_BN_CLICKED(BT_CLEAR, &CMourseButtonDlg::OnBnClickedClear)
END_MESSAGE_MAP()


// CMourseButtonDlg 消息处理程序

BOOL CMourseButtonDlg::OnInitDialog()
{
	CDialogEx::OnInitDialog();
    m_hButton = NULL;
    m_dwThreadId = 0;
    SetDlgItemInt(EDT_SLEEP, 1000, FALSE);
    SetDlgItemInt(EDT_X, 0, FALSE);
    SetDlgItemInt(EDT_Y, 0, FALSE);

    RegisterHotKey(this->GetSafeHwnd(), GAT_F1, MOD_CONTROL, VK_F1);
    RegisterHotKey(this->GetSafeHwnd(), GAT_F2, MOD_CONTROL, VK_F2);
    RegisterHotKey(this->GetSafeHwnd(), GAT_F3, MOD_CONTROL, VK_F3);
    RegisterHotKey(this->GetSafeHwnd(), GAT_F4, MOD_CONTROL, VK_F4);
    RegisterHotKey(this->GetSafeHwnd(), GAT_F5, MOD_CONTROL, VK_F5);
	// 将“关于...”菜单项添加到系统菜单中。

	// IDM_ABOUTBOX 必须在系统命令范围内。
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		BOOL bNameValid;
		CString strAboutMenu;
		bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
		ASSERT(bNameValid);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// 设置此对话框的图标。  当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标

	// TODO: 在此添加额外的初始化代码

	return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
}

void CMourseButtonDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialogEx::OnSysCommand(nID, lParam);
	}
}

// 如果向对话框添加最小化按钮，则需要下面的代码
//  来绘制该图标。  对于使用文档/视图模型的 MFC 应用程序，
//  这将由框架自动完成。

void CMourseButtonDlg::OnPaint()
{
	if (IsIconic())
	{
		CPaintDC dc(this); // 用于绘制的设备上下文

		SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);

		// 使图标在工作区矩形中居中
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// 绘制图标
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialogEx::OnPaint();
	}
}

//当用户拖动最小化窗口时系统调用此函数取得光标
//显示。
HCURSOR CMourseButtonDlg::OnQueryDragIcon()
{
	return static_cast<HCURSOR>(m_hIcon);
}

DWORD WINAPI OnClicking(LPVOID lpParam)
{

    CMourseButtonDlg *pCMB = (CMourseButtonDlg *)lpParam;

    if (pCMB->m_cbWhile)
    {
        while (true)
        {
            POSITION pos = pCMB->m_lstPoint.GetHeadPosition();
            while (pos != NULL)
            {
                CPoint poinr = pCMB->m_lstPoint.GetNext(pos);
                SetCursorPos(poinr.x, poinr.y);//移动到某点坐标
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);//点下左键
                mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);//松开左键
                Sleep(pCMB->m_dwSleep); //等待延时
            }
        }
    }
    else
    {
        POSITION pos = pCMB->m_lstPoint.GetHeadPosition();
        while (pos != NULL)
        {
            CPoint poinr = pCMB->m_lstPoint.GetNext(pos);
            SetCursorPos(poinr.x, poinr.y);//移动到某点坐标
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);//点下左键
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);//松开左键
            Sleep(pCMB->m_dwSleep); //等待延时
        }
    }
    

    pCMB->m_hButton = NULL;
    pCMB->m_dwThreadId = 0;
    //CString csEditInfo = NULL;
    //CEdit cedt = (CEdit)GetDlgItem(pCMB->GetSafeHwnd(), EDT_INFO);
    //GetDlgItem(EDT_INFO)->GetWindowText(csEditInfo);
    //csEditInfo += "结束点击\r\n";
    //GetDlgItem(EDT_INFO)->SetWindowText(csEditInfo);
    return 0;
}

void CMourseButtonDlg::StartMouseClick()
{
    //F1开始
    UpdateData(TRUE);
    m_dwSleep = GetDlgItemInt(EDT_SLEEP, NULL, FALSE);
    if (m_hButton == NULL && !m_lstPoint.IsEmpty())
    {
        CString csEditInfo = NULL;
        GetDlgItem(EDT_INFO)->GetWindowText(csEditInfo);
        csEditInfo += "开始点击\r\n";
        GetDlgItem(EDT_INFO)->SetWindowText(csEditInfo);

        m_hButton = CreateThread(
            NULL,                        // no security attributes 
            0,                           // use default stack size  
            OnClicking,                  // thread function 
            this,          // argument to thread function 
            0,                           // use default creation flags 
            &m_dwThreadId);                // returns the thread identifier 
                                         // Check the return value for success. 
    }
}


void CMourseButtonDlg::StopMouseClick()
{
    //F2结束
    if (m_dwThreadId != 0 && m_hButton != NULL)
    {
        TerminateThread(m_hButton, 0);
        m_hButton = NULL;
        CString csEditInfo = NULL;
        GetDlgItem(EDT_INFO)->GetWindowText(csEditInfo);
        csEditInfo += "结束点击\r\n";
        GetDlgItem(EDT_INFO)->SetWindowText(csEditInfo);
    }
}


void CMourseButtonDlg::GetMousePointerAsScreen()
{
    //F3获取当前鼠标位置
    CPoint point;
    GetCursorPos(&point);
    CString csPointInfo = NULL;
    csPointInfo.Format("x = %d, y = %d\r\n", point.x, point.y);
    CString csEditInfo = NULL;
    GetDlgItem(EDT_INFO)->GetWindowText(csEditInfo);
    csEditInfo += csPointInfo;
    GetDlgItem(EDT_INFO)->SetWindowText(csEditInfo);
    //设置文本框的作弊
    SetDlgItemInt(EDT_X, point.x, FALSE);
    SetDlgItemInt(EDT_Y, point.y, FALSE);

}


LONG CMourseButtonDlg::OnHotKey(WPARAM wPARAM, LPARAM lPARAM)
{
    if (wPARAM == GAT_F1)
    {
        StartMouseClick();
    }
    if (wPARAM == GAT_F2)
    {
        StopMouseClick();
    }
    if (wPARAM == GAT_F3)
    {
        GetMousePointerAsScreen();
    }
    if (wPARAM == GAT_F4)
    {
        OnBnClickedRecord();
    }
    if (wPARAM == GAT_F5)
    {
        OnBnClickedClear();
    }

    return 0;
}

void CMourseButtonDlg::OnBnClickedRecord()
{
    //记录一个点击事件
    CPoint point;
    CString csInfo;
    CString csEditInfo = NULL;

    point.x = GetDlgItemInt(EDT_X, NULL, FALSE);
    point.y = GetDlgItemInt(EDT_Y, NULL, FALSE);
    m_lstPoint.AddTail(point);
    csInfo.Format("记录位置,x = %d, y = %d\r\n", point.x, point.y);
    GetDlgItem(EDT_INFO)->GetWindowText(csEditInfo);
    csEditInfo += csInfo;
    GetDlgItem(EDT_INFO)->SetWindowText(csEditInfo);
}

void CMourseButtonDlg::OnBnClickedClear()
{
    //清空点击事件
    m_lstPoint.RemoveAll();
    CString csEditInfo = NULL;
    GetDlgItem(EDT_INFO)->GetWindowText(csEditInfo);
    csEditInfo += "清空记录\r\n";
    GetDlgItem(EDT_INFO)->SetWindowText(csEditInfo);
}
