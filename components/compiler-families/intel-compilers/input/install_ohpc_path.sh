#!/bin/bash

# Install from release rpms into standard OpenHPC path

delim=ohpc
pubdir=/opt/${delim}/pub

version=16.0.0-109
release_dir=parallel_studio_xe_2016_composer_edition

#skip_keys='i486.rpm$|/intel-ipp|/intel-mkl-pgi'
skip_keys='i486.rpm$|intel-vtune-amplifier|intel-mpi|clck_|intel-advisor|intel-inspector|intel-itac|intel-tc-|intel-ta-'
INSTALL=1
TAR=1
UNINSTALL=0
DEVEL=1

# Devel RPMs

for rpm in `ls $release_dir/rpm/*.rpm` ; do 

    echo $rpm | egrep -q "$skip_keys" 
    if [ $? -eq 0 ];then
        echo "  --> skipping potential install of $rpm"
        continue
    fi

    echo $rpm | egrep -q '\-devel\-\S*.rpm'
    if [ $? -eq 0 ];then
        if [ $DEVEL -eq 1 ];then
            echo "  (devel) $rpm found"
        else
            echo "  --> skipping potential install of (devel) $rpm"
            continue
        fi
    else
        if [ $DEVEL -eq 0 ];then
            echo "  (non-devel) $rpm found"
        else
            echo "  --> skipping potential install of (non-devel) $rpm"
            continue
        fi
    fi


    if [ $INSTALL -eq 1 ];then
        echo "--> installing $rpm...."
        rpm -ivh --nodeps --relocate /opt/intel=${pubdir}/compiler/intel $rpm
    fi

    if [ $UNINSTALL -eq 1 ];then
	localrpm=`basename --suffix=.rpm $rpm`
        echo "--> uninstalling $localrpm ...."
        rpm -e --nodeps $localrpm
    fi
done

if [ $TAR -eq 1 ];then
    if [ $DEVEL -eq 1 ];then
        echo "creating devel tarball..."
        tar cfz intel-compilers-devel-${delim}-$version.tar.gz ${pubdir}/compiler/intel
    else
        echo "creating runtime tarball..."
        tar cfz intel-compilers-${delim}-$version.tar.gz ${pubdir}/compiler/intel
    fi

fi


