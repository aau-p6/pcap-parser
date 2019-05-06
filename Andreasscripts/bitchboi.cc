/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2009 The Boeing Company
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

// This script configures two nodes on an 802.11b physical layer, with
// 802.11b NICs in adhoc mode, and by default, sends one packet of 1000
// (application) bytes to the other node.  The physical layer is configured
// to receive at a fixed RSS (regardless of the distance and transmit
// power); therefore, changing position of the nodes has no effect.
//
// There are a number of command-line options available to control
// the default behavior.  The list of available command-line options
// can be listed with the following command:
// ./waf --run "wifi-simple-adhoc --help"
//
// For instance, for this configuration, the physical layer will
// stop successfully receiving packets when rss drops below -97 dBm.
// To see this effect, try running:
//
// ./waf --run "wifi-simple-adhoc --rss=-97 --numPackets=20"
// ./waf --run "wifi-simple-adhoc --rss=-98 --numPackets=20"
// ./waf --run "wifi-simple-adhoc --rss=-99 --numPackets=20"
//
// Note that all ns-3 attributes (not just the ones exposed in the below
// script) can be changed at command line; see the documentation.
//
// This script can also be helpful to put the Wifi layer into verbose
// logging mode; this command will turn on all wifi logging:
//
// ./waf --run "wifi-simple-adhoc --verbose=1"
//
// When you are done, you will notice two pcap trace files in your directory.
// If you have tcpdump installed, you can try this:
//
// tcpdump -r wifi-simple-adhoc-0-0.pcap -nn -tt
//
#include <chrono>
#include <fstream>
#include <iostream>
#include "ns3/command-line.h"
#include "ns3/config.h"
#include "ns3/double.h"
#include "ns3/string.h"
#include "ns3/log.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/mobility-helper.h"
#include "ns3/ipv4-address-helper.h"
#include "ns3/yans-wifi-channel.h"
#include "ns3/mobility-model.h"
#include "ns3/internet-stack-helper.h"
#include "ns3/network-module.h"
#include "ns3/aodv-module.h"
#include "ns3/olsr-module.h"
#include "ns3/dsdv-module.h"
#include "ns3/aodv-module.h"
#include "ns3/applications-module.h"
#include "ns3/pointer.h"
#include "ns3/olsr-helper.h"
#include "ns3/aodv-helper.h"
#include "ns3/uinteger.h"
#include "ns3/ipv4-static-routing-helper.h"
#include "ns3/ipv4-list-routing-helper.h"
#include <iostream>
#include <fstream>
#include <ctime>
#include <iomanip>
#include "ns3/flow-monitor-helper.h"
auto T1=0;
auto T2=0;
auto now = 0;
using namespace ns3;
NS_LOG_COMPONENT_DEFINE ("WifiSimpleAdhoc");
using namespace std;
int GTC = 0;
/*static void 
CourseChange (std::string foo, Ptr<const MobilityModel> mobility)
{
  Vector pos = mobility->GetPosition ();
  Vector vel = mobility->GetVelocity ();
  std::cout << Simulator::Now () << ", model=" << mobility << ", POS: x=" << pos.x << ", y=" << pos.y
            << ", z=" << pos.z << "; VEL:" << vel.x << ", y=" << vel.y
            << ", z=" << vel.z << std::endl;
}*/
vector<Ptr<Socket>> VectorSource;

void ReceivePacket (Ptr<Socket> socket)
{
  while (socket->Recv ())
    {
      NS_LOG_UNCOND ("Received one packet!");
      
    }
}


 static void GenerateTrafficChild (Ptr<Socket> socket, uint32_t pktSize,
                             int pktCount, Time pktInterval)
{
    std::chrono::system_clock::time_point tid = std::chrono::system_clock::now();
    auto temp = tid.time_since_epoch();
    auto Millis = std::chrono::duration_cast<std::chrono::microseconds>(temp).count();
    srand(Millis);
    int v = rand() % VectorSource.size();
    socket = VectorSource[v];
    //NS_LOG_UNCOND(socket->GetNode()->GetId());
    socket = VectorSource[v];
    double Tid =(rand() % 15 + 5)/10;
    Time interPacketInterval = Seconds (Tid);
    pktInterval = interPacketInterval;
    if(pktCount > 0){
      socket->Send (Create<Packet> (pktSize));
      //NS_LOG_UNCOND ("Sending one packet!fgt");
      //NS_LOG_UNCOND (pktCount);
      Simulator::Schedule (pktInterval, &GenerateTrafficChild,
                           socket, pktSize,pktCount - 1, pktInterval);
      
      //NS_LOG_UNCOND ("Sending one packet!");
    }
  else
    { 
      socket->Close ();
    }
    
}


static void GenerateTraffic (Ptr<Socket> socket, uint32_t pktSize,
                             int pktCount, Time pktInterval)
{
    
    std::chrono::system_clock::time_point tid = std::chrono::system_clock::now();
    auto temp = tid.time_since_epoch();
    auto Millis = std::chrono::duration_cast<std::chrono::microseconds>(temp).count();
    srand(Millis);
    int v = rand() % VectorSource.size();
    socket = VectorSource[v];
    socket = VectorSource[v];
    if(pktCount > 0){
      socket->Send (Create<Packet> (pktSize));
      string info = "We still goin stronk  " + to_string(pktCount);

      //NS_LOG_UNCOND ("Sending one packet!");
      NS_LOG_UNCOND (info);
      double Tid =(rand() % 15 + 5)/10;
      Time interPacketInterval = Seconds (Tid);
      pktInterval = interPacketInterval;
      Simulator::Schedule (pktInterval, &GenerateTraffic,
                           socket, pktSize,pktCount - 1, pktInterval);
      if (GTC < 2){
          GTC ++;
      Simulator::Schedule (pktInterval, &GenerateTrafficChild,
                           socket, pktSize,pktCount - 1, pktInterval);
      //NS_LOG_UNCOND ("Spawner et nyt monster");
      }
      
      //NS_LOG_UNCOND ("Sending one packet!");
    }
  else
    {
      
      socket->Close ();
    }
    
}





int main (int argc, char *argv[])
{
  std::string phyMode ("DsssRate1Mbps");
  //double rss = -90;  // -dBm
  uint32_t packetSize = 1000; // bytes
  uint32_t numPackets = 30;
  uint32_t sinkNode = 0; // Node der modtager (Gateway)
  uint32_t sourceNode = 1;
  uint32_t numNodes = 20;
  double interval = 1.0; // seconds mellem hver pakke sendes
  bool verbose = false;
  bool tracing = true;
  int nodeSpeed = 20;
  int nodePause = 0;
  string File_name = "OLSR";
  int Run_number = 1;

  
  /*Config::SetDefault ("ns3::RandomWalk2dMobilityModel::Mode", StringValue ("Time"));
  Config::SetDefault ("ns3::RandomWalk2dMobilityModel::Time", StringValue ("2s"));
  Config::SetDefault ("ns3::RandomWalk2dMobilityModel::Speed", StringValue ("ns3::ConstantRandomVariable[Constant=1.0]"));
  Config::SetDefault ("ns3::RandomWalk2dMobilityModel::Bounds", StringValue ("0|200|0|200"));
*/
  
  CommandLine cmd;
  cmd.AddValue ("phyMode", "Wifi Phy mode", phyMode);
  //cmd.AddValue ("rss", "received signal strength", rss);
  cmd.AddValue ("packetSize", "size of application packet sent", packetSize);
  cmd.AddValue ("numPackets", "number of packets generated", numPackets);
  cmd.AddValue ("interval", "interval (seconds) between packets", interval);
  cmd.AddValue ("verbose", "turn on all WifiNetDevice log components", verbose);
  cmd.AddValue ("numNodes", "number of nodes", numNodes);
  cmd.AddValue ("sinkNode", "Receiver node number", sinkNode);
  cmd.AddValue ("sourceNode", "Sender node number", sourceNode);
  cmd.AddValue ("File_name","Filens navn", File_name);
  cmd.AddValue ("Run_number", "Hvilket run vi er ved", Run_number);
  cmd.Parse (argc, argv);
  // Convert to time object
  Time interPacketInterval = Seconds (interval);

  // Fix non-unicast data rate to be the same as that of unicast
  Config::SetDefault ("ns3::WifiRemoteStationManager::NonUnicastMode",
                      StringValue (phyMode));

  NodeContainer c;
  c.Create (numNodes);

  // The below set of helpers will help us to put together the wifi NICs we want
  WifiHelper wifi;
  if (verbose)
    {
      wifi.EnableLogComponents ();  // Turn on all Wifi logging
    }
  wifi.SetStandard (WIFI_PHY_STANDARD_80211b);

  YansWifiPhyHelper wifiPhy =  YansWifiPhyHelper::Default ();
  // This is one parameter that matters when using FixedRssLossModel
  // set it to zero; otherwise, gain will be added
  wifiPhy.Set ("RxGain", DoubleValue (-10) );
  // ns-3 supports RadioTap and Prism tracing extensions for 802.11b
  wifiPhy.SetPcapDataLinkType (WifiPhyHelper::DLT_IEEE802_11_RADIO);

  YansWifiChannelHelper wifiChannel;
  wifiChannel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
  // The below FixedRssLossModel will cause the rss to be fixed regardless
  // of the distance between the two stations, and the transmit power
  //wifiChannel.AddPropagationLoss ("ns3::FixedRssLossModel","Rss",DoubleValue (rss));
  wifiChannel.AddPropagationLoss ("ns3::FriisPropagationLossModel");
  wifiPhy.SetChannel (wifiChannel.Create ());

  // Add a mac and disable rate control
  WifiMacHelper wifiMac;
  wifi.SetRemoteStationManager ("ns3::ConstantRateWifiManager",
                                "DataMode",StringValue (phyMode),
                                "ControlMode",StringValue (phyMode));
  // Set it to adhoc mode
  wifiMac.SetType ("ns3::AdhocWifiMac");
  NetDeviceContainer devices = wifi.Install (wifiPhy, wifiMac, c);

  // Note that with FixedRssLossModel, the positions below are not
  // used for received signal strength.
  MobilityHelper mobility;
  int64_t streamIndex = 0;
/*  mobility.SetPositionAllocator ("ns3::RandomDiscPositionAllocator",
                                 "X", StringValue ("100.0"),
                                 "Y", StringValue ("100.0"),
                                 "Rho", StringValue ("ns3::UniformRandomVariable[Min=0|Max=100]"));
  mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                             "Mode", StringValue ("Time"),
                             "Time", StringValue ("5s"),
                             "Speed", StringValue ("ns3::ConstantRandomVariable[Constant=1.0]"),
                             "Bounds", StringValue ("0|200|0|200"));
  mobility.InstallAll ();
  */
  //Config::Connect ("/NodeList/*/$ns3::MobilityModel/CourseChange",
  //                 MakeCallback (&CourseChange));

  ObjectFactory pos;
  pos.SetTypeId ("ns3::RandomRectanglePositionAllocator");
  pos.Set ("X", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=1500.0]"));
  pos.Set ("Y", StringValue ("ns3::UniformRandomVariable[Min=0.0|Max=1500.0]"));

  Ptr<PositionAllocator> taPositionAlloc = pos.Create ()->GetObject<PositionAllocator> ();
  streamIndex += taPositionAlloc->AssignStreams (streamIndex);

  std::stringstream ssSpeed;
  ssSpeed << "ns3::UniformRandomVariable[Min=0.0|Max=" << nodeSpeed << "]";
  std::stringstream ssPause;
  ssPause << "ns3::ConstantRandomVariable[Constant=" << nodePause << "]";
  mobility.SetMobilityModel ("ns3::RandomWaypointMobilityModel",
                                  "Speed", StringValue (ssSpeed.str ()),
                                  "Pause", StringValue (ssPause.str ()),
                                  "PositionAllocator", PointerValue (taPositionAlloc));
  mobility.SetPositionAllocator (taPositionAlloc);
  mobility.Install (c);
  streamIndex += mobility.AssignStreams (c, streamIndex);
  NS_UNUSED (streamIndex);
  
  OlsrHelper aodv;
  Ipv4StaticRoutingHelper StaticRouting;
  
  Ipv4ListRoutingHelper list;
  list.Add (StaticRouting, 0);
  list.Add (aodv,10);
  aodv::RoutingProtocol testing;
  
  InternetStackHelper internet;
  internet.SetRoutingHelper (list); // has effect on the next Install ()
  internet.Install (c);

  Ipv4AddressHelper ipv4;
  NS_LOG_INFO ("Assign IP Addresses.");
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer i = ipv4.Assign (devices);

  TypeId tid = TypeId::LookupByName ("ns3::UdpSocketFactory");
  
  
  Ptr<Socket> recvSink = Socket::CreateSocket (c.Get (sinkNode), tid);
  InetSocketAddress local = InetSocketAddress (Ipv4Address::GetAny (), 80);
  recvSink->Bind (local);
  recvSink->SetRecvCallback (MakeCallback (&ReceivePacket));
  
  
  
  for (uint32_t v = 1; v < numNodes; v++){
  Ptr<Socket> SamletSource = Socket::CreateSocket (c.Get (v), tid);
  InetSocketAddress remote = InetSocketAddress (i.GetAddress (sinkNode, 0), 80);
  //InetSocketAddress remote = InetSocketAddress (Ipv4Address ("255.255.255.255"), 80);
  //source->SetAllowBroadcast (true);
  SamletSource->Connect (remote);
  
  VectorSource.push_back(SamletSource);
  }
  
  Ptr<Socket> source = VectorSource[sourceNode]; 
    Simulator::ScheduleWithContext (source->GetNode ()->GetId (),
                                 Seconds (1.0), &GenerateTraffic,
                                 source, packetSize, numPackets, interPacketInterval); 
    
//NS_LOG_UNCOND(book);
    
  if (tracing == true)
    {
      AsciiTraceHelper ascii;
      wifiPhy.EnableAsciiAll (ascii.CreateFileStream ("wifi-simple-adhoc-grid.tr"));
      //wifiPhy.EnablePcap ("wifi-simple-adhoc-grid", devices);
      // Trace routing tables
      //Ptr<OutputStreamWrapper> routingStream = Create<OutputStreamWrapper> ("wifi-simple-adhoc-grid.routes", std::ios::out);
      //aodv.PrintRoutingTableAllEvery (Seconds (2), routingStream);
      //Ptr<OutputStreamWrapper> neighborStream = Create<OutputStreamWrapper> ("wifi-simple-adhoc-grid.neighbors", std::ios::out);
      //aodv.PrintNeighborCacheAllEvery (Seconds (2), neighborStream);

      // To do-- enable an IP-level trace that shows forwarding events only
    }

  // Tracing
  string pcap = File_name + "/wifi-simple-adhoc";
  wifiPhy.EnablePcap (pcap, devices);
  
  // Give OLSR time to converge-- 30 seconds perhaps
 // Simulator::Schedule (Seconds (30.0), &GenerateTraffic,
   //                    source, packetSize, numPackets, interPacketInterval);

  // Output what we are doing
  //NS_LOG_UNCOND ("Testing " << numPackets  );//<< " packets sent with receiver rss " << rss );
  //NS_LOG_UNCOND("Here it goes");
  //NS_LOG_UNCOND(typeid(source).name());
  //NS_LOG_UNCOND("here it was ");
  // Bruges til at sende pakker


//Source er en pointer til noden
// source->.... er node nummeret 
  string xml = File_name  + "/OLSR.xml";  
  Ptr<FlowMonitor> flowMonitor;
  FlowMonitorHelper flowHelper;
  flowMonitor = flowHelper.InstallAll();
  
    
  Simulator::Stop (Seconds (30.0));
  Simulator::Run ();
  flowMonitor->SerializeToXmlFile(xml, true, true);
  //flowMonitor->SerializeToXmlFile("OLSRResults/Aodvtest.xml", true, true);
  Simulator::Destroy ();

  return 0;
}



