# Warning:
# Anyone editing this spec file please make sure the same spec file
# works on other fedora and epel releases, which are supported by this software.
# No quick Rawhide-only fixes will be allowed.

%global etcfiles disablesid.conf dropsid.conf enablesid.conf modifysid.conf pulledpork.conf

# define pulledpork real name
%define pname pulledpork

Summary:	Pulled Pork for Snort and Suricata rule management
Name:		pulledpork7
Version:	0.7.3
Release:	7%{?dist}
# contrib/oink-conv.pl is GPLv2+
License:	GPLv2+
URL:		https://github.com/shirkdog/pulledpork
Source0:	https://github.com/shirkdog/pulledpork/archive/v%{version}.tar.gz#/%{pname}-%{version}.tar.gz
Source1:	%{pname}.conf
Patch0:		pulledpork-drop-enable.patch
Patch1:		pulledpork-do-not-drop-noalert.patch
BuildArch:	noarch

BuildRequires:	perl-generators
%if 0%{?fedora}
BuildRequires:	perl-interpreter
%else
BuildRequires:	perl
%endif

# Used by pulledpork to download rules, without it one gets errors like
# Error 501 when fetching https://snort.org/downloads/community/community-rules.tar.gz.md5
# https://github.com/shirkdog/pulledpork/issues/221
Requires:	perl(LWP::Protocol::https)

# handle license on el{6,7}: global must be defined after the License field above
%{!?_licensedir: %global license %doc}


%description
Pulled Pork for Snort and Suricata rule management (from Google code).


%prep
%autosetup -n %{pname}-%{version}


%build


%install
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_datadir}/%{pname}
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/%{pname}

%{__install} -m 0755 %{pname}.pl $RPM_BUILD_ROOT/%{_bindir}/%{pname}
%{__sed} -i 's|#!/usr/bin/env perl|#!/usr/bin/perl -w|' $RPM_BUILD_ROOT/%{_bindir}/%{pname}

%{__cp} -rp contrib $RPM_BUILD_ROOT/%{_datadir}/%{pname}
%{__chmod} 0755 $RPM_BUILD_ROOT/%{_datadir}/%{pname}/contrib/oink-conv.pl


cd etc
%{__rm} -f pulledpork.conf
%{__cp} %{SOURCE1} .
for file in disablesid.conf dropsid.conf enablesid.conf modifysid.conf pulledpork.conf; do
    %{__install} -m 0664 $file $RPM_BUILD_ROOT/%{_sysconfdir}/%{pname}
done


%files
%{_bindir}/%{pname}
%dir %{_datadir}/%{pname}
%dir %{_datadir}/%{pname}/contrib
%{_datadir}/%{pname}/contrib/oink-conv.pl
%{_datadir}/%{pname}/contrib/README.CONTRIB
%dir %{_sysconfdir}/%{pname}
%config(noreplace) %{_sysconfdir}/%{pname}/disablesid.conf
%config(noreplace) %{_sysconfdir}/%{pname}/dropsid.conf
%config(noreplace) %{_sysconfdir}/%{pname}/enablesid.conf
%config(noreplace) %{_sysconfdir}/%{pname}/modifysid.conf
%config(noreplace) %{_sysconfdir}/%{pname}/pulledpork.conf
%doc README.md doc/README.CATEGORIES doc/README.CHANGES doc/README.RULESET doc/README.SHAREDOBJECTS
%license LICENSE


%changelog
* Tue Sep 29 2020 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 0.7.3-7
- Rename to pulledpork7 - NethServer/dev#6287

* Wed Nov 20 2019 Filippo Carletti <filippo.carletti@gmail.com> - 0.7.3-6
- Don't drop rules with the noalert flowbit

* Fri Jun 28 2019 Filippo Carletti <filippo.carletti@gmail.com> - 0.7.3-5
- Don't drop disabled by default rules

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 09 2017 Marcin Dulak <Marcin.Dulak@gmail.com> - 0.7.3-1
- version 0.7.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Marcin Dulak <Marcin.Dulak@gmail.com> - 0.7.2-2
- pulledpork.conf: IPRVersion needs to be path ending with slash
- pulledpork.conf: version must match the pulledpork version

* Tue Nov 08 2016 Marcin Dulak <Marcin.Dulak@gmail.com> - 0.7.2-1
- version 0.7.2, based on https://github.com/jasonish/nsm-rpms

