extern "C" _declspec(dllexport)void KLD_Set_Unite(int mode);
extern "C" _declspec(dllexport)int KLD_Get_Unite();
extern "C" _declspec(dllexport)void Set_Base_Address(unsigned int Address);
extern "C" _declspec(dllexport)unsigned int Read_Base_Address();
extern "C" _declspec(dllexport)void KLD_InitDevice();
extern "C" _declspec(dllexport)unsigned int KLD_ReadLimitPort(int PortNO);
extern "C" _declspec(dllexport)unsigned int KLD_ReadAState(int channel);
extern "C" _declspec(dllexport)unsigned int KLD_ReadState(int channel);
extern "C" _declspec(dllexport)void KLD_Position(int axis, int direction, unsigned long freq, unsigned long pulse_number);
extern "C" _declspec(dllexport)void KLD_Velocity(int axis, int direction, unsigned long freq);
extern "C" _declspec(dllexport)void KLD_Motor_Off(int axis);
extern "C" _declspec(dllexport)unsigned int KLD_ReadCurrentlyFreq(int axis);
extern "C" _declspec(dllexport)void KLD_Hand_Open(unsigned int pulse_number);
extern "C" _declspec(dllexport)void KLD_Hand_Close(unsigned int pulse_number);
extern "C" _declspec(dllexport)unsigned int KLD_ReadBState(int PortNO,int channel);
extern "C" _declspec(dllexport)int Read_CardNo();
extern "C" _declspec(dllexport)int KLD_Card_Test();
extern "C" _declspec(dllexport)unsigned int Read_Card_Category();
extern "C" _declspec(dllexport)unsigned short Read_movement_mode();
extern "C" _declspec(dllexport)void Set_movement_mode(unsigned short mode);
extern "C" _declspec(dllexport)void SetMotorPID(int axis, long P,long I,long D);
extern "C" _declspec(dllexport)void Sevon_Output(int channel, int m_direction, long freq, long pulse_number);
extern "C" _declspec(dllexport)unsigned int ReadSta(int channel);
extern "C" _declspec(dllexport) unsigned long ReadPos(int channel);
