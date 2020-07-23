using System;
using System.Runtime.InteropServices;

namespace DotNetCoreComServer
{

    [ComVisible(true)]
    [Guid("00000000-0000-0000-C0C0-000000000003")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    public interface IDotNetCoreComServer
    {
        void SayHello();
    }
}
