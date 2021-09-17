# CVC4 - Installation

To install CVC4 multiple steps are necessary, which are explained in the following.

## Cross-Compiling

To create the CVC4 binary I did a cross-compiling-procedure with the provided docker container:
https://www.ev3dev.org/docs/tutorials/using-docker-to-cross-compile/

1. `sudo apt-get update`
2. `export CC=arm-linux-gnueabi-gcc `
3. `export CXX=arm-linux-gnueabi-g++`
4. `sudo apt-get install python3:armel`
5. `sudo apt-get install libgmp3-dev:armel`
6. `sudo apt install python-pip`
7. `pip install toml`
8. `sudo apt install default-jdk:armel`
9. Cross-compile antlr
   dependency: `./configure CC=arm-linux-gnueabi-gcc CXX=arm-linux-gnueabi-g++ --prefix=/src/LIBANTLR3C_INSTALL_DIR`
10. `./configure.sh production --antlr-dir=/src/LIBANTLR3C_INSTALL_DIR/libantlr3c-3.4 --gmp-dir=/usr/lib/arm-linux-gnueabi --static --static-binary`

For details see: https://hackmd.io/@EzPfmI1gT8S-9pvnJOhNlg/Skago80uO