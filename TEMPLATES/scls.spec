Name:           scls-%{scls_flavor}
Version:        2024
Release:        2%{?dist}
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
#Requires:       scls-%{scls_flavor}-fftw
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

# Function to remove specific paths from a colon-separated variable
remove_from_var() {
    local var_name=$1
    local pattern=$2
    if [[ -n "${!var_name}" ]]; then
        # Convert the variable into an array of paths, filter out unwanted paths, then reassemble
        IFS=':' read -ra paths <<< "${!var_name}"
        local new_paths=()
        for path in "${paths[@]}"; do
            if [[ ! $path =~ $pattern ]]; then
                new_paths+=("$path")
            fi
        done
        # Re-join the paths and export the variable
        export "$var_name"="$(IFS=:; echo "${new_paths[*]}")"
    fi
}

# Function to safely append to any colon-separated variable
add_to_var() {
    local var_name=$1
    local new_path=$2
    if [[ ":${!var_name}:" != *":$new_path:"* ]]; then
        if [[ -z "${!var_name}" ]]; then
            export "$var_name"="$new_path"
        else
            export "$var_name"="$new_path:${!var_name}"
        fi
    fi
}

# Remove unwanted paths
remove_from_var PATH '^/opt/scls/.*/bin$'
remove_from_var PKG_CONFIG_PATH '^/opt/scls/.*/lib/pkgconfig$'
remove_from_var CMAKE_PREFIX_PATH '^/opt/scls/.*/lib/cmake$'

# Add new paths
add_to_var PATH "%{scls_prefix}/bin"
add_to_var PKG_CONFIG_PATH "%{scls_prefix}/lib/pkgconfig"
add_to_var CMAKE_PREFIX_PATH "%{scls_prefix}/lib/cmake"

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
* Mon Mar  4 2024 Christian Messe <cmesse@lbl.gov> - 2024-2
- remove FFTW

* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 2024-1
- Initial Package
