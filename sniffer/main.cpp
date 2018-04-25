#include <arpa/inet.h>
#include <linux/if_packet.h>
#include <linux/ip.h>
#include <linux/udp.h>
#include <linux/tcp.h>
#include <linux/icmp.h>
#include <net/if.h>
#include <netinet/ether.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#include <iostream>

#include "arphdr.h"
#include "structures.h"
#include "postgresqlcache.h"
#include "utils.h"

#define BUFSIZE 65536

PostgreSQLCache *pc;

void processFrame(unsigned char *buffer, int buflen)
{
    struct ethhdr *eth = (struct ethhdr *)(buffer);
    char source_addr[18];
    char destination_addr[18];
    snprintf(source_addr, 18, "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X", eth->h_source[0], eth->h_source[1], eth->h_source[2], eth->h_source[3], eth->h_source[4], eth->h_source[5]);
    snprintf(destination_addr, 18, "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X", eth->h_dest[0], eth->h_dest[1], eth->h_dest[2], eth->h_dest[3], eth->h_dest[4], eth->h_dest[5]);
    std::string source = std::string(source_addr);
    std::string destination = std::string(destination_addr);
    if(source == "00:00:00:00:00:00" && destination == "00:00:00:00:00:00")
        return;
    pc->counterMutex.lock();
    pc->c->l2_frames++;
    pc->c->l2_traffic += buflen;
    pc->counterMutex.unlock();

    if(eth->h_proto == 0x0608) // ARP
    {
        pc->counterMutex.lock();
        pc->c->l3_traffic += (buflen - sizeof(struct ethhdr));
        pc->c->l3_frames++;
        pc->c->arp++;
        pc->counterMutex.unlock();
        struct arphdr_t *arph = (struct arphdr_t *)(buffer + sizeof(struct ethhdr));
        if(ntohs(arph->htype) == 1 && ntohs(arph->ptype) == 0x0800)
        {
            char sender_mac[18];
            char target_mac[18];
            char sender_ip[16];
            char target_ip[16];
            snprintf(sender_mac, 18, "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X", arph->sha[0], arph->sha[1], arph->sha[2], arph->sha[3], arph->sha[4], arph->sha[5]);
            snprintf(target_mac, 18, "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X", arph->tha[0], arph->tha[1], arph->tha[2], arph->tha[3], arph->tha[4], arph->tha[5]);
            snprintf(sender_ip, 16, "%d.%d.%d.%d", arph->spa[0], arph->spa[1], arph->spa[2], arph->spa[3]);
            snprintf(target_ip, 16, "%d.%d.%d.%d", arph->tpa[0], arph->tpa[1], arph->tpa[2], arph->tpa[3]);

            /*rapidjson::Value sender_hw_val;
            sender_hw_val.SetString(std::string(sender_mac).c_str(), std::string(sender_mac).length(), allocator);
            arp.AddMember("sender_hw", sender_hw_val, allocator);

            rapidjson::Value target_hw_val;
            target_hw_val.SetString(std::string(target_mac).c_str(), std::string(target_mac).length(), allocator);
            arp.AddMember("target_hw", target_hw_val, allocator);

            rapidjson::Value sender_ip_val;
            sender_ip_val.SetString(std::string(sender_ip).c_str(), std::string(sender_ip).length(), allocator);
            arp.AddMember("sender_ip", sender_ip_val, allocator);

            rapidjson::Value target_ip_val;
            target_ip_val.SetString(std::string(target_ip).c_str(), std::string(target_ip).length(), allocator);
            arp.AddMember("target_ip", target_ip_val, allocator);

            rapidjson::Value hw_type_val;
            hw_type_val.SetInt(ntohs(arph->htype));
            arp.AddMember("hw_type", hw_type_val, allocator);

            rapidjson::Value proto_type_val;
            proto_type_val.SetInt(ntohs(arph->ptype));
            arp.AddMember("proto_type", proto_type_val, allocator);

            rapidjson::Value operation_val;
            operation_val.SetInt(ntohs(arph->oper));
            arp.AddMember("operation", operation_val, allocator);*/
        }
    }
    else if(eth->h_proto == 0x0008)
    {
        pc->counterMutex.lock();
        pc->c->l3_traffic += (buflen - sizeof(struct ethhdr));
        pc->c->l3_frames++;
        pc->c->ip++;
        pc->counterMutex.unlock();
        unsigned short iphdrlen;
        struct sockaddr_in source_addr;
        struct sockaddr_in destination_addr;
        struct iphdr *iph = (struct iphdr*) (buffer + sizeof(struct ethhdr));
        iphdrlen =iph->ihl*4;
        memset(&source_addr, 0, sizeof(source_addr));
        source_addr.sin_addr.s_addr = iph->saddr;
        memset(&destination_addr, 0, sizeof(destination_addr));
        destination_addr.sin_addr.s_addr = iph->daddr;

        std::string source_ip = std::string(inet_ntoa(source_addr.sin_addr));
        std::string destination_ip = std::string(inet_ntoa(destination_addr.sin_addr));

        if(iph->protocol == 1)
        {
            pc->counterMutex.lock();
            pc->c->l4_frames++;
            pc->c->l4_traffic += (buflen - sizeof(struct ethhdr) - iphdrlen);
            pc->c->icmp++;
            pc->counterMutex.unlock();
            struct icmphdr *icmph = (struct icmphdr *)(buffer + iphdrlen + sizeof(struct ethhdr));
            ICMPSegment icmp_seg;
            icmp_seg.ip_dst = destination_ip;
            icmp_seg.ip_src = source_ip;
            icmp_seg.timestamp = getCurrentDateTime();
            icmp_seg.type = icmph->type;
            pc->pushICMPSegment(icmp_seg);
        }
        else if(iph->protocol == 6)
        {
            pc->counterMutex.lock();
            pc->c->l4_frames++;
            pc->c->l4_traffic += (buflen - sizeof(struct ethhdr) - iphdrlen);
            pc->c->tcp++;
            pc->counterMutex.unlock();
            struct tcphdr *tcph = (struct tcphdr*) (buffer + iphdrlen + sizeof(struct ethhdr));
            TCPSessionMin tcp_sess_min;
            tcp_sess_min.dst_port = ntohs(tcph->dest);
            tcp_sess_min.ip_dst = destination_ip;
            tcp_sess_min.ip_src = source_ip;
            tcp_sess_min.src_port = ntohs(tcph->source);
            TCPSegment tcp_seg;
            tcp_seg.direction = UNKNOWN;
            tcp_seg.timestamp = getCurrentDateTime();
            tcp_seg.size = buflen - iphdrlen - sizeof(struct ethhdr);
            std::vector<std::string> flags;
            pc->counterMutex.lock();
            if(tcph->ack != 0)
            {
                flags.push_back("ACK");
                pc->c->tcp_ack++;
            }
            if(tcph->psh != 0)
            {
                flags.push_back("PSH");
                pc->c->tcp_psh++;
            }
            if(tcph->rst != 0)
            {
                flags.push_back("RST");
                pc->c->tcp_rst++;
            }
            if(tcph->syn != 0)
            {
                flags.push_back("SYN");
                pc->c->tcp_syn++;
            }
            if(tcph->fin != 0)
            {
                flags.push_back("FIN");
                pc->c->tcp_fin++;
            }
            if(tcph->ack != 0 && tcph->syn != 0)
            {
                pc->c->tcp_synack++;
            }
            pc->counterMutex.unlock();
            tcp_seg.flags = flags;
            pc->pushTCPSegment(tcp_sess_min, tcp_seg);
        }
        else if(iph->protocol == 17)
        {
            pc->counterMutex.lock();
            pc->c->l4_frames++;
            pc->c->l4_traffic += (buflen - sizeof(struct ethhdr) - iphdrlen);
            pc->c->udp++;
            pc->counterMutex.unlock();
            struct udphdr *udph = (struct udphdr*) (buffer + iphdrlen + sizeof(struct ethhdr));
            UDPSegment udp_seg;
            udp_seg.dst_port = ntohs(udph->dest);
            udp_seg.ip_dst = destination_ip;
            udp_seg.ip_src = source_ip;
            udp_seg.size = buflen - iphdrlen - sizeof(struct ethhdr);
            udp_seg.src_port = ntohs(udph->source);
            udp_seg.timestamp = getCurrentDateTime();
            pc->pushUDPSegment(udp_seg);
        }
    }
}

int main(int argc, char *argv[])
{
    int sock_r;
    int buflen;

    if(argc < 2)
    {
        printf("USAGE:\n%s <INTERFACE_NAME>\n", argv[0]);
        exit(1);
    }

    sock_r = socket(PF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if(sock_r < 0)
    {
        perror("error in socket()\n");
        return -1;
    }

    struct ifreq ifr;
    struct sockaddr_ll ll;
    memset(&ifr, 0, sizeof(ifr));
    strncpy(ifr.ifr_name, argv[1], sizeof(ifr.ifr_name));
    if(ioctl(sock_r, SIOCGIFINDEX, &ifr) < 0)
    {
        perror("ioctl[SIOCGIFINDEX]");
        close(sock_r);
        return -1;
    }
    memset(&ll, 0, sizeof(ll));
    ll.sll_family = AF_PACKET;
    ll.sll_ifindex = ifr.ifr_ifindex;
    ll.sll_protocol = htons(ETH_P_ALL);
    if(bind(sock_r, (struct sockaddr *) &ll, sizeof(ll)) < 0)
    {
        perror("bind[AF_PACKET]");
        close(sock_r);
        return -1;
    }
    struct packet_mreq mr;
    memset(&mr, 0, sizeof(mr));
    mr.mr_ifindex = ll.sll_ifindex;
    mr.mr_type = PACKET_MR_PROMISC;
    if(setsockopt(sock_r, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mr, sizeof(mr)) < 0)
    {
        perror("setsockopt[PACKET_MR_PROMISC]");
        close(sock_r);
        return -1;
    }

    pc = new PostgreSQLCache();

    unsigned char *buffer = (unsigned char *) malloc(BUFSIZE);
    while(true)
    {
        memset(buffer, 0, BUFSIZE);

        buflen = recvfrom(sock_r, buffer, BUFSIZE, 0, NULL, NULL);
        if(buflen < 0)
        {
            perror("error in recvfrom()\n");
            continue;
        }

        processFrame(buffer, buflen);
    }
    free(buffer);
    return 0;
}
