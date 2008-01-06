%define name	strongswan
%define version 4.1.10
%define release %mkrel 1

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
Patch1:         %{name}_modprobe_syslog.dif
Group:		System/Servers
BuildRequires:	libgmp-devel
BuildRequires:	libldap-devel
BuildRequires:	libcurl-devel
BuildRequires:	opensc-devel
Requires:	ipsec-tools
Requires(post,preun):	rpm-helper

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch1 -p0

%build
#autoreconf
%configure2_5x \
        --enable-smartcard --with-default-pkcs11=%{_libdir}/opensc-pkcs11.so \
        --enable-cisco-quirks   \
        --enable-http           \
        --enable-ldap           \
        --enable-xml            \
        --enable-p2p
#       --enable-dbus
#       --enable-manager

#%make \
#    OPT_FLAGS="%{optflags}" \
#    CONFDIR=%{_sysconfdir}/freeswan/ \
#    FINALLIBEXECDIR=%{_libdir}/ipsec \
#    FINALLIBDIR=%{_libdir}/ipsec \
#    FINALCONFDIR=%{_sysconfdir}/freeswan \
#    FINALCONFFILE=%{_sysconfdir}/ipsec.conf \
#    INC_USRLOCAL=%{_prefix} \
#    INC_MANDIR=share/man
%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/%{source_name}/ipsec.d/{cacerts,crls,private,certs,acerts,aacerts,ocspcerts}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/run/pluto

#%make \
#    INC_USRLOCAL=%{_prefix} \
#    INC_MANDIR=share/man \
#    FINALLIBEXECDIR=%{_libdir}/ipsec \
#    FINALLIBDIR=%{_libdir}/ipsec \
#    FINALEXAMPLECONFDIR=%{_docdir}/%{name} \
#    CONFDIR="%{buildroot}"%{_sysconfdir}/freeswan \
#    DESTDIR="%{buildroot}" \
#    install

%makeinstall_std

# (fg) File is copied over here
install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/ipsec

mv %{buildroot}%{_sysconfdir}/ipsec.conf %{buildroot}%{_sysconfdir}/%{source_name}/

rm -f %{buildroot}%{_libdir}/libstrongswan.{so,a,la}
find  %{buildroot}%{_libdir}/ipsec -name "*.a" -o -name "*.la" | xargs -r rm -f


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
%{_docdir}/%{name}-%{version}/*
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
%{_initrddir}/ipsec
%config(noreplace) %{_sysconfdir}/rc.d/*/*
%dir %{_libdir}/ipsec/*
%{_libdir}/ipsec/*
%{_mandir}/man*/*.lzma
