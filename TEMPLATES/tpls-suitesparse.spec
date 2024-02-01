Name:           tpls-%{tpls_flavor}-suitesparse
Version:        7.5.1
Release:        1%{?dist}
Summary:        A collection of sparse matrix libraries

License:        (LGPLv2+ or BSD) and LGPLv2+ and GPLv2+
URL:            http://faculty.cse.tamu.edu/davis/suitesparse.html
Source0:        https://github.com/DrTimothyAldenDavis/SuiteSparse/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  tpls-%{tpls_flavor}-cmake
BuildRequires:  tpls-%{tpls_flavor}-gmp
BuildRequires:  tpls-%{tpls_flavor}-mpfr
BuildRequires:  tpls-%{tpls_flavor}-metis
Requires:  tpls-%{tpls_flavor}-gmp
Requires:  tpls-%{tpls_flavor}-mpfr
Requires:  tpls-%{tpls_flavor}-metis

%description
suitesparse is a collection of libraries for computations involving sparse
matrices.  The package includes the following libraries:
  AMD                 approximate minimum degree ordering
  BTF                 permutation to block triangular form (beta)
  CAMD                constrained approximate minimum degree ordering
  COLAMD              column approximate minimum degree ordering
  CCOLAMD             constrained column approximate minimum degree ordering
  CHOLMOD             sparse Cholesky factorization
  CSparse             a concise sparse matrix package
  CXSparse            CSparse extended: complex matrix, int and long int support
  KLU                 sparse LU factorization, primarily for circuit simulation
  LDL                 a simple LDL factorization
  SQPR                a multithread, multifrontal, rank-revealing sparse QR
                      factorization method
  UMFPACK             sparse LU factorization
  SuiteSparse_config  configuration file for all the above packages.
  RBio                read/write files in Rutherford/Boeing format

%prep
%setup -q -n SuiteSparse-%{version}

%build

%{expand: %setup_tpls_env}


%{tpls_env} %tpls_cmake  \
	-DCMAKE_C_COMPILER=%{tpls_cc} \
    -DCMAKE_C_FLAGS="%{tpls_cflags}" \
    -DCMAKE_CXX_COMPILER=%{tpls_cxx} \
    -DCMAKE_CXX_FLAGS="%{tpls_cxxflags}" \
    -DCMAKE_Fortran_COMPILER=%{tpls_fc} \
    -DCMAKE_Fortran_FLAGS="%{tpls_fcflags}" \
%if "%{tpls_gpu}" == "lapack"
	-DBLA_VENDOR="Generic" \
%elif "%{tpls_cc}" == "nvc"
	-DBLA_VENDOR="NVHPC" \
%elif "%{tpls_int}" == "32"
	-DBLA_VENDOR="Intel10_64lp" \
%else
	-DBLA_VENDOR="Intel10_64ilp" \
%endif
%if "%{tpls_libs}" == "static"
	-DBLA_STATIC=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DBUILD_STATIC_LIBS=ON \
%else
	-DBLA_STATIC=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_STATIC_LIBS=OFF \
%if "%{tpls_compiler}" == "intel"
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib -L%{tpls_comproot}/lib -Wl,-rpath,%{tpls_comproot}/lib" \
%else
	-DCMAKE_SHARED_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
	-DCMAKE_EXE_LINKER_FLAGS="-L%{tpls_prefix}/lib -Wl,-rpath,%{tpls_prefix}/lib" \
%endif
%endif
	-DSUITESPARSE_USE_CUDA=OFF \
%if "%{tpls_int}" == "32"
	-DSUITESPARSE_USE_64BIT_BLAS=OFF \
%else
	-DSUITESPARSE_USE_64BIT_BLAS=ON \
%endif
	-DBUILD_TESTING=ON

%make_build

%install
%make_install
%{tpls_remove_la_files}

%files
%{tpls_prefix}/bin/suitesparse_mongoose
%{tpls_prefix}/include/suitesparse/GraphBLAS.h
%{tpls_prefix}/include/suitesparse/LAGraph.h
%{tpls_prefix}/include/suitesparse/LAGraphX.h
%{tpls_prefix}/include/suitesparse/Mongoose.hpp
%{tpls_prefix}/include/suitesparse/ParU.hpp
%{tpls_prefix}/include/suitesparse/ParU_C.h
%{tpls_prefix}/include/suitesparse/ParU_definitions.h
%{tpls_prefix}/include/suitesparse/RBio.h
%{tpls_prefix}/include/suitesparse/SPEX.h
%{tpls_prefix}/include/suitesparse/SuiteSparseQR.hpp
%{tpls_prefix}/include/suitesparse/SuiteSparseQR_C.h
%{tpls_prefix}/include/suitesparse/SuiteSparseQR_definitions.h
%{tpls_prefix}/include/suitesparse/SuiteSparse_config.h
%{tpls_prefix}/include/suitesparse/amd.h
%{tpls_prefix}/include/suitesparse/btf.h
%{tpls_prefix}/include/suitesparse/camd.h
%{tpls_prefix}/include/suitesparse/ccolamd.h
%{tpls_prefix}/include/suitesparse/cholmod.h
%{tpls_prefix}/include/suitesparse/colamd.h
%{tpls_prefix}/include/suitesparse/cs.h
%{tpls_prefix}/include/suitesparse/klu.h
%{tpls_prefix}/include/suitesparse/klu_cholmod.h
%{tpls_prefix}/include/suitesparse/ldl.h
%{tpls_prefix}/include/suitesparse/umfpack.h
%{tpls_prefix}/lib/cmake/AMD/AMDConfig.cmake
%{tpls_prefix}/lib/cmake/AMD/AMDConfigVersion.cmake
%{tpls_prefix}/lib/cmake/AMD/AMDTargets-release.cmake
%{tpls_prefix}/lib/cmake/AMD/AMDTargets.cmake
%{tpls_prefix}/lib/cmake/BTF/BTFConfig.cmake
%{tpls_prefix}/lib/cmake/BTF/BTFConfigVersion.cmake
%{tpls_prefix}/lib/cmake/BTF/BTFTargets-release.cmake
%{tpls_prefix}/lib/cmake/BTF/BTFTargets.cmake
%{tpls_prefix}/lib/cmake/CAMD/CAMDConfig.cmake
%{tpls_prefix}/lib/cmake/CAMD/CAMDConfigVersion.cmake
%{tpls_prefix}/lib/cmake/CAMD/CAMDTargets-release.cmake
%{tpls_prefix}/lib/cmake/CAMD/CAMDTargets.cmake
%{tpls_prefix}/lib/cmake/CCOLAMD/CCOLAMDConfig.cmake
%{tpls_prefix}/lib/cmake/CCOLAMD/CCOLAMDConfigVersion.cmake
%{tpls_prefix}/lib/cmake/CCOLAMD/CCOLAMDTargets-release.cmake
%{tpls_prefix}/lib/cmake/CCOLAMD/CCOLAMDTargets.cmake
%{tpls_prefix}/lib/cmake/CHOLMOD/CHOLMODConfig.cmake
%{tpls_prefix}/lib/cmake/CHOLMOD/CHOLMODConfigVersion.cmake
%{tpls_prefix}/lib/cmake/CHOLMOD/CHOLMODTargets-release.cmake
%{tpls_prefix}/lib/cmake/CHOLMOD/CHOLMODTargets.cmake
%{tpls_prefix}/lib/cmake/COLAMD/COLAMDConfig.cmake
%{tpls_prefix}/lib/cmake/COLAMD/COLAMDConfigVersion.cmake
%{tpls_prefix}/lib/cmake/COLAMD/COLAMDTargets-release.cmake
%{tpls_prefix}/lib/cmake/COLAMD/COLAMDTargets.cmake
%{tpls_prefix}/lib/cmake/CXSparse/CXSparseConfig.cmake
%{tpls_prefix}/lib/cmake/CXSparse/CXSparseConfigVersion.cmake
%{tpls_prefix}/lib/cmake/CXSparse/CXSparseTargets-release.cmake
%{tpls_prefix}/lib/cmake/CXSparse/CXSparseTargets.cmake
%{tpls_prefix}/lib/cmake/GraphBLAS/GraphBLASConfig.cmake
%{tpls_prefix}/lib/cmake/GraphBLAS/GraphBLASConfigVersion.cmake
%{tpls_prefix}/lib/cmake/GraphBLAS/GraphBLASTargets-release.cmake
%{tpls_prefix}/lib/cmake/GraphBLAS/GraphBLASTargets.cmake
%{tpls_prefix}/lib/cmake/KLU/KLUConfig.cmake
%{tpls_prefix}/lib/cmake/KLU/KLUConfigVersion.cmake
%{tpls_prefix}/lib/cmake/KLU/KLUTargets-release.cmake
%{tpls_prefix}/lib/cmake/KLU/KLUTargets.cmake
%{tpls_prefix}/lib/cmake/KLU_CHOLMOD/KLU_CHOLMODConfig.cmake
%{tpls_prefix}/lib/cmake/KLU_CHOLMOD/KLU_CHOLMODConfigVersion.cmake
%{tpls_prefix}/lib/cmake/KLU_CHOLMOD/KLU_CHOLMODTargets-release.cmake
%{tpls_prefix}/lib/cmake/KLU_CHOLMOD/KLU_CHOLMODTargets.cmake
%{tpls_prefix}/lib/cmake/LAGraph/FindGraphBLAS.cmake
%{tpls_prefix}/lib/cmake/LAGraph/LAGraphConfig.cmake
%{tpls_prefix}/lib/cmake/LAGraph/LAGraphConfigVersion.cmake
%{tpls_prefix}/lib/cmake/LAGraph/LAGraphTargets-release.cmake
%{tpls_prefix}/lib/cmake/LAGraph/LAGraphTargets.cmake
%{tpls_prefix}/lib/cmake/LDL/LDLConfig.cmake
%{tpls_prefix}/lib/cmake/LDL/LDLConfigVersion.cmake
%{tpls_prefix}/lib/cmake/LDL/LDLTargets-release.cmake
%{tpls_prefix}/lib/cmake/LDL/LDLTargets.cmake
%{tpls_prefix}/lib/cmake/ParU/ParUConfig.cmake
%{tpls_prefix}/lib/cmake/ParU/ParUConfigVersion.cmake
%{tpls_prefix}/lib/cmake/ParU/ParUTargets-release.cmake
%{tpls_prefix}/lib/cmake/ParU/ParUTargets.cmake
%{tpls_prefix}/lib/cmake/RBio/RBioConfig.cmake
%{tpls_prefix}/lib/cmake/RBio/RBioConfigVersion.cmake
%{tpls_prefix}/lib/cmake/RBio/RBioTargets-release.cmake
%{tpls_prefix}/lib/cmake/RBio/RBioTargets.cmake
%{tpls_prefix}/lib/cmake/SPEX/FindGMP.cmake
%{tpls_prefix}/lib/cmake/SPEX/FindMPFR.cmake
%{tpls_prefix}/lib/cmake/SPEX/SPEXConfig.cmake
%{tpls_prefix}/lib/cmake/SPEX/SPEXConfigVersion.cmake
%{tpls_prefix}/lib/cmake/SPEX/SPEXTargets-release.cmake
%{tpls_prefix}/lib/cmake/SPEX/SPEXTargets.cmake
%{tpls_prefix}/lib/cmake/SPQR/SPQRConfig.cmake
%{tpls_prefix}/lib/cmake/SPQR/SPQRConfigVersion.cmake
%{tpls_prefix}/lib/cmake/SPQR/SPQRTargets-release.cmake
%{tpls_prefix}/lib/cmake/SPQR/SPQRTargets.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse/SuiteSparseBLAS.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse/SuiteSparseBLAS32.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse/SuiteSparseBLAS64.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse/SuiteSparseLAPACK.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse/SuiteSparsePolicy.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse/SuiteSparseReport.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse/SuiteSparse__thread.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse_Mongoose/SuiteSparse_MongooseConfig.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse_Mongoose/SuiteSparse_MongooseConfigVersion.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse_Mongoose/SuiteSparse_MongooseTargets-release.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse_Mongoose/SuiteSparse_MongooseTargets.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse_config/SuiteSparse_configConfig.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse_config/SuiteSparse_configConfigVersion.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse_config/SuiteSparse_configTargets-release.cmake
%{tpls_prefix}/lib/cmake/SuiteSparse_config/SuiteSparse_configTargets.cmake
%{tpls_prefix}/lib/cmake/UMFPACK/UMFPACKConfig.cmake
%{tpls_prefix}/lib/cmake/UMFPACK/UMFPACKConfigVersion.cmake
%{tpls_prefix}/lib/cmake/UMFPACK/UMFPACKTargets-release.cmake
%{tpls_prefix}/lib/cmake/UMFPACK/UMFPACKTargets.cmake
%if "%{tpls_libs}" == "static"
%{tpls_prefix}/lib/libamd.a
%{tpls_prefix}/lib/libbtf.a
%{tpls_prefix}/lib/libcamd.a
%{tpls_prefix}/lib/libccolamd.a
%{tpls_prefix}/lib/libcholmod.a
%{tpls_prefix}/lib/libcolamd.a
%{tpls_prefix}/lib/libcxsparse.a
%{tpls_prefix}/lib/libgraphblas.a
%{tpls_prefix}/lib/libklu.a
%{tpls_prefix}/lib/libklu_cholmod.a
%{tpls_prefix}/lib/liblagraph.a
%{tpls_prefix}/lib/liblagraphx.a
%{tpls_prefix}/lib/libldl.a
%{tpls_prefix}/lib/libparu.a
%{tpls_prefix}/lib/librbio.a
%{tpls_prefix}/lib/libspex.a
%{tpls_prefix}/lib/libspqr.a
%{tpls_prefix}/lib/libsuitesparse_mongoose.a
%{tpls_prefix}/lib/libsuitesparseconfig.a
%{tpls_prefix}/lib/libumfpack.a
%else
%{tpls_prefix}/lib/libamd.so
%{tpls_prefix}/lib/libamd.so.*
%{tpls_prefix}/lib/libbtf.so
%{tpls_prefix}/lib/libbtf.so.*
%{tpls_prefix}/lib/libcamd.so
%{tpls_prefix}/lib/libcamd.so.*
%{tpls_prefix}/lib/libccolamd.so
%{tpls_prefix}/lib/libccolamd.so.*
%{tpls_prefix}/lib/libcholmod.so
%{tpls_prefix}/lib/libcholmod.so.*
%{tpls_prefix}/lib/libcolamd.so
%{tpls_prefix}/lib/libcolamd.so.*
%{tpls_prefix}/lib/libcxsparse.so
%{tpls_prefix}/lib/libcxsparse.so.*
%{tpls_prefix}/lib/libgraphblas.so
%{tpls_prefix}/lib/libgraphblas.so.*
%{tpls_prefix}/lib/libklu.so
%{tpls_prefix}/lib/libklu.so.*
%{tpls_prefix}/lib/libklu_cholmod.so
%{tpls_prefix}/lib/libklu_cholmod.so.*
%{tpls_prefix}/lib/liblagraph.so
%{tpls_prefix}/lib/liblagraph.so.*
%{tpls_prefix}/lib/liblagraphx.so
%{tpls_prefix}/lib/liblagraphx.so.*
%{tpls_prefix}/lib/libldl.so
%{tpls_prefix}/lib/libldl.so.*
%{tpls_prefix}/lib/libparu.so
%{tpls_prefix}/lib/libparu.so.*
%{tpls_prefix}/lib/librbio.so
%{tpls_prefix}/lib/librbio.so.*
%{tpls_prefix}/lib/libspex.so
%{tpls_prefix}/lib/libspex.so.*
%{tpls_prefix}/lib/libspqr.so
%{tpls_prefix}/lib/libspqr.so.*
%{tpls_prefix}/lib/libsuitesparse_mongoose.so
%{tpls_prefix}/lib/libsuitesparse_mongoose.so.*
%{tpls_prefix}/lib/libsuitesparseconfig.so
%{tpls_prefix}/lib/libsuitesparseconfig.so.*
%{tpls_prefix}/lib/libumfpack.so
%{tpls_prefix}/lib/libumfpack.so.*
%endif
%{tpls_prefix}/lib/pkgconfig/AMD.pc
%{tpls_prefix}/lib/pkgconfig/BTF.pc
%{tpls_prefix}/lib/pkgconfig/CAMD.pc
%{tpls_prefix}/lib/pkgconfig/CCOLAMD.pc
%{tpls_prefix}/lib/pkgconfig/CHOLMOD.pc
%{tpls_prefix}/lib/pkgconfig/COLAMD.pc
%{tpls_prefix}/lib/pkgconfig/CXSparse.pc
%{tpls_prefix}/lib/pkgconfig/GraphBLAS.pc
%{tpls_prefix}/lib/pkgconfig/KLU.pc
%{tpls_prefix}/lib/pkgconfig/KLU_CHOLMOD.pc
%{tpls_prefix}/lib/pkgconfig/LAGraph.pc
%{tpls_prefix}/lib/pkgconfig/LDL.pc
%{tpls_prefix}/lib/pkgconfig/ParU.pc
%{tpls_prefix}/lib/pkgconfig/RBio.pc
%{tpls_prefix}/lib/pkgconfig/SPEX.pc
%{tpls_prefix}/lib/pkgconfig/SPQR.pc
%{tpls_prefix}/lib/pkgconfig/SuiteSparse_Mongoose.pc
%{tpls_prefix}/lib/pkgconfig/SuiteSparse_config.pc
%{tpls_prefix}/lib/pkgconfig/UMFPACK.pc


%changelog
* Wed Jan 24 2024 Christian Messe <cmesse@lbl.gov> - 7.5.1-1
- Initial Package
