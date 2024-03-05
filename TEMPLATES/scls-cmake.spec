%global major_version 3
%global minor_version 28
%global patch_version 3

%define scls_oflags -O2

Name:           scls-%{scls_flavor}-cmake
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release:        2%{?dist}
Summary:        Cross-platform make system

License:        BSD-3-Clause AND MIT-open-group AND Zlib AND Apache-2.0
URL:            http://www.cmake.org
Source0:        http://www.cmake.org/files/v%{major_version}.%{minor_version}/cmake-%{version}.tar.gz
Patch0:         cmake_icpx.patch

BuildRequires:  %{scls_rpm_cc}   >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_cxx}  >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_fc}   >= %{scls_comp_minver}

%if "%{scls_compiler}" == "intel"
BuildRequires:  intel-oneapi-openmp  >= %{scls_comp_minver}
Requires:       intel-oneapi-openmp  >= %{scls_comp_minver}
%endif

BuildRequires:  sed
BuildRequires:  git
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
Requires:       ncurses

%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files. CMake generates
native makefiles and workspaces that can be used in the compiler
environment of your choice. CMake is quite sophisticated: it is possible
to support complex environments requiring system configuration, preprocessor
generation, code generation, and template instantiation.



%prep
%setup -n cmake-%{version}

%patch0 -p1

%build
sed -i '/"lib64"/s/64//' Modules/GNUInstallDirs.cmake

mkdir build && cd build

%{setup_scls_env}

%{scls_env} \
CFLAGS+=" %{scls_oflags}" \
CXXFLAGS+=" %{scls_oflags}" \
FCFLAGS+=" %{scls_oflags}" \
../bootstrap \
    --prefix=%{scls_prefix} \
    --no-qt-gui \
    --no-system-libs \
    --parallel=$(nproc) \
    --generator="Unix Makefiles"
    
make %{?_smp_mflags}

%check
#cd build
#make test

%install
cd build
%make_install

%files
%{scls_prefix}/bin/ccmake
%{scls_prefix}/bin/cmake
%{scls_prefix}/bin/cpack
%{scls_prefix}/bin/ctest
%{scls_prefix}/doc/cmake-%{major_version}.%{minor_version}
%{scls_prefix}/share/aclocal/cmake.m4
%{scls_prefix}/share/bash-completion/completions/cmake
%{scls_prefix}/share/bash-completion/completions/cpack
%{scls_prefix}/share/bash-completion/completions/ctest
%{scls_prefix}/share/cmake-%{major_version}.%{minor_version}
%{scls_prefix}/share/emacs/site-lisp/cmake-mode.el
%{scls_prefix}/share/vim/vimfiles/indent/cmake.vim
%{scls_prefix}/share/vim/vimfiles/syntax/cmake.vim

%changelog
* Mon Mar  4 2024 Christian Messe <cmesse@lbl.gov> - 3.28.3-2
- Update to 3.28.3

* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.28.2-1
- Initial Package
