#
# Conditional build:
%bcond_with	gtk2		# use GTK+ 2.x instead of 3.x
%bcond_without	champlain	# maps support via libchamplain [gtk+3 only]
%bcond_without	clutter		# GPU accelleration via clutter [gtk+3 only]
#
%if %{with gtk2}
%undefine	with_champlain
%undefine	with_clutter
%endif
Summary:	Graphics file browser utility
Summary(hu.UTF-8):	Képfájl-böngésző eszköz
Summary(pl.UTF-8):	Narzędzie do przeglądania plików graficznych
Name:		geeqie
Version:	1.4
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	http://www.geeqie.org/%{name}-%{version}.tar.xz
# Source0-md5:	52a4d387093e02182201b1cc02d99cc9
Patch0:		libdir-fix.patch
Patch1:		exiv2-0.27.patch
Patch2:		no-changelog.patch
URL:		http://www.geeqie.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
%{?with_clutter:BuildRequires:	clutter-devel >= 1.0}
%{?with_clutter:BuildRequires:	clutter-gtk-devel >= 1.0}
BuildRequires:	exiv2-devel >= 0.11
BuildRequires:	gdk-pixbuf2-devel >= 2
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	gnome-doc-utils
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 2:2.20.0}
%{!?with_gtk2:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	lcms2-devel >= 2.0
%{?with_champlain:BuildRequires:	libchamplain-devel >= 0.12}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	lirc-devel
BuildRequires:	lua51-devel >= 5.1.5-2
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	desktop-file-utils
Requires:	exiv2-libs >= 0.11
Requires:	glib2 >= 1:2.24.0
%{?with_gtk2:Requires:	gtk+2 >= 2:2.20.0}
%{!?with_gtk2:Requires:	gtk+3 >= 3.0.0}
%{?with_champlain:Requires:	libchamplain >= 0.12}
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d auxdir
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_clutter:--disable-gpu-accel} \
	--enable-gtk3%{?with_gtk2:=no} \
	%{?with_champlain:--enable-map}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	GNOME_DOC_TOOL=/disable-install-hook \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/{applications,template.desktop}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%find_lang %{name}

%post
%update_desktop_database

%postun
%update_desktop_database

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.md TODO doc/html
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/geeqie-import
%attr(755,root,root) %{_libdir}/%{name}/geeqie-rotate
%attr(755,root,root) %{_libdir}/%{name}/geeqie-symlink
%attr(755,root,root) %{_libdir}/%{name}/geeqie-ufraw
%{_libdir}/%{name}/geocode-parameters.awk
