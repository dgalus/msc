TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
        main.cpp \
    postgresqldatabase.cpp

HEADERS += \
    arphdr.h \
    utils.h \
    structures.h \
    counters.h \
    postgresqldatabase.h \
    idatabase.h
