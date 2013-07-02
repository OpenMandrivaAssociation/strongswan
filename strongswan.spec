#%%define Werror_cflags %nil

Summary:	IPSEC implementation
Name:		strongswan
Version:	5.0.1
Release:	2
License:	GPLv2+
URL:		http://www.strongswan.org/
Source0:	http://download.strongswan.org/%{name}-%{version}.tar.bz2
Source1:	strongswan.init
Patch0:		strongswan-4.5.2-format_not_a_string_literal_and_no_format_arguments.diff
Patch1:		strongswan-5.0.1-rosa-link.patch
Group:		System/Servers
BuildRequires:	gmp-devel
BuildRequires:	libldap-devel
BuildRequires:	curl-devel
BuildRequires:	opensc-devel
BuildRequires:  libxml2-devel
BuildRequires:  libfcgi-devel
BuildRequires:  intltool
Requires:	%{_lib}opensc3
Requires(post): rpm-helper
Requires(preun): rpm-helper

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
%setup -q
#patch0 -p0 -b .str
%patch1 -p1 -b .link

%build
autoreconf
%serverbuild

%configure2_5x \
    --enable-smartcard \
    --enable-cisco-quirks \
    --enable-ldap \
    --with-default-pkcs11=%{_libdir}/opensc-pkcs11.so \
    --disable-static \
    --with-systemdsystemunitdir=%{_systemunitdir}

%make

%install
install -d %{buildroot}%{_sysconfdir}/ipsec.d/{cacerts,crls,private,certs,acerts,aacerts,ocspcerts}
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/run/pluto


make install DESTDIR=%{buildroot}

# (fg) File is copied over here
install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/ipsec

#mv %{buildroot}%{_sysconfdir}/ipsec.conf %{buildroot}%{_sysconfdir}/%{source_name}/

#rm -f %{buildroot}%{_libdir}/lib*.{so,a,la}

#%pre
#%_pre_useradd strongswan

%post
%_post_service ipsec


%preun
%_preun_service ipsec

#%postun
#%_postun_userdel strongswan

%files
%defattr(-,root,root,755)
%doc AUTHORS TODO NEWS README LICENSE
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
%{_systemunitdir}/strongswan.service
%{_libdir}/ipsec
%{_mandir}/man*/*
%{_sbindir}/ipsec


%changelog
* Wed May 25 2011 Funda Wang <fwang@mandriva.org> 4.5.2-1mdv2011.0
+ Revision: 678997
- fix build
- new version 4.5.2

* Thu Dec 23 2010 Funda Wang <fwang@mandriva.org> 4.3.6-3mdv2011.0
+ Revision: 624023
- update requires

* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 4.3.6-2mdv2011.0
+ Revision: 615010
- the mass rebuild of 2010.1 packages

* Fri Feb 12 2010 Frederik Himpe <fhimpe@mandriva.org> 4.3.6-1mdv2010.1
+ Revision: 505052
- update to new version 4.3.6

* Wed Feb 10 2010 Funda Wang <fwang@mandriva.org> 4.3.5-3mdv2010.1
+ Revision: 503626
- rebuild for new gmp

* Thu Feb 04 2010 Funda Wang <fwang@mandriva.org> 4.3.5-2mdv2010.1
+ Revision: 500815
- fix opensc2 requires

* Mon Nov 09 2009 Frederik Himpe <fhimpe@mandriva.org> 4.3.5-1mdv2010.1
+ Revision: 463623
- update to new version 4.3.5

* Wed Aug 19 2009 Frederik Himpe <fhimpe@mandriva.org> 4.3.4-1mdv2010.0
+ Revision: 417955
- update to new version 4.3.4

* Wed Jul 22 2009 Frederik Himpe <fhimpe@mandriva.org> 4.3.3-1mdv2010.0
+ Revision: 398490
- update to new version 4.3.3

* Mon Jun 22 2009 Frederik Himpe <fhimpe@mandriva.org> 4.3.2-1mdv2010.0
+ Revision: 388054
- update to new version 4.3.2

* Wed May 27 2009 Frederik Himpe <fhimpe@mandriva.org> 4.3.1-1mdv2010.0
+ Revision: 380247
- update to new version 4.3.1

* Tue Mar 31 2009 Oden Eriksson <oeriksson@mandriva.com> 4.2.14-1mdv2009.1
+ Revision: 362884
- 4.2.14 (fixes CVE-2009-0790)
- added P0 to fix build with -Werror=format-security

* Mon Feb 23 2009 Frederik Himpe <fhimpe@mandriva.org> 4.2.12-1mdv2009.1
+ Revision: 344304
- Update to new version 4.2.12

* Fri Jan 23 2009 Jérôme Soyer <saispo@mandriva.org> 4.2.11-1mdv2009.1
+ Revision: 332879
- New upstream release

* Mon Jan 12 2009 Jérôme Soyer <saispo@mandriva.org> 4.2.10-1mdv2009.1
+ Revision: 328668
- New upstream release
- New upstream release

* Wed Dec 03 2008 Jérôme Soyer <saispo@mandriva.org> 4.2.9-1mdv2009.1
+ Revision: 309644
- New release 4.2.9

* Fri Sep 19 2008 Frederik Himpe <fhimpe@mandriva.org> 4.2.7-1mdv2009.0
+ Revision: 286024
- Update to new version 4.2.7 (fixes denial of service vulnerablity)

* Thu Aug 28 2008 Frederik Himpe <fhimpe@mandriva.org> 4.2.6-1mdv2009.0
+ Revision: 276940
- update to new version 4.2.6

* Sat Aug 02 2008 Thierry Vignaud <tv@mandriva.org> 4.2.5-4mdv2009.0
+ Revision: 261210
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 4.2.5-3mdv2009.0
+ Revision: 253581
- rebuild

* Mon Jul 28 2008 Funda Wang <fwang@mandriva.org> 4.2.5-1mdv2009.0
+ Revision: 250813
- New version 4.2.5

  + Jérôme Soyer <saispo@mandriva.org>
    - Fix lib building
    - Add files
    - Clean Init
      Fix building
      Fix Running
    - Clean specs
    - Add some doc
    - Fix specs
    - Clean specs
    - Try to build a new release
    - Try to build a new release

  + Olivier Blin <oblin@mandriva.com>
    - initscript is not a config file
    - fix ipsec.conf path

* Fri Jan 04 2008 Thierry Vignaud <tv@mandriva.org> 2.8.3-2mdv2008.1
+ Revision: 145485
- adapt to new docdir layout
- fix prereq on rpm-helper
- kill re-definition of %%buildroot on Pixel's request


* Fri Mar 16 2007 Olivier Blin <oblin@mandriva.com> 2.8.3-2mdv2007.1
+ Revision: 145276
- fix build on x86_64
- 2.8.3 (and fix installation, #26453)

  + Jérôme Soyer <saispo@mandriva.org>
    - Import strongswan

* Sat Sep 10 2005 Andreas Hasenack <andreas@mandriva.com> 2.0.2-4mdk
- added gcc4 patch from ehabkost@mandriva.com and from openswan cvs
- rebuilt with openldap-2.3.x

* Mon Feb 07 2005 Buchan Milne <bgmilne@linux-mandrake.com> 2.0.2-3mdk
- rebuild for ldap2.2_7

* Thu Oct 14 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.2-2mdk
- rebuilt against new libcurl
- misc spec file fixes

* Thu Jun 10 2004 Florin <florin@mandrakesoft.com> 2.0.2-1mdk
- first Mandrake release

