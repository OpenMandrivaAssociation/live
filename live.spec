Summary:	LIVE555 Streaming Media Library
Name:		live
Version:	2013.06.18
Release:	2
Source0:	http://live555.com/liveMedia/public/%{name}.%{version}.tar.gz
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.live555.com/liveMedia/

%description
This code forms a set of C++ libraries for multimedia streaming, using
open standard protocols (RTP/RTCP, RTSP, SIP). These libraries - which
can be compiled for Unix (including Linux and Mac OS X), Windows, and
QNX (and other POSIX-compliant systems) - can be used to build
streaming applications.

This package contains the example apps of LIVE555.

%package	devel
Summary:	Development files of the LIVE555 Streaming Media Library
Group:		Development/C++

%description	devel
This code forms a set of C++ libraries for multimedia streaming, using
open standard protocols (RTP/RTCP, RTSP, SIP). These libraries - which
can be compiled for Unix (including Linux and Mac OS X), Windows, and
QNX (and other POSIX-compliant systems) - can be used to build
streaming applications.

This package contains all needed files to build programs based on LIVE555.

%prep
%setup -q -n %{name}
sed -i -e "s/-O2/$RPM_OPT_FLAGS/" \
  config.linux-with-shared-libraries
  
find . -name '*.cpp' -exec chmod 644 {} \;

%build
%setup_compile_flags
./genMakefiles linux
make clean
make CFLAGS="%{optflags} -DRTSPCLIENT_SYNCHRONOUS_INTERFACE=1"

%install
for dir in BasicUsageEnvironment groupsock liveMedia UsageEnvironment; do
  mkdir -p %{buildroot}%{_libdir}/%{name}/$dir
  cp -r $dir/*.a $dir/include %{buildroot}%{_libdir}/%{name}/$dir
done
mkdir -p %{buildroot}%{_bindir}
for testprog in `find testProgs mediaServer -type f -perm 755`; do
  install $testprog %{buildroot}%{_bindir}
done

%files
%doc COPYING README
%{_bindir}/MPEG2TransportStreamIndexer
%{_bindir}/live555MediaServer
%{_bindir}/openRTSP
%{_bindir}/playSIP
%{_bindir}/sapWatch
%{_bindir}/test*
%{_bindir}/vobStreamer

%files devel
%{_libdir}/%{name}
