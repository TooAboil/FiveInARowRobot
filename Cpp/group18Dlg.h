// group18Dlg.h : header file
//

#if !defined(AFX_GROUP18DLG_H__601F8C2C_2760_4B38_B810_44A95DBAB01C__INCLUDED_)
#define AFX_GROUP18DLG_H__601F8C2C_2760_4B38_B810_44A95DBAB01C__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CGroup18Dlg dialog

class CGroup18Dlg : public CDialog
{
// Construction
public:
	CGroup18Dlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	//{{AFX_DATA(CGroup18Dlg)
	enum { IDD = IDD_GROUP18_DIALOG };
	UINT	m_COMNUM;
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CGroup18Dlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CGroup18Dlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnZaxisUp();
	afx_msg void OnZaxisDown();
	afx_msg void OnClawTurn0();
	afx_msg void OnClawTurn1();
	afx_msg void OnStop();
	afx_msg void OnArm0turn0();
	afx_msg void OnArm0turn1();
	afx_msg void OnArm1turn0();
	afx_msg void OnArm1turn1();
	afx_msg void OnButton1();
	virtual void OnOK();
	afx_msg void OnTimer(UINT nIDEvent);
	afx_msg void OnButton2();
	afx_msg void OnButton3();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_GROUP18DLG_H__601F8C2C_2760_4B38_B810_44A95DBAB01C__INCLUDED_)
