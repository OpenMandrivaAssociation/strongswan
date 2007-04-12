%define name	strongswan
%define version 2.8.3
%define release %mkrel 2

%define source_name freeswan

Summary:	StrongSWAN IPSEC implementation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://www.strongswan.org/
Source0:	%{name}-%{version}.tar.bz2
Source1:	freeswan.init
Patch0:		strongswan-2.8.3-libdir.patch
Group:		System/Servers
BuildRequires:	libgmp-devel
BuildRequires:	libldap-devel
BuildRequires:	libcurl-devel
BuildRequires:	opensc-devel
Requires:	ipsec-tools
PreReq:		rpm-helper
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description 
FreeS/WAN is a free implementation of IPSEC & IKE for Linux.  IPSEC is 
the Internet Protocol Security and uses strong cryptography to provide
both authentication and encryption services.  These services allow you
to build secure tunnels through untrusted networks.  Everything passing
through the untrusted net is encrypted by the ipsec gateway machine and 
decrypted by the gateway at the other end of the tunnel.  The resulting
tunnel is a virtual private network or VPN.

This package contains the daemons and userland tools for setting up
FreeS/WAN on a freeswan enabled kernel.

%prep

%setup -q -n %{name}-%{version}
%patch0 -p1 -b .libdir

# enable LDAP v3 support
perl -pi -e "s,#LDAP_VERSION=3,LDAP_VERSION=3,g" %{_builddir}/%{name}-%{version}/programs/pluto/Makefile

# enable smartcard support
perl -pi -e "s,#SMARTCARD=1,SMARTCARD=1,g" %{_builddir}/%{name}-%{version}/programs/pluto/Makefile

# enable OCSP and dynamic CRL fetching using HTTP or FTP
perl -pi -e "s,#LIBCURL=1,LIBCURL=1,g" %{_builddir}/%{name}-%{version}/programs/pluto/Makefile

# change some default settings
find . -type f | xargs perl -pi -e "s,/usr/local/man,%{_mandir},g"
find . -type f | xargs perl -pi -e "s,/usr/local,%{_prefix},g"
find . -type f | xargs perl -pi -e "s,/libexec/ipsec,/lib/ipsec,g"
find . -type f | xargs perl -pi -e "s,/etc/ipsec.conf,/etc/freeswan/ipsec.conf,g"
find . -type f | xargs perl -pi -e "s,/etc/ipsec.secrets,/etc/freeswan/ipsec.secrets,g"
find . -type f | xargs perl -pi -e "s,/etc/ipsec.d,/etc/freeswan/ipsec.d,g"

#fix the ipsec_aes commands
find . -type f | xargs perl -pi -e "s,modprobe ipsec_aes,modprobe aes,g"
find . -type f | xargs perl -pi -e "s,rmmod ipsec_aes,rmmod aes,g"

%build

%serverbuild

perl -p -i -e "s|INC_USRLOCAL=/usr/local|INC_USRLOCAL=%{_prefix}|" Makefile.inc
perl -p -i -e "s|INC_USRLOCAL=/libexec/ipsec/|INC_USRLOCAL=%{_lib}/ipsec/|" Makefile.inc

%make \
    OPT_FLAGS="%{optflags}" \
    CONFDIR=%{_sysconfdir}/freeswan/ \
    FINALLIBEXECDIR=%{_libdir}/ipsec \
    FINALLIBDIR=%{_libdir}/ipsec \
    FINALCONFDIR=%{_sysconfdir}/freeswan \
    FINALCONFFILE=%{_sysconfdir}/ipsec.conf \
    INC_USRLOCAL=%{_prefix} \
    INC_MANDIR=share/man programs 

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/%{source_name}/ipsec.d/{cacerts,crls,private,certs,acerts,aacerts,ocspcerts}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/run/pluto

make \
    INC_USRLOCAL=%{_prefix} \
    INC_MANDIR=share/man \
    FINALLIBEXECDIR=%{_libdir}/ipsec \
    FINALLIBDIR=%{_libdir}/ipsec \
    FINALEXAMPLECONFDIR=%{_docdir}/%{name}-%{version} \
    CONFDIR="%{buildroot}"%{_sysconfdir}/freeswan \
    DESTDIR="%{buildroot}" \
    install

# (fg) File is copied over here
install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/ipsec

mv %{buildroot}%{_sysconfdir}/ipsec.d/{examples,policies} %{buildroot}%{_sysconfdir}/%{source_name}/ipsec.d/

find . -name ".cvsignore" | xargs rm -rf

%post
is=%{_sysconfdir}/freeswan/ipsec.secrets; if [ ! -f $is ]; then ipsec newhostkey --output $is && chmod 400 $is; else ipsec newhostkey --output $is.rpmnew && chmod 400 $is.rpmnew; fi

%_post_service ipsec 

%preun
%_preun_service ipsec

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc CHANGES CREDITS README
%docdir %{_docdir}/%{name}-%{version}
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/acerts
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/aacerts
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/ocspcerts
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/certs
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/cacerts
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/crls
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/private
%attr(700,root,root) %dir %{_sysconfdir}/%{source_name}/ipsec.d/policies/
%config(noreplace) %{_sysconfdir}/%{source_name}/ipsec.d/examples/*
%config(noreplace) %{_sysconfdir}/%{source_name}/ipsec.d/policies/*
%config(noreplace) %{_sysconfdir}/%{source_name}/ipsec.conf
%config(noreplace) %{_initrddir}/ipsec
%config(noreplace) %{_sysconfdir}/rc.d/*/*
%dir %{_libdir}/ipsec
%{_libdir}/ipsec/*
%{_sbindir}/*
%{_mandir}/*/*


