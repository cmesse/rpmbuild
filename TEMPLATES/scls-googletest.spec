%define scls_oflags -O2

Name:           scls-%{scls_flavor}-googletest
Version:        1.14.0
Release:        1%{?dist}
Summary:        GoogleTest - Google Testing and Mocking Framework


License:        BSD-3-Clause
URL:            https://github.com/google/googletest
Source0:        https://github.com/google/googletest/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  scls-%{scls_flavor}-cmake

%description
Googletest is a comprehensive testing framework for C++ designed to support test-driven development and Google's extensive internal test suites. It provides a rich set of assertions, user-defined assertions, death tests, and easy-to-use fixtures for writing both small and large test cases. Googletest is portable and can be used across diverse platforms. It encourages organized, expressive, and efficient testing practices, and integrates well with various build systems. This makes it suitable for both new and existing C++ projects looking to implement robust testing.

%prep
%setup -q -n googletest-%{version}

%build
mkdir build && cd build
%{scls_env} \
%{scls_cmake} \
    -DCMAKE_C_COMPILER_AR=%{scls_ar} \
    -DCMAKE_C_COMPILER=%{scls_cc} \
    -DCMAKE_C_FLAGS="%{scls_cflags} %{scls_oflags}" \
    -DCMAKE_CXX_COMPILER=%{scls_cxx} \
    -DCMAKE_CXX_FLAGS="%{scls_cxxflags} %{scls_oflags}" \
%if "%{scls_libs}" == "static"
	-DBUILD_SHARED_LIBS=OFF \
%else
	-DBUILD_SHARED_LIBS=ON \
%if "%{scls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib -L%{scls_comproot}/lib -Wl,-rpath,%{scls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{scls_prefix}/lib -Wl,-rpath,%{scls_prefix}/lib" \
%endif
%endif
	..

%make_build


%install
cd build
%make_install

%files
%{scls_prefix}/include/gmock
%{scls_prefix}/include/gtest
%{scls_prefix}/lib/cmake/GTest
%if "%{scls_libs}" == "static"
%{scls_prefix}/lib/libgmock.a
%{scls_prefix}/lib/libgmock_main.a
%{scls_prefix}/lib/libgtest.a
%{scls_prefix}/lib/libgtest_main.a
%else
%{scls_prefix}/lib/libgmock.so
%{scls_prefix}/lib/libgmock.so.*
%{scls_prefix}/lib/libgmock_main.so
%{scls_prefix}/lib/libgmock_main.so.*
%{scls_prefix}/lib/libgtest.so
%{scls_prefix}/lib/libgtest.so.*
%{scls_prefix}/lib/libgtest_main.so
%{scls_prefix}/lib/libgtest_main.so.*
%endif
%{scls_prefix}/lib/pkgconfig/gmock.pc
%{scls_prefix}/lib/pkgconfig/gmock_main.pc
%{scls_prefix}/lib/pkgconfig/gtest.pc
%{scls_prefix}/lib/pkgconfig/gtest_main.pc

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 1.14.0-1
- Initial Package

