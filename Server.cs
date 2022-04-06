using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using System.Threading;
using UnityEngine.UI;
//using System.Collections.Concurrent;

public class Client2Text : MonoBehaviour
{
    Thread mThread;
    public string connectionIP = "127.0.0.0";
    public int connectionPort = 9999;
    IPAddress localAdd;
    TcpListener listener;
    TcpClient client;
    //[SerializeField] UnityEngine.UI.
    public Text Thistext;
    public Text OpeningText;
    bool running;
    //ConcurrentQueue<string> m_queuedLogs = new ConcurrentQueue<string>();


    void Start()
    {
        ThreadStart ts = new ThreadStart(GetInfo);
        mThread = new Thread(ts);
        mThread.Start();
    }

    // void Update()
    // {
    //     SendAndReceiveData();

    // }

    void GetInfo()
    {
        localAdd = IPAddress.Parse(connectionIP);
        listener = new TcpListener(IPAddress.Any, connectionPort);
        listener.Start();

        client = listener.AcceptTcpClient();

        running = true;
        while (running)
        {
            SendAndReceiveData();
        }
        listener.Stop();
    }

    void SendAndReceiveData()
    {
        NetworkStream nwStream = client.GetStream();
        byte[] buffer = new byte[client.ReceiveBufferSize];
        
        UnityMainThread.wkr.AddJob(() => 
        {
            OpeningText.text = "Motion Sensor is Active\nDistance Sensor is Acrive";  
        });

        

        //---receiving Data from the Host----
        int bytesRead = nwStream.Read(buffer, 0, client.ReceiveBufferSize); //Getting data in Bytes from Python
        string dataReceived = Encoding.ASCII.GetString(buffer, 0, bytesRead); //Converting byte data to string

        if (dataReceived != null)
        {
            //Update();//---Sending Data to Host----
            byte[] myWriteBuffer = Encoding.ASCII.GetBytes("Message"); //Converting string to byte data
            nwStream.Write(myWriteBuffer, 0, myWriteBuffer.Length);
            UnityMainThread.wkr.AddJob(() => 
            {
            // Will run on main thread, hence issue is solved
                Thistext.text = dataReceived;
                // Thistext.text + assigning receivedPos in SendAndReceiveData() //Sending the data in Bytes to Python      
            });
            //SendAndReceiveData();

        }
    }
    
    
}
