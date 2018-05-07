#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <string>
#include <vector>


#define UNKNOWN 0
#define FROM_SRC_TO_DST 1
#define FROM_DST_TO_SRC 2

struct TCPSession {
    std::string ip_src;
    uint16_t src_port;
    std::string ip_dst;
    uint16_t dst_port;
    bool is_active;
    std::string first_segm_tstmp;
    std::string last_segm_tstmp;
    std::string remote_geolocation;
};

struct TCPSessionMin {
    std::string ip_src;
    uint16_t src_port;
    std::string ip_dst;
    uint16_t dst_port;
};

struct TCPSegment {
    std::vector<std::string> flags;
    int size;
    std::string timestamp;
    int direction;
};

struct ICMPSegment {
    std::string ip_src;
    std::string ip_dst;
    uint8_t type;
    std::string timestamp;
};

struct UDPSegment {
    std::string ip_src;
    uint16_t src_port;
    std::string ip_dst;
    uint16_t dst_port;
    int size;
    std::string timestamp;
};

struct ARPPacket {

};

struct HTTPSite {
    std::string ip;
    std::string domain;
    std::string url;
};

#endif // STRUCTURES_H
