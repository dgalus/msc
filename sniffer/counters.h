#ifndef COUNTERS_H
#define COUNTERS_H

class Counters {

public:
    double tcp_syn;
    double tcp_ack;
    double tcp_synack;
    double tcp_psh;
    double tcp_rst;
    double tcp_fin;
    double tcp;
    double ip;
    double arp;
    double udp;
    double icmp;
    double l2_traffic;
    double l3_traffic;
    double l4_traffic;
    double l2_frames;
    double l3_frames;
    double l4_frames;
};

#endif // COUNTERS_H
