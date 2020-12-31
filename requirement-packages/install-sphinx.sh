#!/bin/bash
INSTALL_DATE=$(date +%Y%m%d)
sudo apt-get install -y gcc automake autoconf libtool bison swig python-dev libpulse-dev build-essential git libtool pkg-config intltool-debian checkinstall

mkdir sphinx-source
cd sphinx-source/

git clone https://github.com/cmusphinx/sphinxbase.git
git clone https://github.com/cmusphinx/pocketsphinx.git
git clone https://github.com/cmusphinx/sphinxtrain.git

cd sphinxbase/
./autogen.sh
make
sudo checkinstall --pkgversion=$INSTALL_DATE -y -D make install
echo '/usr/local/lib' | sudo tee --append /etc/ld.so.conf.d/cmu-sphinx.conf
sudo ldconfig

cd ../pocketsphinx/
./autogen.sh
make
sudo checkinstall --pkgversion=$INSTALL_DATE -y -D make install

cd ../sphinxtrain/
./autogen.sh
make
sudo checkinstall --pkgversion=$INSTALL_DATE -y -D make install

cd ..
svn checkout https://svn.code.sf.net/p/cmusphinx/code/trunk cmusphinx-code
cd cmusphinx-code/cmuclmtk/
./autogen.sh
make
sudo checkinstall --pkgversion=$INSTALL_DATE -y -D make install

