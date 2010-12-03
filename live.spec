%define name live
%define version 2010.04.09

Summary: LIVE555 Streaming Media Library
Name: %{name}
Version: %{version}
Release: %mkrel 2
Source0: http://live555.com/liveMedia/public/%{name}.%version.tar.gz
Patch0: live.2007.01.09-optflags.patch
Patch1: live-pic.patch
Patch2: live-format-strings.patch
License: LGPLv2+
Group: System/Libraries
URL: http://www.live555.com/liveMedia/
BuildRoot: %{_tmppath}/%{name}-buildroot

%description
This code forms a set of C++ libraries for multimedia streaming, using
open standard protocols (RTP/RTCP, RTSP, SIP). These libraries - which
can be compiled for Unix (including Linux and Mac OS X), Windows, and
QNX (and other POSIX-compliant systems) - can be used to build
streaming applications.

This package contains the example apps of LIVE555.

%package devel
Summary: Development files of the LIVE555 Streaming Media Library
Group: Development/C++

%description devel
This code forms a set of C++ libraries for multimedia streaming, using
open standard protocols (RTP/RTCP, RTSP, SIP). These libraries - which
can be compiled for Unix (including Linux and Mac OS X), Windows, and
QNX (and other POSIX-compliant systems) - can be used to build
streaming applications.

This package contains all needed files to build programs based on LIVE555.

%prep
%setup -q -n %name
%patch0 -p1 -b .optflags
%patch1 -p1 -b .pic
%patch2 -p1
rm -f testProgs/qtParse

%build
./genMakefiles linux
make clean
make RPM_OPT_FLAGS="%{optflags}"

%install
rm -rf $RPM_BUILD_ROOT
for dir in BasicUsageEnvironment groupsock liveMedia UsageEnvironment; do
  mkdir -p %buildroot%_libdir/%name/$dir
  cp -r $dir/*.a $dir/include %buildroot%_libdir/%name/$dir
done
mkdir -p %buildroot%_bindir
for testprog in `find testProgs mediaServer -type f -perm 755`; do
  install $testprog %buildroot%_bindir
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING README
%_bindir/MPEG2TransportStreamIndexer
%_bindir/live555MediaServer
%_bindir/openRTSP
%_bindir/playSIP
%_bindir/sapWatch
%_bindir/test*
%_bindir/vobStreamer


%files devel
%defattr(-,root,root)
%_libdir/%name


