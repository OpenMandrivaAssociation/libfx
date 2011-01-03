%define	snap 20051220

%define	major 0
%define libname	%mklibname fx %{major}

Summary:	A library for call control with analogue telephony interfaces
Name:		libfx
Version:	0.0.3
Release:	%mkrel 0.%{snap}.5
License:	GPL
Group:		System/Libraries
URL:		http://www.soft-switch.org/
Source0:	http://www.soft-switch.org/downloads/snapshots/unicall/libfx-%{snap}.tar.bz2
Patch0:		libfx-zaptel_header.diff
BuildRequires:	zaptel-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	libspandsp-devel
BuildRequires:	libsupertone-devel
BuildRequires:	libunicall-devel
BuildRequires:	tiff-devel >= 3.6.1-3mdk
BuildRequires:	libxml2-devel
BuildRequires:	jpeg-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
libfx is a library for call control with analogue telephony interfaces.

%package -n	%{libname}
Summary:	A library for call control with analogue telephony interfaces
Group:          System/Libraries

%description -n	%{libname}
libfx is a library for call control with analogue telephony interfaces.

%package -n	%{libname}-devel
Summary:	Header files and libraries needed for development with libfx
Group:		Development/C
Provides:	%{name}-devel lib%{name}-devel
Obsoletes:	%{name}-devel lib%{name}-devel
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
This package includes the header files and libraries needed for
developing programs using libfx.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -pi -e "s|^protocoldir=.*|protocoldir=\"%{_libdir}/unicall/protocols\"|g" configure.ac Makefile.am

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force && aclocal && autoconf && automake --add-missing --copy

%configure2_5x \
    --enable-shared \
    --enable-static

make CFLAGS="%{optflags} -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_includedir}

%makeinstall_std

install -m0644 libfx.h %{buildroot}%{_includedir}/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/unicall/protocols/*.so

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/unicall/protocols/*.a
%{_libdir}/unicall/protocols/*.la
%{_includedir}/*.h


