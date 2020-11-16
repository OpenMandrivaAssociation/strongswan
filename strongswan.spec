#%%define Werror_cflags %%nil

%define	major	0
%define	libswan	%mklibname	%{name} %{major}

%bcond_without	nm

Summary:	IPSEC implementation
Name:		strongswan
Version:	5.9.1
Release:	1
License:	GPLv2+
Group:		System/Servers
Url:		https://www.strongswan.org/
Source0:	http://download.strongswan.org/%{name}-%{version}.tar.bz2
Source1:	tmpfiles-%{name}.conf
Patch0:		strongswan-5.6.0-uintptr_t.patch
# To fix openssl plugin failure at loading (rbz #10579)
Patch1:		strongswan-5.8.4-openssl-disable-fips.patch
Source100:	%{name}.rpmlintrc
BuildRequires:	bison
BuildRequires:	byacc
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	gmp-devel >= 4.1.4
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	trousers-devel
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(sqlite3) >= 3.3.1
BuildRequires:	pkgconfig(systemd)
%if %{with nm}
BuildRequires:	pkgconfig(libnm)
%endif
Requires(post,preun,postun):	systemd
Requires:	%{libswan} = %{EVRD}

%description
FreeS/WAN is a free implementation of IPSEC & IKE for Linux. IPSEC is the
Internet Protocol Security and uses strong cryptography to provide both
authentication and encryption services. These services allow you to build
secure tunnels through untrusted networks. Everything passing through the
untrusted net is encrypted by the ipsec gateway machine and decrypted by the
gateway at the other end of the tunnel. The resulting tunnel is a virtual
private network or VPN.
This package contains the daemons and userland tools for setting up FreeS/WAN
on a freeswan enabled kernel.

%files
%doc COPYING NEWS README TODO
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/nm-%{name}-service.conf
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/ipsec.conf
%config(noreplace) %{_sysconfdir}/%{name}/ipsec.secrets
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%dir %{_sysconfdir}/%{name}/ipsec.d/
%dir %{_sysconfdir}/%{name}/ipsec.d/aacerts
%dir %{_sysconfdir}/%{name}/ipsec.d/acerts
%dir %{_sysconfdir}/%{name}/ipsec.d/certs
%dir %{_sysconfdir}/%{name}/ipsec.d/cacerts
%dir %{_sysconfdir}/%{name}/ipsec.d/crls
%dir %{_sysconfdir}/%{name}/ipsec.d/ocspcerts
%dir %{_sysconfdir}/%{name}/ipsec.d/private
%dir %{_sysconfdir}/%{name}/ipsec.d/reqs
%dir %{_sysconfdir}/%{name}/%{name}.d
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/aikgen.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/attest.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/charon.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/charon-logging.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/charon-systemd.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/imcv.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/pki.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/scepclient.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/sec-updater.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/starter.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/swanctl.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/tnc.conf
%dir %{_sysconfdir}/%{name}/%{name}.d/charon
#{_sysconfdir}/%%{name}/%%{name}.d/charon/*.conf
# We need to prevent overwriting of user's custom config
# but there are near 90 files here...
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.d/charon/*.conf
%dir %{_sysconfdir}/%{name}/swanctl
%config(noreplace) %{_sysconfdir}/%{name}/swanctl/swanctl.conf
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-starter.service
%{_sbindir}/charon-cmd
%{_sbindir}/charon-systemd
%{_sbindir}/sec-updater
%{_sbindir}/sw-collector
%{_sbindir}/%{name}
%{_sbindir}/swanctl
%{_bindir}/aikgen
%{_bindir}/pki
%{_bindir}/pt-tls-client
%{_bindir}/tpm_extendpcr
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/_copyright
%{_libexecdir}/%{name}/_imv_policy
%{_libexecdir}/%{name}/_updown
%{_libexecdir}/%{name}/charon
%{_libexecdir}/%{name}/duplicheck
%{_libexecdir}/%{name}/imv_policy_manager
#{_libexecdir}/%%{name}/pt-tls-client
%{_libexecdir}/%{name}/scepclient
%{_libexecdir}/%{name}/starter
%{_libexecdir}/%{name}/stroke
%{_libexecdir}/%{name}/xfrmi
%{_datadir}/%{name}/swidtag/*.swidtag
%{_datadir}/%{name}/templates/config/plugins/*.conf
%{_datadir}/%{name}/templates/config/%{name}.conf
%{_datadir}/%{name}/templates/config/%{name}.d/*.conf
%{_datadir}/%{name}/templates/database/imv/*.sql
%{_datadir}/%{name}/templates/database/sw-collector/*.sql
%{_mandir}/man1/%{name}*.1.*
%{_mandir}/man5/%{name}.conf.5.*
%{_mandir}/man5/%{name}_ipsec.conf.5.*
%{_mandir}/man5/%{name}_ipsec.secrets.5.*
%{_mandir}/man5/%{name}_swanctl.conf.5.*
%{_mandir}/man8/%{name}.8.*
%{_mandir}/man8/%{name}_charon-cmd.8.*
%{_mandir}/man8/%{name}_scepclient.8.*
%{_mandir}/man8/%{name}_sec-updater.8.*
%{_mandir}/man8/%{name}_sw-collector.8.*
%{_mandir}/man8/%{name}_swanctl.8.*

%post
# FIXME: New releases changed the way of starting the daemon;
# the old way (using ipsec) is now in %%{name}-starter.service:
# use it until we are sure that swanctl config is OK.
#systemd_post %%{name}.service
%systemd_post %{name}-starter.service

%preun
#systemd_preun %%{name}.service
%systemd_preun %{name}-starter.service

%postun
#systemd_postun_with_restart %%{name}.service
%systemd_postun_with_restart %{name}-starter.service

#----------------------------------------------------------------------------

%package -n %{libswan}
Summary:	Libraries and plugins for Strongswan
Group:		System/Libraries

%description -n %{libswan}
FreeS/WAN is a free implementation of IPSEC & IKE for Linux. IPSEC is the
Internet Protocol Security and uses strong cryptography to provide both
authentication and encryption services.
This package contains the libraries needed from %{name}, including the
IMC/IMV dynamic libraries that can be used by any third party TNC
Client/Server implementation possessing a standard IF-IMC/IMV interface.

%files -n %{libswan}
%doc COPYING
%{_libdir}/%{name}/libcharon.so.%{major}*
%{_libdir}/%{name}/libimcv.so.%{major}*
%{_libdir}/%{name}/libipsec.so.%{major}*
%{_libdir}/%{name}/libpttls.so.%{major}*
%{_libdir}/%{name}/libradius.so.%{major}*
%{_libdir}/%{name}/lib%{name}.so.%{major}*
%{_libdir}/%{name}/libsimaka.so.%{major}*
%{_libdir}/%{name}/libtls.so.%{major}*
%{_libdir}/%{name}/libtpmtss.so.%{major}*
%{_libdir}/%{name}/libtnccs.so.%{major}*
%{_libdir}/%{name}/libvici.so.%{major}*
%dir %{_libdir}/%{name}/imcvs
%{_libdir}/%{name}/imcvs/imc-attestation.so
%{_libdir}/%{name}/imcvs/imc-hcd.so
%{_libdir}/%{name}/imcvs/imc-os.so
%{_libdir}/%{name}/imcvs/imc-scanner.so
%{_libdir}/%{name}/imcvs/imc-swima.so
%{_libdir}/%{name}/imcvs/imc-test.so
%{_libdir}/%{name}/imcvs/imv-attestation.so
%{_libdir}/%{name}/imcvs/imv-hcd.so
%{_libdir}/%{name}/imcvs/imv-os.so
%{_libdir}/%{name}/imcvs/imv-scanner.so
%{_libdir}/%{name}/imcvs/imv-swima.so
%{_libdir}/%{name}/imcvs/imv-test.so
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/lib%{name}-acert.so
%{_libdir}/%{name}/plugins/lib%{name}-aes.so
%{_libdir}/%{name}/plugins/lib%{name}-attr.so
%{_libdir}/%{name}/plugins/lib%{name}-chapoly.so
%{_libdir}/%{name}/plugins/lib%{name}-cmac.so
%{_libdir}/%{name}/plugins/lib%{name}-constraints.so
%{_libdir}/%{name}/plugins/lib%{name}-counters.so
%{_libdir}/%{name}/plugins/lib%{name}-curl.so
%{_libdir}/%{name}/plugins/lib%{name}-curve25519.so
%{_libdir}/%{name}/plugins/lib%{name}-des.so
%{_libdir}/%{name}/plugins/lib%{name}-dhcp.so
%{_libdir}/%{name}/plugins/lib%{name}-dnskey.so
%{_libdir}/%{name}/plugins/lib%{name}-drbg.so
%{_libdir}/%{name}/plugins/lib%{name}-duplicheck.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-aka.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-aka-3gpp.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-aka-3gpp2.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-dynamic.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-md5.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-gtc.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-identity.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-mschapv2.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-peap.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-radius.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-sim.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-sim-file.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-tls.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-tnc.so
%{_libdir}/%{name}/plugins/lib%{name}-eap-ttls.so
%{_libdir}/%{name}/plugins/lib%{name}-ext-auth.so
%{_libdir}/%{name}/plugins/lib%{name}-farp.so
%{_libdir}/%{name}/plugins/lib%{name}-fips-prf.so
%{_libdir}/%{name}/plugins/lib%{name}-gmp.so
%{_libdir}/%{name}/plugins/lib%{name}-ha.so
%{_libdir}/%{name}/plugins/lib%{name}-hmac.so
%{_libdir}/%{name}/plugins/lib%{name}-ipseckey.so
%{_libdir}/%{name}/plugins/lib%{name}-kernel-libipsec.so
%{_libdir}/%{name}/plugins/lib%{name}-kernel-netlink.so
%{_libdir}/%{name}/plugins/lib%{name}-ldap.so
%{_libdir}/%{name}/plugins/lib%{name}-led.so
%{_libdir}/%{name}/plugins/lib%{name}-md4.so
%{_libdir}/%{name}/plugins/lib%{name}-md5.so
%{_libdir}/%{name}/plugins/lib%{name}-mgf1.so
%{_libdir}/%{name}/plugins/lib%{name}-nonce.so
%{_libdir}/%{name}/plugins/lib%{name}-openssl.so
%{_libdir}/%{name}/plugins/lib%{name}-pem.so
%{_libdir}/%{name}/plugins/lib%{name}-pkcs1.so
%{_libdir}/%{name}/plugins/lib%{name}-pkcs7.so
%{_libdir}/%{name}/plugins/lib%{name}-pkcs8.so
%{_libdir}/%{name}/plugins/lib%{name}-pkcs11.so
%{_libdir}/%{name}/plugins/lib%{name}-pkcs12.so
%{_libdir}/%{name}/plugins/lib%{name}-pgp.so
%{_libdir}/%{name}/plugins/lib%{name}-pubkey.so
%{_libdir}/%{name}/plugins/lib%{name}-rc2.so
%{_libdir}/%{name}/plugins/lib%{name}-sshkey.so
%{_libdir}/%{name}/plugins/lib%{name}-random.so
%{_libdir}/%{name}/plugins/lib%{name}-resolve.so
%{_libdir}/%{name}/plugins/lib%{name}-revocation.so
%{_libdir}/%{name}/plugins/lib%{name}-sha1.so
%{_libdir}/%{name}/plugins/lib%{name}-sha2.so
%{_libdir}/%{name}/plugins/lib%{name}-sha3.so
%{_libdir}/%{name}/plugins/lib%{name}-socket-default.so
%{_libdir}/%{name}/plugins/lib%{name}-soup.so
%{_libdir}/%{name}/plugins/lib%{name}-sqlite.so
%{_libdir}/%{name}/plugins/lib%{name}-stroke.so
%{_libdir}/%{name}/plugins/lib%{name}-systime-fix.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-ifmap.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-imc.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-imv.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-pdp.so
%{_libdir}/%{name}/plugins/lib%{name}-tnc-tnccs.so
%{_libdir}/%{name}/plugins/lib%{name}-tnccs-20.so
%{_libdir}/%{name}/plugins/lib%{name}-tnccs-11.so
%{_libdir}/%{name}/plugins/lib%{name}-tnccs-dynamic.so
%{_libdir}/%{name}/plugins/lib%{name}-tpm.so
%{_libdir}/%{name}/plugins/lib%{name}-unity.so
%{_libdir}/%{name}/plugins/lib%{name}-updown.so
%{_libdir}/%{name}/plugins/lib%{name}-vici.so
%{_libdir}/%{name}/plugins/lib%{name}-x509.so
%{_libdir}/%{name}/plugins/lib%{name}-xauth-eap.so
%{_libdir}/%{name}/plugins/lib%{name}-xauth-generic.so
%{_libdir}/%{name}/plugins/lib%{name}-xauth-noauth.so
%{_libdir}/%{name}/plugins/lib%{name}-xauth-pam.so
%{_libdir}/%{name}/plugins/lib%{name}-xcbc.so

#----------------------------------------------------------------------------

%if %{with nm}
%package	charon-nm
Summary:	NetworkManager plugin for Strongswan
Group:		System/Servers

%description charon-nm
NetworkManager plugin integrates a subset of Strongswan capabilities
to NetworkManager.

%files charon-nm
%doc COPYING
%{_libexecdir}/%{name}/charon-nm
%endif

#----------------------------------------------------------------------------

%package tnc-imcvs
Summary:	Trusted network connect (TNC)'s IMC/IMV functionality
Group:		System/Servers
Requires:	%{name} = %{EVRD}
Requires:	%{libswan} = %{EVRD}

%description tnc-imcvs
This package provides Trusted Network Connect's (TNC) IMC and IMV
functionality. Specifically it includes PTS based IMC/IMV for TPM based
remote attestation and scanner and test IMCs and IMVs.

%files tnc-imcvs
%doc COPYING
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/attest

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
libtoolize --install --copy --force --automake
aclocal -I m4
autoconf
autoheader
automake --add-missing --copy

%serverbuild
# TODO: Command-line too long: consider using --enable-all
#  by default and selectively disabling unwanted options, if any
%configure2_5x \
	--disable-static \
	--with-ipsec-script=%{name} \
	--sysconfdir=%{_sysconfdir}/%{name} \
	--with-ipsecdir=%{_libexecdir}/%{name} \
	--with-ipseclibdir=%{_libdir}/%{name} \
	--with-piddir="/run/%{name}" \
	--with-fips-mode=2 \
	--enable-acert \
	--enable-aikgen \
	--enable-chapoly \
	--enable-cmd \
	--enable-curl \
	--enable-dhcp \
	--enable-duplicheck \
	--enable-eap-aka \
	--enable-eap-aka-3gpp \
	--enable-eap-aka-3gpp2 \
	--enable-eap-dynamic \
	--enable-eap-gtc \
	--enable-eap-identity \
	--enable-eap-md5 \
	--enable-eap-mschapv2 \
	--enable-eap-peap \
	--enable-eap-radius \
	--enable-eap-sim \
	--enable-eap-sim-file \
	--enable-eap-tls \
	--enable-eap-ttls \
	--enable-eap-tnc \
	--enable-ext-auth \
	--enable-farp \
	--enable-ha \
	--enable-imc-attestation \
	--enable-imc-hcd \
	--enable-imc-os \
	--enable-imc-scanner \
	--enable-imc-swima \
	--enable-imc-test \
	--enable-imv-attestation \
	--enable-imv-hcd \
	--enable-imv-os \
	--enable-imv-scanner  \
	--enable-imv-swima \
	--enable-imv-test \
	--enable-ipseckey \
	--enable-kernel-libipsec \
	--enable-ldap \
	--enable-led \
	--enable-md4 \
%if %{with nm}
	--enable-nm \
%endif
	--enable-openssl \
	--enable-pkcs11 \
	--enable-sha3 \
	--enable-soup \
	--enable-sqlite \
	--enable-swanctl \
	--enable-systemd \
	--enable-systime-fix \
	--enable-tnc-ifmap \
	--enable-tnc-imc \
	--enable-tnc-imv \
	--enable-tnc-pdp \
	--enable-tnccs-11 \
	--enable-tnccs-20 \
	--enable-tnccs-dynamic \
	--enable-tpm \
	--enable-tss-trousers \
	--disable-tss-tss2 \
	--enable-unity \
	--enable-vici \
	--enable-xauth-eap \
	--enable-xauth-noauth \
	--enable-xauth-pam

%make


%install
%makeinstall_std

# Prefix man pages
for i in %{buildroot}%{_mandir}/*/*; do
	if echo "$i" | grep -vq '/%{name}[^\/]*$'; then
		mv "$i" "`echo "$i" | sed -re 's|/([^/]+)$|/%{name}_\1|'`"
	fi
done

# Delete unwanted library files: no -devel package
rm %{buildroot}%{_libdir}/%{name}/*.so
find %{buildroot} -type f -name '*.la' -delete

# Fix config permissions
chmod 644 %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf

# Protect configuration from ordinary user's eyes
chmod 700 %{buildroot}%{_sysconfdir}/%{name}

# Create ipsec.d directory tree.
install -d -m 700 %{buildroot}%{_sysconfdir}/%{name}/ipsec.d
for i in aacerts acerts certs cacerts crls ocspcerts private reqs; do
	install -d -m 700 %{buildroot}%{_sysconfdir}/%{name}/ipsec.d/${i}
done

# Install tmpfiles support
install -D -m 0644 %{SOURCE1} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

# Put a config file in the right spot
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d/
cp %{buildroot}%{_datadir}/dbus-1/system.d/nm-%{name}-service.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
rm -rf %{buildroot}%{_datadir}/dbus-1
