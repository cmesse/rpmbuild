%global major_version 3
%global minor_version 28
%global patch_version 1

Name:           tpls-%{tpls_flavor}-cmake
Version:        %{major_version}.%{minor_version}.%{patch_version}
Release:        1%{?dist}
Summary:        Cross-platform make system

License:        BSD-3-Clause AND MIT-open-group AND Zlib AND Apache-2.0
URL:            http://www.cmake.org
Source0:        http://www.cmake.org/files/v%{major_version}.%{minor_version}/cmake-%{version}.tar.gz
Patch0:         cmake_icpx.patch

BuildRequires:  %{tpls_rpm_cc}   >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_cxx}  >= %{tpls_comp_minver}
BuildRequires:  %{tpls_rpm_fc}  >= %{tpls_comp_minver}

BuildRequires:  sed
BuildRequires:  git
BuildRequires:  ncurses-devel

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

%{setup_tpls_env}

%{tpls_env} ../bootstrap \
    --prefix=%{tpls_prefix} \
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
%{tpls_prefix}/bin/ccmake
%{tpls_prefix}/bin/cmake
%{tpls_prefix}/bin/cpack
%{tpls_prefix}/bin/ctest
%{tpls_prefix}/doc/cmake-%{major_version}.%{minor_version}
%{tpls_prefix}/share/aclocal/cmake.m4
%{tpls_prefix}/share/bash-completion/completions/cmake
%{tpls_prefix}/share/bash-completion/completions/cpack
%{tpls_prefix}/share/bash-completion/completions/ctest
%{tpls_prefix}/share/cmake-%{major_version}.%{minor_version}
%{tpls_prefix}/share/emacs/site-lisp/cmake-mode.el
%{tpls_prefix}/share/vim/vimfiles/indent/cmake.vim
%{tpls_prefix}/share/vim/vimfiles/syntax/cmake.vim

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 3.28.1
- Initial Package
