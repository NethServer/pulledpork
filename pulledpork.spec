%global etcfiles disablesid.conf dropsid.conf enablesid.conf modifysid.conf pulledpork.conf

Summary:	Pulled Pork for Snort and Suricata rule management
Name:		pulledpork
Version:	0.7.2
Release:	2%{?dist}
# contrib/oink-conv.pl is GPLv2+
License:	GPLv2+
URL:		https://github.com/shirkdog/pulledpork
Source0:	https://github.com/shirkdog/pulledpork/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
BuildArch:	noarch

BuildRequires:	perl-generators
BuildRequires:	perl

# Used by pulledpork to download rules, without it one gets errors like
# Error 501 when fetching https://snort.org/downloads/community/community-rules.tar.gz.md5
# https://github.com/shirkdog/pulledpork/issues/221
Requires:	perl(LWP::Protocol::https)

# handle license on el{6,7}: global must be defined after the License field above
%{!?_licensedir: %global license %doc}


%description
Pulled Pork for Snort and Suricata rule management (from Google code).


%prep
%autosetup -n %{name}-%{version}


%build


%install
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_bindir}
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}
%{__install} -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}

%{__install} -m 0755 %{name}.pl $RPM_BUILD_ROOT/%{_bindir}/%{name}
%{__sed} -i 's|#!/usr/bin/env perl|#!/usr/bin/perl -w|' $RPM_BUILD_ROOT/%{_bindir}/%{name}

%{__cp} -rp contrib $RPM_BUILD_ROOT/%{_datadir}/%{name}
%{__chmod} 0755 $RPM_BUILD_ROOT/%{_datadir}/%{name}/contrib/oink-conv.pl


cd etc
%{__rm} -f pulledpork.conf
%{__cp} %{SOURCE1} .
for file in disablesid.conf dropsid.conf enablesid.conf modifysid.conf pulledpork.conf; do
    %{__install} -m 0664 $file $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}
done


%files
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/contrib
%{_datadir}/%{name}/contrib/oink-conv.pl
%{_datadir}/%{name}/contrib/README.CONTRIB
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/disablesid.conf
%config(noreplace) %{_sysconfdir}/%{name}/dropsid.conf
%config(noreplace) %{_sysconfdir}/%{name}/enablesid.conf
%config(noreplace) %{_sysconfdir}/%{name}/modifysid.conf
%config(noreplace) %{_sysconfdir}/%{name}/pulledpork.conf
%doc README.md doc/README.CATEGORIES doc/README.CHANGES doc/README.RULESET doc/README.SHAREDOBJECTS
%license LICENSE


%changelog
* Wed Nov 30 2016 Marcin Dulak <Marcin.Dulak@gmail.com> - 0.7.2-2
- pulledpork.conf: IPRVersion needs to be path ending with slash
- pulledpork.conf: version must match the pulledpork version

* Tue Nov 08 2016 Marcin Dulak <Marcin.Dulak@gmail.com> - 0.7.2-1
- version 0.7.2, based on https://github.com/jasonish/nsm-rpms

