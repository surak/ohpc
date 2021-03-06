#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%include %{_sourcedir}/OHPC_macros
%{!?PROJ_DELIM: %define PROJ_DELIM -ohpc}

%define pname intel-compilers

Summary:   Intel(R) Parallel Studio XE
Name:      %{pname}%{PROJ_DELIM}
Version:   16.0.109
Release:   1
License:   Intel(R)
URL:       https://software.intel.com/en-us/intel-parallel-studio-xe
Group:     ohpc/compiler-families
BuildArch: x86_64
Source0:   intel-compilers%{PROJ_DELIM}-16.0.0-109.tar.gz
Source1:   OHPC_macros
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
AutoReq: no

%define __spec_install_post /usr/lib/rpm/brp-strip-comment-note /bin/true
%define __spec_install_post /usr/lib/rpm/brp-compress /bin/true
%define __spec_install_post /usr/lib/rpm/brp-strip /bin/true

requires: gcc-c++

#!BuildIgnore: post-build-checks rpmlint-Factory
%define debug_package %{nil}

%define composer_release compilers_and_libraries_20%{version}
%define package_target %{OHPC_COMPILERS}/intel

%define module_version  16.0.0.109

%description

OpenHPC collection of runtime packages for Intel(R) Parallel Studio
compiler suite (including compilers for C,C++, and Fortran).


%prep

%build

%install

%{__mkdir} -p %{buildroot}/
cd %{buildroot}
%{__tar} xfz %{SOURCE0}

cd -

# OpenHPC module file
%{__mkdir} -p %{buildroot}/%{OHPC_MODULES}/intel
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/intel/%{module_version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "See the man pages for icc, icpc, and ifort for detailed information"
puts stderr "on available compiler options and command-line syntax."

puts stderr "\nVersion %{module_version}\n"

}

module-whatis "Name: Intel Compiler"
module-whatis "Version: %{version}"
module-whatis "Category: compiler, runtime support"
module-whatis "Description: Intel Compiler Family (C/C++/Fortran for x86_64)"
module-whatis "URL: http://software.intel.com/en-us/articles/intel-compilers/"

set     version			    %{version}

# update module path hierarchy
prepend-path    MODULEPATH          %{OHPC_MODULEDEPS}/intel

prepend-path    PATH                %{package_target}/compilers_and_libraries_20%{version}/linux/bin/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/mpirt/bin/intel64_lin:%{package_target}/debugger_2016/gdb/intel64_mic/bin
prepend-path    MANPATH             %{package_target}/documentation_2016/en/man/common/:%{package_target}/documentation_2016/en/debugger/gdb-ia/man/:%{package_target}/documentation_2016/en/debugger/gdb-mic/man/:%{package_target}/documentation_2016/en/debugger/gdb-igfx/man/:

setenv          MKLROOT             %{package_target}/compilers_and_libraries_20%{version}/linux/mkl
prepend-path    CPATH               %{package_target}/compilers_and_libraries_20%{version}/linux/mkl/include:%{package_target}/compilers_and_libraries_20%{version}/linux/mkl/include/intel64/lp64
prepend-path    NLSPATH             %{package_target}/compilers_and_libraries_20%{version}/linux/mkl/lib/intel64/locale/en_US
 
prepend-path    LIBRARY_PATH        %{package_target}/compilers_and_libraries_20%{version}/linux/ipp/../compiler/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/ipp/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/compiler/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/mkl/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/tbb/lib/intel64/gcc4.4:%{package_target}/compilers_and_libraries_20%{version}/linux/daal/lib/intel64_lin:%{package_target}/compilers_and_libraries_20%{version}/linux/daal/../tbb/lib/intel64_lin/gcc4.4:%{package_target}/compilers_and_libraries_20%{version}/linux/daal/../compiler/lib/intel64_lin
prepend-path    LD_LIBRARY_PATH     %{package_target}/compilers_and_libraries_20%{version}/linux/compiler/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/mpirt/lib/intel64_lin:%{package_target}/compilers_and_libraries_20%{version}/linux/ipp/../compiler/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/ipp/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/compiler/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/mkl/lib/intel64:%{package_target}/compilers_and_libraries_20%{version}/linux/tbb/lib/intel64/gcc4.4:%{package_target}/debugger_2016/libipt/intel64/lib:%{package_target}/compilers_and_libraries_20%{version}/linux/daal/lib/intel64_lin:%{package_target}/compilers_and_libraries_20%{version}/linux/daal/../tbb/lib/intel64_lin/gcc4.4:%{package_target}/compilers_and_libraries_20%{version}/linux/daal/../compiler/lib/intel64_lin

prepend-path    MIC_LD_LIBRARY_PATH %{package_target}/compilers_and_libraries_20%{version}/linux/compiler/lib/mic:%{package_target}/compilers_and_libraries_20%{version}/linux/compiler/lib/mic:%{package_target}/compilers_and_libraries_20%{version}/linux/mkl/lib/mic:%{package_target}/compilers_and_libraries_20%{version}/linux/tbb/lib/mic

setenv          GDBSERVER_MIC       %{package_target}/debugger_2016/gdb/targets/mic/bin/gdbserver
setenv          GDB_CROSS           %{package_target}/debugger_2016/gdb/intel64_mic/bin/gdb-mic
setenv          INTEL_PYTHONHOME    %{package_target}/debugger_2016/python/intel64/
setenv          MPM_LAUNCHER        %{package_target}/debugger_2016/mpm/mic/bin/start_mpm.sh
setenv          TBBROOT             %{package_target}/compilers_and_libraries_20%{version}/linux/tbb
setenv          TBB_INC             %{package_target}/compilers_and_libraries_20%{version}/linux/tbb/include
setenv          TBB_LIB             %{package_target}/compilers_and_libraries_20%{version}/linux/tbb/lib/intel64/gcc4.4
prepend-path    CPATH               %{package_target}/compilers_and_libraries_20%{version}/linux/tbb/include

family "compiler"
EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/intel/.version.%{module_version}
#%Module1.0#####################################################################
set     ModulesVersion      "%{module_version}"
EOF

# Provide standalone module for use with GNU toolchain

%{__mkdir} -p %{buildroot}/%{OHPC_MODULEDEPS}/gnu/mkl
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/gnu/mkl/%{module_version}
#%Module1.0#####################################################################

proc ModulesHelp { } {

puts stderr " "
puts stderr "Sets MKLROOT environment variable"
puts stderr " "
puts stderr "%{module_version}"

}

module-whatis "Name: Intel Math Kernel Library"
module-whatis "Version: %{version}"
module-whatis "Category: library, runtime support"
module-whatis "Description: Intel Math Kernel Library for C/C++ and Fortran"
module-whatis "URL: https://software.intel.com/en-us/en-us/intel-mkl"

setenv	        MKLROOT 	    %{package_target}/compilers_and_libraries_20%{version}/linux/mkl
prepend-path    LD_LIBRARY_PATH     %{package_target}/compilers_and_libraries_20%{version}/linux/mkl/lib/intel64

EOF

export NO_BRP_CHECK_RPATH true

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{OHPC_HOME}

%changelog

