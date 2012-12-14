%define	snap 20051220

%define	major	0
%define libname	%mklibname fx %{major}
%define devname	%mklibname fx -d

Summary:	A library for call control with analogue telephony interfaces
Name:		libfx
Version:	0.0.3
Release:	0.%{snap}.5
License:	GPL
Group:		System/Libraries
URL:		http://www.soft-switch.org/
Source0:	http://www.soft-switch.org/downloads/snapshots/unicall/libfx-%{snap}.tar.bz2
Patch0:		libfx-zaptel_header.diff

BuildRequires:	file
BuildRequires:	jpeg-devel
BuildRequires:	libsupertone-devel
BuildRequires:	libunicall-devel
BuildRequires:	zaptel-devel
BuildRequires:	pkgconfig(spandsp)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libxml-2.0)

%description
libfx is a library for call control with analogue telephony interfaces.

%package -n	%{libname}
Summary:	A library for call control with analogue telephony interfaces
Group:          System/Libraries

%description -n	%{libname}
libfx is a library for call control with analogue telephony interfaces.

%package -n	%{devname}
Summary:	Header files and libraries needed for development with libfx
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel
Obsoletes:	%{_lib}%{name}0-devel

%description -n	%{devname}
This package includes the header files and libraries needed for
developing programs using libfx.

%prep
%setup -q
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
install -d %{buildroot}%{_includedir}

%makeinstall_std

install -m0644 libfx.h %{buildroot}%{_includedir}/

%files -n %{libname}
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/unicall/protocols/*.so

%files -n %{devname}
%{_libdir}/unicall/protocols/*.a
%{_libdir}/unicall/protocols/*.la
%{_includedir}/*.h

