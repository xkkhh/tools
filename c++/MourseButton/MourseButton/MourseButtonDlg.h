
// MourseButtonDlg.h : 头文件
//

#pragma once
#include "afxwin.h"


// CMourseButtonDlg 对话框
class CMourseButtonDlg : public CDialogEx
{
// 构造
public:
	CMourseButtonDlg(CWnd* pParent = NULL);	// 标准构造函数

// 对话框数据
#ifdef AFX_DESIGN_TIME
	enum { IDD = IDD_MOURSEBUTTON_DIALOG };
#endif

	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV 支持


// 实现
protected:
	HICON m_hIcon;

	// 生成的消息映射函数
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	DECLARE_MESSAGE_MAP()
public:
    afx_msg void StartMouseClick();
    afx_msg void StopMouseClick();
    afx_msg void GetMousePointerAsScreen();
    afx_msg LONG OnHotKey(WPARAM wPARAM, LPARAM lPARAM);
    afx_msg void OnBnClickedRecord();
    afx_msg void OnBnClickedClear();
public:
    HANDLE m_hButton;
    DWORD m_dwThreadId;
    CList<CPoint> m_lstPoint; //记录链表
    DWORD m_dwSleep;
    CButton m_edtInfo;
    BOOL m_cbWhile;
};
