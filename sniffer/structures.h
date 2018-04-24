#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <string>
#include <vector>

enum class TCPSegmentDirection {
    UNKNOWN,
    FROM_SRC_TO_DST,
    FROM_DST_TO_SRC
};

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
    TCPSegmentDirection direction;
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


#endif // STRUCTURES_H
