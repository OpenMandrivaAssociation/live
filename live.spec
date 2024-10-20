# Weird libraries with circular interdependencies
%define _disable_ld_no_undefined 1

Summary:	LIVE555 Streaming Media Library
Name:		live
Version:	2023.03.30
Release:	1
Source0:	http://live555.com/liveMedia/public/%{name}.%{version}.tar.gz
License:	LGPLv2+
Group:		System/Libraries
URL:		https://www.live555.com/liveMedia/

BuildRequires:  pkgconfig(openssl)

Obsoletes:	%{mklibname BasicUsageEnvironment 0} < 2015.08.07
Obsoletes:	%{mklibname BasicUsageEnvironment 1} < 2023.03.30
Obsoletes:	%{mklibname UsageEnvironment 2} < 2015.08.07
Obsoletes:	%{mklibname UsageEnvironment 3} < 2023.03.30
Obsoletes:	%{mklibname groupsock 4} < 2015.08.07
Obsoletes:	%{mklibname groupsock 25} < 2021.05.01
Obsoletes:	%{mklibname groupsock 30} < 2023.03.30
Obsoletes:	%{mklibname liveMedia 42} < 2015.08.07
Obsoletes:	%{mklibname liveMedia 58} < 2017.10.28
Obsoletes:	%{mklibname liveMedia 87} < 2021.05.01
Obsoletes:	%{mklibname liveMedia 107} < 2023.03.30

%define BasicUsageEnvironmentMajor 2
%define UsageEnvironmentMajor 3
%define groupsockMajor 30
%define liveMediaMajor 107

%libpackage BasicUsageEnvironment %{BasicUsageEnvironmentMajor}
%libpackage UsageEnvironment %{UsageEnvironmentMajor}
%libpackage groupsock %{groupsockMajor}
%libpackage liveMedia %{liveMediaMajor}

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
Requires:	%{mklibname BasicUsageEnvironment} = %EVRD
Requires:	%{mklibname UsageEnvironment} = %EVRD
Requires:	%{mklibname groupsock} = %EVRD
Requires:	%{mklibname liveMedia} = %EVRD

%description	devel
This code forms a set of C++ libraries for multimedia streaming, using
open standard protocols (RTP/RTCP, RTSP, SIP). These libraries - which
can be compiled for Unix (including Linux and Mac OS X), Windows, and
QNX (and other POSIX-compliant systems) - can be used to build
streaming applications.

This package contains all needed files to build programs based on LIVE555.

%prep
%setup -q -n %{name}
%autopatch -p1
sed -i -e "s/-O2/$RPM_OPT_FLAGS/" \
  config.linux-with-shared-libraries
  
find . -name '*.cpp' -exec chmod 644 {} \;

%build
%setup_compile_flags
./genMakefiles linux-with-shared-libraries
make clean
%make LINK="%{__cxx} -o" LIBRARY_LINK="%{__cc} -o" C_COMPILER="%{__cc}" CPLUSPLUS_COMPILER="%{__cxx}" CFLAGS="%{optflags} -DRTSPCLIENT_SYNCHRONOUS_INTERFACE=1" PREFIX=%{_prefix} LIBDIR=%{_libdir}

%install
%make_install PREFIX=%{_prefix} LIBDIR=%{_libdir}
# Based on http://www.mail-archive.com/live-devel@lists.live555.com/msg09499.html
if [ -d %{buildroot}%{_libdir}/pkgconfig ]; then
	echo "pkgconfig file was added upstream, remove our addition"
	exit 1
fi
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat >%{buildroot}%{_libdir}/pkgconfig/live555.pc <<EOF
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_prefix}/include

Name: %{name}555
Description: multimedia RTSP streaming library
Version: %{version}
Cflags: -I\${includedir}/liveMedia -I\${includedir}/groupsock -I\${includedir}/BasicUsageEnvironment -I\${includedir}/UsageEnvironment
Libs: -lliveMedia -lgroupsock -lBasicUsageEnvironment -lUsageEnvironment
EOF

%files
%doc COPYING README
%{_bindir}/MPEG2TransportStreamIndexer
%{_bindir}/mikeyParse
%{_bindir}/live555MediaServer
%{_bindir}/live555ProxyServer
%{_bindir}/live555HLSProxy
%{_bindir}/openRTSP
%{_bindir}/playSIP
%{_bindir}/registerRTSPStream
%{_bindir}/sapWatch
%{_bindir}/test*
%{_bindir}/vobStreamer


%files devel
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
