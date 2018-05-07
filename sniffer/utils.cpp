#include "utils.h"

std::string getCurrentDateTime()
{
    time_t now = time(0);
    struct tm tstruct;
    char buf[80];
    tstruct = *localtime(&now);
    strftime(buf, sizeof(buf), "%Y-%m-%d %X", &tstruct);
    return std::string(buf);
}

std::string getStrBetweenTwoStr(const std::string &s, const std::string &startDelim, const std::string &stopDelim)
{
    unsigned firstDelimPos = s.find(startDelim);
    unsigned endPosOfFirstDelim = firstDelimPos + startDelim.length();
    unsigned lastDelimPos = s.find_first_of(stopDelim, endPosOfFirstDelim);
    
    return s.substr(endPosOfFirstDelim, lastDelimPos-endPosOfFirstDelim);
}