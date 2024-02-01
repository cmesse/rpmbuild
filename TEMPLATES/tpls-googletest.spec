Name:           tpls-%{tpls_flavor}-googletest
Version:        1.14.0
Release:        1%{?dist}
Summary:        GoogleTest - Google Testing and Mocking Framework


License:        BSD-3-Clause
URL:            https://github.com/google/googletest
Source0:        https://github.com/google/googletest/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake

%description
Googletest is a comprehensive testing framework for C++ designed to support test-driven development and Google's extensive internal test suites. It provides a rich set of assertions, user-defined assertions, death tests, and easy-to-use fixtures for writing both small and large test cases. Googletest is portable and can be used across diverse platforms. It encourages organized, expressive, and efficient testing practices, and integrates well with various build systems. This makes it suitable for both new and existing C++ projects looking to implement robust testing.

%prep
%setup -q -n googletest-%{version}

%build
mkdir build && cd build
%{tpls_env} \
%{tpls_cmake} \
    -DCMAKE_C_COMPILER_AR=%{tpls_ar} \
    -DCMAKE_C_COMPILER=%{tpls_cc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_cxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
%if "%{tpls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
%if "%{tpls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
%endif
%endif
	..

%make_build


%install
cd build
%make_install

%files
%{tpls_prefix}/include/gmock
%{tpls_prefix}/include/gtest
%{tpls_prefix}/lib/cmake/GTest
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libgmock.a
%{tpls_prefix}/lib/libgmock_main.a
%{tpls_prefix}/lib/libgtest.a
%{tpls_prefix}/lib/libgtest_main.a
%else
%{tpls_prefix}/lib/libgmock.so
%{tpls_prefix}/lib/libgmock.so.*
%{tpls_prefix}/lib/libgmock_main.so
%{tpls_prefix}/lib/libgmock_main.so.*
%{tpls_prefix}/lib/libgtest.so
%{tpls_prefix}/lib/libgtest.so.*
%{tpls_prefix}/lib/libgtest_main.so
%{tpls_prefix}/lib/libgtest_main.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/gmock.pc
%{tpls_prefix}/lib/pkgconfig/gmock_main.pc
%{tpls_prefix}/lib/pkgconfig/gtest.pc
%{tpls_prefix}/lib/pkgconfig/gtest_main.pc

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 1.14.0-1
- Initial Package

