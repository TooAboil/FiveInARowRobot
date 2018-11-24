// group18.h : main header file for the GROUP18 application
//

#if !defined(AFX_GROUP18_H__5026BF01_B33A_4EE7_AE98_A509C2B1AC4E__INCLUDED_)
#define AFX_GROUP18_H__5026BF01_B33A_4EE7_AE98_A509C2B1AC4E__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols

/////////////////////////////////////////////////////////////////////////////
// CGroup18App:
// See group18.cpp for the implementation of this class
//

class CGroup18App : public CWinApp
{
public:
	CGroup18App();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CGroup18App)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation

	//{{AFX_MSG(CGroup18App)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_GROUP18_H__5026BF01_B33A_4EE7_AE98_A509C2B1AC4E__INCLUDED_)
