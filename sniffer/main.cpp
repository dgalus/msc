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

#include "utils.h"
#include "arphdr.h"

#define BUFSIZE 65536


void processFrame(unsigned char *buffer)
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

    if(eth->h_proto == 0x0608) // ARP
    {
        struct arphdr_t *arph = (struct arphdr_t *)(buffer + sizeof(struct ethhdr));
        if(ntohs(arph->htype) == 1 && ntohs(arph->ptype) == 0x0800)
        {
            rapidjson::Value arp(rapidjson::kObjectType);

            char sender_mac[18];
            char target_mac[18];
            char sender_ip[16];
            char target_ip[16];
            snprintf(sender_mac, 18, "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X", arph->sha[0], arph->sha[1], arph->sha[2], arph->sha[3], arph->sha[4], arph->sha[5]);
            snprintf(target_mac, 18, "%.2X:%.2X:%.2X:%.2X:%.2X:%.2X", arph->tha[0], arph->tha[1], arph->tha[2], arph->tha[3], arph->tha[4], arph->tha[5]);
            snprintf(sender_ip, 16, "%d.%d.%d.%d", arph->spa[0], arph->spa[1], arph->spa[2], arph->spa[3]);
            snprintf(target_ip, 16, "%d.%d.%d.%d", arph->tpa[0], arph->tpa[1], arph->tpa[2], arph->tpa[3]);

            rapidjson::Value sender_hw_val;
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
            arp.AddMember("operation", operation_val, allocator);

            d.AddMember("arp", arp, allocator);
        }
    }
    else if(eth->h_proto == 0x0008) // IP
    {
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
            struct icmphdr *icmph = (struct icmphdr *)(buffer + iphdrlen + sizeof(struct ethhdr));

            rapidjson::Value icmp(rapidjson::kObjectType);

            rapidjson::Value type_val;
            type_val.SetUint((unsigned int) icmph->type);
            icmp.AddMember("type", type_val, allocator);

            d.AddMember("icmp", icmp, allocator);
        }
        else if(iph->protocol == 6)
        {
            struct tcphdr *tcph = (struct tcphdr*) (buffer + iphdrlen + sizeof(struct ethhdr));

            rapidjson::Value tcp(rapidjson::kObjectType);

            rapidjson::Value src_port_val;
            src_port_val.SetUint(ntohs(tcph->source));
            tcp.AddMember("src_port", src_port_val, allocator);

            rapidjson::Value dest_port_val;
            dest_port_val.SetUint(ntohs(tcph->dest));
            tcp.AddMember("dest_port", dest_port_val, allocator);

            rapidjson::Value seq_val;
            seq_val.SetUint(ntohs(tcph->seq));
            tcp.AddMember("seq", seq_val, allocator);

            rapidjson::Value ack_seq_val;
            ack_seq_val.SetUint(ntohs(tcph->ack_seq));
            tcp.AddMember("ack_seq", ack_seq_val, allocator);

            rapidjson::Value urg_flag_val;
            urg_flag_val.SetBool((tcph->urg != 0));
            tcp.AddMember("urg", urg_flag_val, allocator);

            rapidjson::Value ack_flag_val;
            ack_flag_val.SetBool((tcph->ack != 0));
            tcp.AddMember("ack", ack_flag_val, allocator);

            rapidjson::Value psh_flag_val;
            psh_flag_val.SetBool((tcph->psh != 0));
            tcp.AddMember("psh", psh_flag_val, allocator);

            rapidjson::Value rst_flag_val;
            rst_flag_val.SetBool((tcph->rst != 0));
            tcp.AddMember("rst", rst_flag_val, allocator);

            rapidjson::Value syn_flag_val;
            syn_flag_val.SetBool((tcph->syn != 0));
            tcp.AddMember("syn", syn_flag_val, allocator);

            rapidjson::Value fin_flag_val;
            fin_flag_val.SetBool((tcph->fin != 0));
            tcp.AddMember("fin", fin_flag_val, allocator);

            d.AddMember("tcp", tcp, allocator);
        }
        else if(iph->protocol == 17)
        {
            struct udphdr *udph = (struct udphdr*) (buffer + iphdrlen + sizeof(struct ethhdr));

            rapidjson::Value udp(rapidjson::kObjectType);

            rapidjson::Value src_port_val;
            src_port_val.SetUint(ntohs(udph->source));
            udp.AddMember("src_port", src_port_val, allocator);

            rapidjson::Value dest_port_val;
            dest_port_val.SetUint(ntohs(udph->dest));
            udp.AddMember("dest_port", dest_port_val, allocator);

            d.AddMember("udp", udp, allocator);
        }
    }
    std::string datetime = getCurrentDateTime();
}

int main(int argc, char *argv[])
{
    int sock_r;
    int buflen;

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

        processFrame(buffer);
    }
    free(buffer);
    return 0;
}
