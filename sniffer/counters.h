#ifndef COUNTERS_H
#define COUNTERS_H

class Counters {
public:
    Counters(){
        zeroize();
    }

    void zeroize()
    {
        tcp_syn = 0;
        tcp_ack = 0;
        tcp_synack = 0;
        tcp_psh = 0;
        tcp_rst = 0;
        tcp_fin = 0;
        tcp = 0;
        ip = 0;
        arp = 0;
        udp = 0;
        icmp = 0;
        l2_traffic = 0;
        l3_traffic = 0;
        l4_traffic = 0;
        l2_frames = 0;
        l3_frames = 0;
        l4_frames = 0;
    }

    unsigned int tcp_syn;
    unsigned int tcp_ack;
    unsigned int tcp_synack;
    unsigned int tcp_psh;
    unsigned int tcp_rst;
    unsigned int tcp_fin;
    unsigned int tcp;
    unsigned int ip;
    unsigned int arp;
    unsigned int udp;
    unsigned int icmp;
    unsigned int l2_traffic;
    unsigned int l3_traffic;
    unsigned int l4_traffic;
    unsigned int l2_frames;
    unsigned int l3_frames;
    unsigned int l4_frames;
};

#endif // COUNTERS_H
