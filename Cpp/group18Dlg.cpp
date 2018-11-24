// group18Dlg.cpp : implementation file
//

#include "stdafx.h"
#include "group18.h"
#include "group18Dlg.h"
#include "Pcomm.h"


#include "WinIo.h"
#include "conio.h"
#include "kld.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

int flag=0;
float tempH,tempL;
char comaH,comaL;

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAboutDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	//{{AFX_MSG(CAboutDlg)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
	//{{AFX_MSG_MAP(CAboutDlg)
		// No message handlers
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CGroup18Dlg dialog

CGroup18Dlg::CGroup18Dlg(CWnd* pParent /*=NULL*/)
	: CDialog(CGroup18Dlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CGroup18Dlg)
	m_COMNUM = 0;
	//}}AFX_DATA_INIT
	// Note that LoadIcon does not require a subsequent DestroyIcon in Win32
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CGroup18Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CGroup18Dlg)
	DDX_Text(pDX, IDC_EDIT1, m_COMNUM);
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CGroup18Dlg, CDialog)
	//{{AFX_MSG_MAP(CGroup18Dlg)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_ZAXIS_UP, OnZaxisUp)
	ON_BN_CLICKED(IDC_ZAXIS_DOWN, OnZaxisDown)
	ON_BN_CLICKED(IDC_CLAW_TURN0, OnClawTurn0)
	ON_BN_CLICKED(IDC_CLAW_TURN1, OnClawTurn1)
	ON_BN_CLICKED(IDC_STOP, OnStop)
	ON_BN_CLICKED(IDC_ARM0TURN0, OnArm0turn0)
	ON_BN_CLICKED(IDC_ARM0TURN1, OnArm0turn1)
	ON_BN_CLICKED(IDC_ARM1TURN0, OnArm1turn0)
	ON_BN_CLICKED(IDC_ARM1TURN1, OnArm1turn1)
	ON_BN_CLICKED(IDC_BUTTON1, OnButton1)
	ON_WM_TIMER()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CGroup18Dlg message handlers

BOOL CGroup18Dlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon
	
	// TODO: Add extra initialization here

	InitializeWinIo();
	KLD_InitDevice();
	SetMotorPID(1,0x21,0x09,0x3);
	SetMotorPID(2,0x21,0x09,0x3);


	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CGroup18Dlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CGroup18Dlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, (WPARAM) dc.GetSafeHdc(), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CGroup18Dlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}

void CGroup18Dlg::OnZaxisUp() 
{
	// TODO: Add your control notification handler code here
	KLD_Position(1,0,1600,8000);
}

void CGroup18Dlg::OnZaxisDown() 
{
	// TODO: Add your control notification handler code here
	KLD_Position(1,1,1600,8000);
}

void CGroup18Dlg::OnClawTurn0() 
{
	// TODO: Add your control notification handler code here
	KLD_Position(2,0,800,3200);
}


void CGroup18Dlg::OnClawTurn1() 
{
	// TODO: Add your control notification handler code here
	KLD_Position(2,1,800,3200);
}


void CGroup18Dlg::OnStop() 
{
	// TODO: Add your control notification handler code here
	KLD_Motor_Off(1);
	KLD_Motor_Off(2);
	KLD_Motor_Off(3);
	KLD_Motor_Off(4);
	KLD_Motor_Off(5);
}

void CGroup18Dlg::OnArm0turn0() 
{
	// TODO: Add your control notification handler code here
	Sevon_Output(2,0,1111,1111);
}


void CGroup18Dlg::OnArm0turn1() 
{
	// TODO: Add your control notification handler code here
	Sevon_Output(2,1,1111,1111);
}

void CGroup18Dlg::OnArm1turn0() 
{
	// TODO: Add your control notification handler code here
	Sevon_Output(1,0,1111,1111);
}

void CGroup18Dlg::OnArm1turn1() 
{
	// TODO: Add your control notification handler code here
	Sevon_Output(1,1,1111,1111);
}



void CGroup18Dlg::OnButton1() 
{
	// TODO: Add your control notification handler code here
	UpdateData(TRUE);
	if( sio_open(m_COMNUM)!=0 )
	{
		sio_close(m_COMNUM);
		AfxMessageBox("Cannot open serial port");
	}else
	{
		sio_ioctl(m_COMNUM, B9600, BIT_8|STOP_1|P_NONE);//设置串口号,波特率,数据位,停止位,校验位
		SetTimer(1,500,NULL);//启动定时器1,定时时间是0.5秒,Read data from the driver's input buffer
		SetTimer(2,200,NULL);
	}
	
}



void CGroup18Dlg::OnOK() 
{
	// TODO: Add extra validation here
	sio_close(m_COMNUM);

	CDialog::OnOK();
}

void CGroup18Dlg::OnTimer(UINT nIDEvent) 
{
	// TODO: Add your message handler code here and/or call default
	//定时器程序
	CDialog::OnTimer(nIDEvent);
	char rxdata[512]; //设置BYTE数组 An 8-bit integerthat is not signed	
	char txdata[512];
	char tempH1,tempH2,tempH3,tempH4,tempL1,tempL2,tempL3,tempL4;
	LONG len;
	switch (nIDEvent)
	{
	case 1:
		len = sio_read(m_COMNUM, rxdata, 512);	
		flag=0;
		if (len == 10)
		{
			comaH = rxdata[0]-'0';
			tempH1 = rxdata[1]-'0';//大臂角度十位
			tempH2 = rxdata[2]-'0';//大臂角度个位
			tempH3 = rxdata[3]-'0';//大臂角度十分位
			tempH4 = rxdata[4]-'0';//大臂角度百分位
			comaL = rxdata[5]-'0';
			tempL1 = rxdata[6]-'0';//小臂角度十位
			tempL2 = rxdata[7]-'0';//小臂角度个位
			tempL3 = rxdata[8]-'0';//小臂角度十分位
			tempL4 = rxdata[9]-'0';//小臂角度百分位
			tempH=tempH1*10+tempH2+tempH3*0.1+tempH4*0.01;
			tempL=tempL1*10+tempL2+tempL3*0.1+tempL4*0.01;
			flag=1;
		}
		break;
	case 2:
		if (flag==1)
		{
			flag=0;
			KillTimer(2);
			txdata[0]=66;
			sio_write(m_COMNUM, txdata, 1);
			Sevon_Output(1,!(comaH),15000,int(2222.22*tempH));//机械爪大手臂顺时针
			Sevon_Output(2,comaL,15000,int(2222.22*tempL));//机械爪小手臂顺时针
			_sleep( int( max(2222.22*tempH/15000, 2222.22*tempL/15000) )*1000);
			KLD_Position(1,1,1600,8000);
			_sleep(6000);
			KLD_Position(1,0,1600,8000);
			_sleep(2000);
			Sevon_Output(1,comaH,20000,int(2222.22*tempH));
			Sevon_Output(2,!(comaL),20000,int(2222.22*tempL));
			_sleep( int( max(2222.22*tempH/15000, 2222.22*tempL/15000) )*1000 );
			txdata[0]=67;
			sio_write(m_COMNUM, txdata, 1);	
			SetTimer(2,100,NULL);
			flag=0;
		}
		break;
	}


}


