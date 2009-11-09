#%%define Werror_cflags %nil

Summary:	StrongSWAN IPSEC implementation
Name:		strongswan
Version:	4.3.5
Release:	%mkrel 1
License:	GPL
URL:		http://www.strongswan.org/
Source0:	http://download.strongswan.org/%{name}-%{version}.tar.bz2
Source1:	strongswan.init
Patch0:		strongswan-4.2.14-format_not_a_string_literal_and_no_format_arguments.diff
Group:		System/Servers
BuildRequires:	libgmp-devel
BuildRequires:	libldap-devel
BuildRequires:	libcurl-devel
BuildRequires:	opensc-devel
BuildRequires:  libxml2-devel
BuildRequires:  libfcgi-devel
Requires:	libopensc2
Requires(post): rpm-helper
Requires(preun): rpm-helper
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
%patch0 -p0

%build
%serverbuild

%configure2_5x \
    --disable-self-test	\
    --enable-smartcard \
    --enable-cisco-quirks \
    --enable-ldap \
    --with-default-pkcs11=%{_libdir}/opensc-pkcs11.so

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/ipsec.d/{cacerts,crls,private,certs,acerts,aacerts,ocspcerts}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/run/pluto


make install DESTDIR=%{buildroot}

# (fg) File is copied over here
install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/ipsec

#mv %{buildroot}%{_sysconfdir}/ipsec.conf %{buildroot}%{_sysconfdir}/%{source_name}/

rm -f %{buildroot}%{_libdir}/libstrongswan.{so,a,la}
find  %{buildroot}%{_libdir}/ipsec -name "*.a" -o -name "*.la" | xargs -r rm -f

#%pre
#%_pre_useradd strongswan

%post
%_post_service ipsec


%preun
%_preun_service ipsec

#%postun
#%_postun_userdel strongswan

#
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc TODO NEWS README COPYING CREDITS
%attr(700,root,root) %dir %{_sysconfdir}/ipsec.d/
%attr(700,root,root) %dir %{_sysconfdir}/ipsec.d/acerts
%attr(700,root,root) %dir %{_sysconfdir}/ipsec.d/aacerts
%attr(700,root,root) %dir %{_sysconfdir}/ipsec.d/ocspcerts
%attr(700,root,root) %dir %{_sysconfdir}/ipsec.d/certs
%attr(700,root,root) %dir %{_sysconfdir}/ipsec.d/cacerts
%attr(700,root,root) %dir %{_sysconfdir}/ipsec.d/crls
%attr(700,root,root) %dir %{_sysconfdir}/ipsec.d/private
%config(noreplace) %{_sysconfdir}/ipsec.conf
%{_initrddir}/ipsec
%config(noreplace) %{_sysconfdir}/strongswan.conf
%{_libdir}/ipsec
%{_mandir}/man*/*
%{_libdir}/libstrongswan.*
%{_sbindir}/ipsec
