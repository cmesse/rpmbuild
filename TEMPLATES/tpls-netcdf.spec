Name:           tpls-%{tpls_flavor}-netcdf
Version:        4.9.2
Release:        1%{?dist}
Summary:        Libraries for the Unidata network Common Data Form

License:        NetCDF
URL:            http://www.unidata.ucar.edu/software/netcdf/
Source0:        https://downloads.unidata.ucar.edu/netcdf-c/%{version}/netcdf-c-%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake
BuildRequires:  tpls-%{tpls_flavor}-hdf5

%if   "%{tpls_mpi}" == "openempi"
BuildRequires:  tpls-%{tpls_flavor}-openmpi
Requires:       tpls-%{tpls_flavor}-openmpi
%elif "%{tpls_mpi}" == "mpich"
BuildRequires:  tpls-%{tpls_flavor}-mpich
Requires:       tpls-%{tpls_flavor}-mpich
%elif "%{tpls_mpi}" == "intelmpi"
BuildRequires:  intel-oneapi-mpi
BuildRequires:  intel-oneapi-mpi-devel
BuildRequires:  intel-oneapi-mpi
%endif

BuildRequires:  libcurl-devel
Requires:  libcurl
Requires:  tpls-%{tpls_flavor}-hdf5

%description
NetCDF (network Common Data Form) is an interface for array-oriented 
data access and a freely-distributed collection of software libraries 
for C, Fortran, C++, and perl that provides an implementation of the 
interface.  The NetCDF library also defines a machine-independent 
format for representing scientific data.  Together, the interface, 
library, and format support the creation, access, and sharing of 
scientific data. The NetCDF software was developed at the Unidata 
Program Center in Boulder, Colorado.

NetCDF data is: 

   o Self-Describing: A NetCDF file includes information about the
     data it contains.

   o Network-transparent:  A NetCDF file is represented in a form that
     can be accessed by computers with different ways of storing
     integers, characters, and floating-point numbers.

   o Direct-access:  A small subset of a large dataset may be accessed
     efficiently, without first reading through all the preceding
     data.

   o Appendable:  Data can be appended to a NetCDF dataset along one
     dimension without copying the dataset or redefining its
     structure. The structure of a NetCDF dataset can be changed,
     though this sometimes causes the dataset to be copied.

   o Sharable:  One writer and multiple readers may simultaneously
     access the same NetCDF file.


%prep
%setup -q -n netcdf-c-%{version}

%build
%{expand: %setup_tpls_env}

mkdir build && cd build
%{tpls_env} \
%{tpls_cmake} \
	-DCMAKE_C_AR=%{tpls_ar} \
    -DCMAKE_C_COMPILER=%{tpls_mpicc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_mpicxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
	-DENABLE_DAP=OFF \
	-DENABLE_DAP2=OFF \
	-DENABLE_DAP4=OFF \
	-DENABLE_EXAMPLES=OFF \
	-DENABLE_HDF4=OFF \
	-DENABLE_HDF5=ON \
	-DENABLE_LIBXML2=OFF \
	-DENABLE_DISKLESS=OFF \
	-DENABLE_PLUGINS=OFF \
	-DENABLE_NCZARR=OFF \
	-DENABLE_FILTER_TESTING=OFF \
	-DHDF5_C_COMPILER_EXECUTABLE=%{tpls_prefix}/bin/h5cc \
	-DHDF5_C_INCLUDE_DIR=%{tpls_prefix}/include \
	-DHDF5_DIFF_EXECUTABLE=%{tpls_prefix}/bin/h5diff \
	-DHDF5_DIR=%{tpls_prefix} \
%if "%{tpls_libs}" == "static"
	-DHDF5_hdf5_LIBRARY_RELEASE=%{tpls_prefix}/lib/libhdf5.a \
	-DHDF5_hdf5_hl_LIBRARY_RELEASE=%{tpls_prefix}/lib/libhdf5_hl.a \
	-DBUILD_STATIC_LIBS=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DCMAKE_STATIC_LINKER_FLAGS="-L%{tpls_prefix}/lib" \
%else
	-DHDF5_hdf5_LIBRARY_RELEASE=%{tpls_prefix}/lib/libhdf5.so \
	-DHDF5_hdf5_hl_LIBRARY_RELEASE=%{tpls_prefix}/lib/libhdf5_hl.so \
	-DBUILD_STATIC_LIBS=OFF \
	-DBUILD_SHARED_LIBS=ON \
%if "%{tpls_compiler}" == "intel"
%if "%{tpls_mpi}" == "intelmpi"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mpiproot}/lib -Wl,-rpath,%{tpls_mpiproot}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_mpiproot}/lib -Wl,-rpath,%{tpls_mpiroot}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%endif
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
%endif	
%endif
	..

%make_build

#%check
#cd build
#%if "%{tpls_compiler}" == "intel"
#%if "%{tpls_mpi}" == "intelmpi"
#LD_LIBRARY_PATH="%{tpls_prefix}/lib:%{tpls_mpiroot}/lib:%{tpls_comproot}/lib"  %make_build test
#%else
#LD_LIBRARY_PATH="%{tpls_prefix}/lib:%{tpls_comproot}/lib"  %make_build test
#%endif
#%else
#LD_LIBRARY_PATH="%{tpls_prefix}/lib"  %make_build test
#%endif

%install
cd build
%make_install
 
%files
%{tpls_prefix}/bin/nc-config
%{tpls_prefix}/bin/nccopy
%{tpls_prefix}/bin/ncdump
%{tpls_prefix}/bin/ncgen
%{tpls_prefix}/bin/ncgen3
%{tpls_prefix}/include/netcdf.h
%{tpls_prefix}/include/netcdf_aux.h
%{tpls_prefix}/include/netcdf_dispatch.h
%{tpls_prefix}/include/netcdf_filter.h
%{tpls_prefix}/include/netcdf_filter_build.h
%{tpls_prefix}/include/netcdf_json.h
%{tpls_prefix}/include/netcdf_mem.h
%{tpls_prefix}/include/netcdf_meta.h
%{tpls_prefix}/include/netcdf_par.h
%{tpls_prefix}/lib/cmake/netCDF
%{tpls_prefix}/lib/libnetcdf.settings
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libnetcdf.a
%else
%{tpls_prefix}/lib/libnetcdf.so
%{tpls_prefix}/lib/libnetcdf.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/netcdf.pc
%{tpls_prefix}/share/man/man1/nccopy.1
%{tpls_prefix}/share/man/man1/ncdump.1
%{tpls_prefix}/share/man/man1/ncgen.1
%{tpls_prefix}/share/man/man1/ncgen3.1
%{tpls_prefix}/share/man/man3/netcdf.3

%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 4.9.2-1
- Initial Package
