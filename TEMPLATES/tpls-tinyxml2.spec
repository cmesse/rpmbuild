Name:           tpls-%{tpls_flavor}-tinyxml2
Version:        10.0.0
Release:        1%{?dist}
Summary:        [brief description]

License:        zlib
URL:            https://github.com/leethomason/tinyxml2
Source0:        https://github.com/leethomason/tinyxml2/releases/tag/%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake

%description
TinyXML-2 is a simple, small, efficient, C++ XML parser that can be
easily integrated into other programs. It uses a Document Object Model
(DOM), meaning the XML data is parsed into a C++ objects that can be
browsed and manipulated, and then written to disk or another output stream.

TinyXML-2 doesn't parse or use DTDs (Document Type Definitions) nor XSLs
(eXtensible Stylesheet Language).

TinyXML-2 uses a similar API to TinyXML-1, But the implementation of the
parser was completely re-written to make it more appropriate for use in a
game. It uses less memory, is faster, and uses far fewer memory allocations.

%prep
%setup -q -n tinyxml2-%{version}

%build
%{tpls_env} \
%{tpls_cmake} . \
%if "%{tpls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
%endif

%make_build

%check
make test

%install

%make_install

%files
%{tpls_prefix}/include/tinyxml2.h
%{tpls_prefix}/lib/cmake/tinyxml2
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libtinyxml2.a
%else
%{tpls_prefix}/lib/libtinyxml2.so
%{tpls_prefix}/lib/libtinyxml2.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/tinyxml2.pc


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 9.3.0
- Initial Package
