TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += main.cpp

INCLUDEPATH += /usr/local/include/
LIBS += -L/usr/local/lib -lopencv_core -lopencv_imgproc -lopencv_highgui

include(deployment.pri)
qtcAddDeployment()

