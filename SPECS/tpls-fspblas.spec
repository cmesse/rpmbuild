Name:           tpls-%{tpls_flavor}-fspblas
Version:        0.5
Release:        1%{?dist}
Summary:        The NIST Reference Implementation of the Fortran Sparse Matrix Toolkit


License:        Public Domain
URL:            https://math.nist.gov/spblas/
Source0:        ftp://gams.nist.gov/pub/karin/fspblas/fspblas.shar.gz

BuildRequires:  tpls-%{tpls_flavor}-blas
Requires:       tpls-%{tpls_flavor}-blas

%description
FSPBLAS, from NIST, serves as a reference Fortran implementation for sparse matrix computations, akin to the role of BLAS in linear algebra. It supports key formats like CSR, CSC, and COO, and includes routines for matrix multiplication and triangular solves. While primarily used for development and testing in scientific computing, for performance-critical applications, alternatives like Intel's MKL are recommended. 

%prep

if [ "%{tpls_gpu}" != "lapack" ] || [ "%{tpls_compiler}" != "gnu" ]; then
    echo "Error: We only want to compile this library for tpls-gnu-lapack-* flavors!"
    exit 1
fi


# Decompress the .shar.gz file
gzip -dc %{SOURCE0} > fspblas.shar

# Execute the shell archive script to extract the contents
sh fspblas.shar  >> /dev/null

# Clean up the shell archive script file
rm -f fspblas.shar

# remove the outpu directory of it already exists
if [ -d fspblas-%{version} ] ; then
    rm -rf fspblas-%{version} ;
fi

# rename the directory
mv fspblas%{version} fspblas-%{version}


%build
cd fspblas-%{version}

%if "%{tpls_compiler}" == "intel"
if [ "$SETVARS_COMPLETED" != "1" ]; then
	source /opt/intel/oneapi/setvars.sh intel64
fi
%endif

rm -f makefile makefile.def


# Set architecture and compiler flags
%if "%{tpls_libs}" == "static"
echo 'ARCH          = %{tpls_ar}' >> Makefile
echo 'ARCHFLAGS     = %{tpls_arflags}'  >> Makefile
echo 'RANLIB        = ranlib' >> Makefile
echo 'FC            = %{tpls_fc}' >> Makefile
%if "%{tpls_compiler}" == "intel"
echo 'FCFLAGS       = %{tpls_foptflags} -diag-disable 8291' >> Makefile
%else
echo 'FCFLAGS       = %{tpls_foptflags}' >> Makefile
%endif
echo 'LDFLAGS       = %{tpls_ldflags} -lblas' >> Makefile
echo 'FSPBLASLIB    = libfspblas.a' >> Makefile
%else
echo 'FC            = %{tpls_fc}' >> Makefile
echo 'FCFLAGS       = %{tpls_foptflags} -fPIC' >> Makefile
echo 'LDFLAGS       = %{tpls_ldflags} %{tpls_rpath} -lblas' >> Makefile
echo 'FSPBLASLIB    = libfspblas.so' >> Makefile
%endif

echo >> Makefile

# Define source and object files
echo 'SRC = $(shell find ./src/*.f -type f) $(shell find ./level1/*.f -type f)'  >> Makefile
echo 'OBJ = $(SRC:.f=.o)' >> Makefile
echo >> Makefile

# Define targets for static and shared libraries
echo 'lib : $(FSPBLASLIB)' >> Makefile
echo >> Makefile

# Rules for building the static library
%if "%{tpls_libs}" == "static"
echo '$(FSPBLASLIB): $(OBJ)' >> Makefile
echo '	$(ARCH) $(ARCHFLAGS) $@ $(notdir $(OBJ))' >> Makefile
echo '	$(RANLIB) $@' >> Makefile
echo >> Makefile
%else
# Rules for building the shared library
echo '$(FSPBLASLIB): $(OBJ)' >> Makefile
echo '	$(FC) -shared $(LDFLAGS) -o $(FSPBLASLIB) $(notdir $(OBJ))' >> Makefile
echo >> Makefile
%endif


# Rules for building the objetcs
echo '%.o: %.f' >> Makefile
echo '	$(FC) $(FCFLAGS) -c $< -o $(notdir $@)' >> Makefile
echo >> Makefile



# Define test source and object files
echo 'TSRC  = $(shell find ./test/t*.f -type f)'  >> Makefile
echo 'TESTS = $(TSRC:.f=)' >> Makefile
echo 'ERRCHK = ./test/errchkmm.o ./test/errchksm.o ./test/resid.o' >> Makefile
echo >> Makefile
echo 'tests : $(TESTS)' >> Makefile
echo >> Makefile

# Rule to compile test source files into executables
echo '$(TESTS): %: %.f $(ERRCHK)' >> Makefile
echo '	$(FC) $(LDFLAGS) $(FSPBLASLIB) $(FCFLAGS) -o $@ $< $(ERRCHK)' >> Makefile

echo >> Makefile

# Rule to compile specific object files into the errchk executable
echo '$(ERRCHK): %.o: %.f' >> Makefile
echo '	$(FC) $(FCFLAGS) -c $< -o $@' >> Makefile


# build the library
make %{?_smp_mflags} lib

%check
make %{?_smp_mflags} tests
pushd ./test
LD_LIBRARY_PATH=.. ./runtests
pwd
popd


%install
mkdir -p  %{buildroot}%{tpls_prefix}/%{tpls_libdir}
%if "%{tpls_libs}" == "static"
install -m 0644 %{_builddir}/fspblas-%{version}/libfspblas.a %{buildroot}%{tpls_prefix}/%{tpls_libdir}/
%else
install -m 0644 %{_builddir}/fspblas-%{version}/libfspblas.so %{buildroot}%{tpls_prefix}/%{tpls_libdir}/
%endif

%files
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/%{tpls_libdir}/libfspblas.a
%else
%{tpls_prefix}/%{tpls_libdir}/libfspblas.so
%endif

%changelog
* Tue Dec 12 2023 Christian Messe <cmesse@lbl.gov> - 0.5.0-1
- Initial package.
