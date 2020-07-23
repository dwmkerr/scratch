using System;
using System.Runtime.InteropServices;

namespace DotNetCoreComServer
{
    [ComVisible(true)]
    [Guid("00000000-0000-0000-C0C0-000000000003")]
    public class DotNetCoreComServer : IDotNetCoreComServer
    {
        public void SayHello()
        {
            Console.WriteLine("Hello");
        }
    }
}