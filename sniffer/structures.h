#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <string>
#include <vector>

enum class TCPSegmentDirection {
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



#endif // STRUCTURES_H
