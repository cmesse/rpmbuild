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

%if "%{scls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
Requires:       intel-oneapi-mpi
%else
BuildRequires:  scls-%{scls_flavor}-%{scls_mpi}
Requires:       scls-%{scls_flavor}-%{scls_mpi}
%endif

%if "%{scls_math}" == "cuda"
BuildRequires:  nvhpc-%{scls_cuda_version}-cuda-multi
Requires:       nvhpc-%{scls_cuda_version}-cuda-multi
BuildRequires:  scls-%{scls_flavor}-slate
Requires:       scls-%{scls_flavor}-slate
%endif

%if "%{scls_math}" == "lapack"
BuildRequires:  scls-%{scls_flavor}-blas
BuildRequires:  scls-%{scls_flavor}-lapack
BuildRequires:  scls-%{scls_flavor}-scalapack
Requires:       scls-%{scls_flavor}-blas
Requires:       scls-%{scls_flavor}-lapack
Requires:       scls-%{scls_flavor}-scalapack
%else
BuildRequires:  intel-oneapi-mkl
BuildRequires:  intel-oneapi-mkl-devel
Requires:       intel-oneapi-mkl
%endif

# layer 1
Requires:       scls-%{scls_flavor}-cmake
Requires:       scls-%{scls_flavor}-gmp
Requires:       scls-%{scls_flavor}-libevent

# layer 2
Requires:       scls-%{scls_flavor}-googletest
Requires:       scls-%{scls_flavor}-hwloc
Requires:       scls-%{scls_flavor}-mpfr
Requires:       scls-%{scls_flavor}-testsweeper
Requires:       scls-%{scls_flavor}-tinyxml2
Requires:       scls-%{scls_flavor}-vtk
Requires:       scls-%{scls_flavor}-zfp

# layer 3
Requires:       scls-%{scls_flavor}-blaspp
Requires:       scls-%{scls_flavor}-blaze


# layer 4
Requires:       scls-%{scls_flavor}-fftw
Requires:       scls-%{scls_flavor}-hdf5
Requires:       scls-%{scls_flavor}-lapackpp
Requires:       scls-%{scls_flavor}-metis

# layer 5
Requires:       scls-%{scls_flavor}-arpack
Requires:       scls-%{scls_flavor}-netcdf
Requires:       scls-%{scls_flavor}-scotch
Requires:       scls-%{scls_flavor}-slate
Requires:       scls-%{scls_flavor}-suitesparse
Requires:       scls-%{scls_flavor}-superlu

# layer 6
Requires:       scls-%{scls_flavor}-armadillo
Requires:       scls-%{scls_flavor}-butterflypack
Requires:       scls-%{scls_flavor}-exodus
Requires:       scls-%{scls_flavor}-mumps

# layer 7
Requires:       scls-%{scls_flavor}-strumpack

# layer 8
Requires:       scls-%{scls_flavor}-petsc
Requires:       scls-%{scls_flavor}-sundials

%description
Scientific Core Libraries

%prep
# No source for this package

%build
# Nothing to build

%install
# Nothing to install

%files
# No files to list

%post
echo ""
echo "     _______.  ______  __          _______."
echo "    /       | /      ||  |        /       |"
echo "   |   (----\`|  ,----'|  |       |   (----\`"
echo "    \   \    |  |     |  |        \   \    "
echo ".----)   |   |  \`----.|  \`----.----)   |   "
echo "|_______/     \______||_______|_______/    "
echo ""
echo " SCIENTIFIC CORE LIBRARIES 2024"
echo " the libraries have been installed in %{scls_prefix}"


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2024
- Initial Package
