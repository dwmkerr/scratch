// dllmain.h : Declaration of module class.

class CNativeAtlComServerModule : public ATL::CAtlDllModuleT< CNativeAtlComServerModule >
{
public :
	DECLARE_LIBID(LIBID_NativeAtlComServerLib)
	DECLARE_REGISTRY_APPID_RESOURCEID(IDR_NATIVEATLCOMSERVER, "{00000000-0000-0000-C0C0-000000000001}")
};

extern class CNativeAtlComServerModule _AtlModule;
