Summary:	Graphics file browser utility
Summary(hu.UTF-8):	Képfájl-böngésző eszköz
Summary(pl.UTF-8):	Narzędzie do przeglądania plików graficznych
Name:		geeqie
Version:	1.0
Release:	2
License:	GPL v2
Group:		X11/Applications/Graphics
Source0:	http://downloads.sourceforge.net/geeqie/%{name}-%{version}.tar.gz
# Source0-md5:	1d67ef990390224c5052697d93bb49c0
URL:		http://geeqie.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	exiv2-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	libjpeg-progs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32		-fomit-frame-pointer

%description
Geeqie is a browser for graphics files. Offering single click viewing
of your graphics files. Includes thumbnail view, zoom and filtering
features. And external editor support.

%description -l fr.UTF-8
Geeqie est un explorateur de fichiers graphiques. Il permet d'un
simple clic l'affichage de vos fichiers graphiques. Les capacités
suivantes sont incluses: vue d'imagettes, zoom, filtres et support
d'éditeurs externes.

%description -l hu.UTF-8
Geeqie egy böngésző, amellyel a grafikus fájlokat tudod kezelni.
Egyszeri kattintásra megnézheted a képfájljaidat. Kicsinyített nézet,
zoom és szűrő eszközök is található, és külső szerkesztő támogatása.

%description -l pl.UTF-8
Geeqie jest przeglądarką plików graficznych. Możesz przeglądać swoje
pliki graficzne jednym kliknięciem myszy. Zawiera widok miniatur, zoom
i opcje filtrowania, jak również wsparcie dla zewnętrznego edytora.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install AUTHORS README TODO ChangeLog $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# gzip -9nf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}%{_state}/{AUTHORS,TODO,ChangeLog}
rm -f $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/COPYING

mv $RPM_BUILD_ROOT%{_datadir}/locale/zh_CN{.GB2312,}

mv $RPM_BUILD_ROOT%{_datadir}/%{name}/applications/*.desktop $RPM_BUILD_ROOT%{_desktopdir}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/{applications,template.desktop}

%find_lang %{name}

%post
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:

%postun
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
#doc AUTHORS README TODO ChangeLog
%docdir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/%{name}.png
%{_mandir}/man1/*
