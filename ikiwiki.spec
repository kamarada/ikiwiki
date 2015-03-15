#
# spec file for package ikiwiki
#
# Copyright (c) 2015 Kamarada Project, Aracaju, Brazil.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://github.com/kamarada
#


%define version 3.20141016.1
%define tarname ikiwiki_%{version}
Name:           ikiwiki
Version:        %{version}
Release:        1
Summary:        A wiki compiler
License:        GPL-2.0+
Group:          Productivity/Networking/Web/Utilities
# git://git.ikiwiki.info/
# https://packages.debian.org/unstable/source/ikiwiki
Source0:        %{tarname}.tar.gz
Source1:        LICENSE
Patch1:         p01_use_suse_openid.patch
Patch2:         p02_dont_call_links_from_backlink.patch
Url:            http://ikiwiki.info/
Vendor:         Joey Hess <joey@ikiwiki.info>
Packager:       Kamarada Linux <kamaradalinux@gmail.com>
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildArch:      noarch
BuildRequires:  fdupes

# http://download.opensuse.org/repositories/devel:/languages:/perl/openSUSE_13.2
# http://download.opensuse.org/repositories/devel:/languages:/perl:/CPAN-N/openSUSE_13.2/
# http://download.opensuse.org/repositories/devel:/languages:/perl:/CPAN-T/openSUSE_13.2/
# http://download.opensuse.org/repositories/server:/search/openSUSE_13.2/

# https://ikiwiki.info/install/

# core modules that ikiwiki needs
# https://github.com/joeyh/ikiwiki/blob/master/Bundle/IkiWiki.pm
BuildRequires:  perl(Text::Markdown)
BuildRequires:  perl(HTML::Scrubber)
BuildRequires:  perl(HTML::Template)
BuildRequires:  perl(HTML::Parser)
BuildRequires:  perl(URI)
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(Date::Parse)
BuildRequires:  perl(CGI::FormBuilder)
BuildRequires:  perl(CGI::Session)
BuildRequires:  perl(Mail::Sendmail)
BuildRequires:  perl(CGI)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(YAML::XS)
BuildRequires:  perl(JSON)
BuildRequires:  perl(RPC::XML)

Requires:       perl(Text::Markdown)
Requires:       perl(HTML::Scrubber)
Requires:       perl(HTML::Template)
Requires:       perl(HTML::Parser)
Requires:       perl(URI)
Requires:       perl(XML::Simple)
Requires:       perl(Date::Parse)
Requires:       perl(CGI::FormBuilder)
Requires:       perl(CGI::Session)
Requires:       perl(Mail::Sendmail)
Requires:       perl(CGI)
Requires:       perl(Data::Dumper)
Requires:       perl(YAML::XS)
Requires:       perl(JSON)
Requires:       perl(RPC::XML)

# modules used by ikiwiki plugins
# https://github.com/joeyh/ikiwiki/blob/master/Bundle/IkiWiki/Extras.pm

BuildRequires:  perl(Authen::Passphrase)
BuildRequires:  perl(Search::Xapian)
BuildRequires:  perl(File::MimeInfo)
BuildRequires:  perl(Locale::gettext)
BuildRequires:  perl(Net::OpenID::Consumer)
BuildRequires:  perl(LWPx::ParanoidAgent)
BuildRequires:  perl(Crypt::SSLeay)
BuildRequires:  perl(Text::CSV)
# BuildRequires:  perl(Text::Typography)
BuildRequires:  perl(Text::Textile)
BuildRequires:  perl(Text::WikiFormat)
BuildRequires:  perl(XML::Feed)
# BuildRequires:  perl(Net::Amazon::S3)
# BuildRequires:  perl(Text::WikiCreole)
BuildRequires:  perl(Term::ReadLine::Gnu)
BuildRequires:  perl(HTML::Tree)
BuildRequires:  perl(Sort::Naturally)
BuildRequires:  perl(Gravatar::URL)
BuildRequires:  perl(Net::INET6Glue)
BuildRequires:  perl(XML::Writer)

Requires:       perl(Authen::Passphrase)
Requires:       perl(Search::Xapian)
Requires:       perl(File::MimeInfo)
Requires:       perl(Locale::gettext)
Requires:       perl(Net::OpenID::Consumer)
Requires:       perl(LWPx::ParanoidAgent)
Requires:       perl(Crypt::SSLeay)
Requires:       perl(Text::CSV)
# Requires:       perl(Text::Typography)
Requires:       perl(Text::Textile)
Requires:       perl(Text::WikiFormat)
Requires:       perl(XML::Feed)
# Requires:       perl(Net::Amazon::S3)
# Requires:       perl(Text::WikiCreole)
Requires:       perl(Term::ReadLine::Gnu)
Requires:       perl(HTML::Tree)
Requires:       perl(Sort::Naturally)
Requires:       perl(Gravatar::URL)
Requires:       perl(Net::INET6Glue)
Requires:       perl(XML::Writer)

# other (?)
BuildRequires:  bzr
# BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  mercurial
# BuildRequires:  perl(Date::Format)
# BuildRequires:  perl(File::chdir)
# BuildRequires:  perl(File::ReadBackwards)
BuildRequires:  perl(Image::Magick)
BuildRequires:  perl(IPC::Run)
BuildRequires:  perl(XML::Twig)
BuildRequires:  po4a
BuildRequires:  python-docutils
BuildRequires:  subversion


%description
Ikiwiki is a wiki compiler. It converts wiki pages into HTML pages suitable for publishing on a website. Ikiwiki stores pages and history in a revision control system such as Subversion or Git. There are many other features, including support for blogging and podcasting, as well as a large array of plugins.

Alternatively, think of ikiwiki as a particularly flexible static site generator with some dynamic features.


%prep
%setup -q -n %{name}
# %patch01 -p1
%patch02 -p1
cp -a %{SOURCE0} COPYING
# remove cvs plugin, File/chdir.pm not available
rm IkiWiki/Plugin/cvs.pm
# remove other problematic files
rm t/cvs.t
rm t/git.t
rm t/html.t
rm t/img.t
rm t/podcast.t
rm t/syslog.t


%build
perl Makefile.PL INSTALLDIRS=vendor PREFIX=%{_prefix}
make


%check
make test


%install
make pure_install DESTDIR="%{buildroot}"

# remove shebang (thanks Fedora)
%{__sed} -e '1{/^#!/d}' -i \
        %{buildroot}%{_sysconfdir}/ikiwiki/auto.setup \
        %{buildroot}%{_sysconfdir}/ikiwiki/auto-blog.setup \
        %{buildroot}%{_prefix}/lib/ikiwiki/plugins/proxy.py

%find_lang %name

%fdupes %{buildroot}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%doc debian/NEWS README debian/changelog
%doc doc/examples html
%doc IkiWiki/Plugin/skeleton.pm.example
%{perl_vendorlib}/IkiWiki*
%{_datadir}/ikiwiki
%exclude %{_datadir}/ikiwiki/examples
%{_bindir}/ikiwiki
%{_bindir}/ikiwiki-transition
%{_bindir}/ikiwiki-makerepo
%{_bindir}/ikiwiki-calendar
%{_bindir}/ikiwiki-update-wikilist
%{_mandir}/*/ikiwiki*
%{_sbindir}/ikiwiki-mass-rebuild
%dir %{_prefix}/lib/w3m
%dir %{_prefix}/lib/w3m/cgi-bin
%{_prefix}/lib/w3m/cgi-bin/ikiwiki-w3m.cgi
%{_prefix}/lib/ikiwiki
%dir /etc/ikiwiki
%config(noreplace)/etc/ikiwiki/wikilist
%config(noreplace)/etc/ikiwiki/auto.setup
%config(noreplace)/etc/ikiwiki/auto-blog.setup
%exclude %{perl_vendorlib}/IkiWiki*/Plugin/skeleton.pm.example
%exclude %{perl_vendorarch}


%changelog
* Sun Mar 15 2015 Kamarada Linux <kamaradalinux@gmail.com>
- Initial import from Debian sid repository, version 3.20141016.1