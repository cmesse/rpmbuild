Name:           scls-%{scls_flavor}
Version:        2024
Release:        1%{?dist}
Summary:        Scientific Core Libraries

License:        Various
URL:            https://belfem.lbl.gov

BuildArch:      noarch

BuildRequires:  %{scls_rpm_cc}   >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_cxx}  >= %{scls_comp_minver}
BuildRequires:  %{scls_rpm_fc}   >= %{scls_comp_minver}

%if "%{scls_compiler}" == "intel"
BuildRequires:  intel-oneapi-openmp  >= %{scls_comp_minver}
Requires:       intel-oneapi-openmp  >= %{scls_comp_minver}
%endif



%if "%{scls_math}" != "lapack"
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
Requires:       intel-oneapi-mkl
%endif

# layer 1
Requires:       scls-%{scls_flavor}-cmake
Requires:       scls-%{scls_flavor}-gmp
Requires:       scls-%{scls_flavor}-libevent
Requires:       scls-%{scls_flavor}-gperftools

# layer 2
Requires:       scls-%{scls_flavor}-googletest
Requires:       scls-%{scls_flavor}-hwloc
Requires:       scls-%{scls_flavor}-mpfr
Requires:       scls-%{scls_flavor}-testsweeper
Requires:       scls-%{scls_flavor}-tinyxml2

# we assume that for rhel 8 and amazon, no visualization is there
%if 0%{?rhel} == 9
Requires:       scls-%{scls_flavor}-vtk
%endif


%if "%{scls_math}" == "lapack"
Requires:  scls-%{scls_flavor}-blas
Requires:  scls-%{scls_flavor}-cblas
Requires:  scls-%{scls_flavor}-lapack
Requires:  scls-%{scls_flavor}-lapacke
%endif

# layer 3
Requires:       scls-%{scls_flavor}-blaspp
Requires:       scls-%{scls_flavor}-blaze
%if "%{scls_math}" == "lapack"
Requires:       scls-%{scls_flavor}-fspblas
%endif
%if "%{scls_mpi}" != "intelmpi"
BuildRequires:  scls-%{scls_flavor}-pmix
%endif

# layer 4
%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif


# layer 5
Requires:       scls-%{scls_flavor}-fftw
Requires:       scls-%{scls_flavor}-hdf5
Requires:       scls-%{scls_flavor}-lapackpp
Requires:       scls-%{scls_flavor}-metis
Requires:       scls-%{scls_flavor}-zfp
Requires:       scls-%{scls_flavor}-nlopt

%if "%{scls_math}" == "lapack"
Requires:       scls-%{scls_flavor}-scalapack
%endif

# layer 6
Requires:       scls-%{scls_flavor}-arpack
Requires:       scls-%{scls_flavor}-netcdf
Requires:       scls-%{scls_flavor}-scotch
Requires:       scls-%{scls_flavor}-slate


# layer 7
Requires:       scls-%{scls_flavor}-superlu
Requires:       scls-%{scls_flavor}-butterflypack
Requires:       scls-%{scls_flavor}-exodus
Requires:       scls-%{scls_flavor}-mumps
Requires:       scls-%{scls_flavor}-suitesparse

# layer 8
Requires:       scls-%{scls_flavor}-armadillo
Requires:       scls-%{scls_flavor}-strumpack
Requires:       scls-%{scls_flavor}-petsc

# layer 9
Requires:       scls-%{scls_flavor}-sundials


%if "%{scls_math}" == "cuda"
BuildRequires:  nvhpc-%{scls_cuda_version}-cuda-multi
Requires:       nvhpc-%{scls_cuda_version}-cuda-multi
%endif

%description
Scientific Core Libraries

%prep
# No source for this package

%build
%{expand: %setup_scls_env}

cat <<'EOF' > activate
#!/usr/bin/env bash
export PATH=\$(echo \$PATH | tr ':' '\\n' | grep -v '^/opt/scls/.*/bin' | tr '\\n' ':' | sed 's/:\$//')
export PATH=%{scls_prefix}/bin:\$PATH
if [ -z "\$PKG_CONFIG_PATH" ]; then
   export PKG_CONFIG_PATH=%{scls_prefix}/lib/pkgconfig
else
   export PKG_CONFIG_PATH=\$(echo \$PKG_CONFIG_PATH | tr ':' '\\n' | grep -v '^/opt/scls/.*/lib/pkgconfig' | tr '\\n' ':' | sed 's/:\$//')
   export PKG_CONFIG_PATH=%{scls_prefix}/lib/pkgconfig:\$PKG_CONFIG_PATH
fi
if [ -z "\$CMAKE_PREFIX_PATH" ]; then
   export CMAKE_PREFIX_PATH=%{scls_prefix}/lib/cmake
else
   export CMAKE_PREFIX_PATH=\$(echo \$CMAKE_PREFIX_PATH | tr ':' '\\n' | grep -v '^/opt/scls/.*/lib/cmake' | tr '\\n' ':' | sed 's/:\$//')
   export CMAKE_PREFIX_PATH=%{scls_prefix}/lib/cmake:\$CMAKE_PREFIX_PATH
fi
export CC=%{scls_cc}
export CXX=%{scls_cxx}
export FC=%{scls_fc}
export PETSC_DIR=%{scls_prefix}
export SCLS=%{scls_prefix}
export MPI_HOME=%{scls_mpiroot}
clear
echo '--------------------------------------------------------------------------------'
echo '    Scientific Core Libraries skylake-gnu-mpich-lapack'
echo '--------------------------------------------------------------------------------'
EOF

chmod +x activate

%install
mkdir -p  %{buildroot}%{scls_prefix}/bin
install -m 755 activate %{buildroot}%{scls_prefix}/bin

%files
%{scls_prefix}/bin/activate

%post
echo ""
echo "     _______.  ______  __          _______."
echo "    /       | /      ||  |        /       |"
echo "   |   (----\`|  ,----'|  |       |   (----\`"
echo "    \   \    |  |     |  |        \   \    "
echo ".----)   |   |  \`----.|  \`----.----)   |   "
echo "|_______/     \______||_______|_______/    "
echo ""
echo "      SCIENTIFIC CORE LIBRARIES 2024"
echo ""
echo " the libraries have been installed in %{scls_prefix}"
echo " you can call"
echo ""
echo "       source %{scls_prefix}/bin/activate"
echo ""
echo " to set the environment variables."

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2024
- Initial Package
