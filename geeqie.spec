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
Version:	1.7.3
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	https://github.com/BestImageViewer/geeqie/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	1a54d7fe8c993c40c2e4c07a03c39d03
Patch0:		libdir-fix.patch
URL:		http://www.geeqie.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.14.1
%{?with_clutter:BuildRequires:	clutter-devel >= 1.0}
%{?with_clutter:BuildRequires:	clutter-gtk-devel >= 1.0}
BuildRequires:	djvulibre-devel >= 3.5.27
BuildRequires:	exiv2-devel >= 0.11
BuildRequires:	ffmpegthumbnailer-devel >= 2.1.0
BuildRequires:	gdk-pixbuf2-devel >= 2
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.52.0
BuildRequires:	graphviz
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 2:2.20.0}
%{!?with_gtk2:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.40.0
BuildRequires:	lcms2-devel >= 2.14
BuildRequires:	libarchive-devel >= 3.4.0
%{?with_champlain:BuildRequires:	libchamplain-devel >= 0.12}
BuildRequires:	libheif-devel >= 1.3.2
BuildRequires:	libjpeg-devel
BuildRequires:	libjxl-devel >= 0.3.7
BuildRequires:	libpng-devel
BuildRequires:	libraw-devel >= 0.20
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel >= 0.6.1
BuildRequires:	lirc-devel
BuildRequires:	lua53-devel >= 5.3
BuildRequires:	openjpeg2-devel >= 2.3.0
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.62
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	desktop-file-utils
Requires:	djvulibre >= 3.5.27
Requires:	exiv2-libs >= 0.11
Requires:	ffmpegthumbnailer >= 2.1.0
Requires:	glib2 >= 1:2.24.0
%{?with_gtk2:Requires:	gtk+2 >= 2:2.20.0}
%{!?with_gtk2:Requires:	gtk+3 >= 3.0.0}
Requires:	lcms2 >= 2.14
Requires:	libarchive >= 3.4.0
%{?with_champlain:Requires:	libchamplain >= 0.12}
Requires:	libheif >= 1.3.2
Requires:	libjpeg-progs
Requires:	libjxl >= 0.3.7
Requires:	libraw >= 0.20
Requires:	libwebp >= 0.6.1
Requires:	openjpeg2 >= 2.3.0
Requires:	poppler-glib >= 0.62
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

%build
%{__sed} -i '1s,/usr/bin/awk,/bin/awk,' \
	plugins/geocode-parameters/geocode-parameters.awk
install -d auxdir
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_clutter:--disable-gpu-accel} \
	%{?with_gtk2:--disable-gtk3} \
	--enable-lirc \
	%{?with_champlain:--enable-map} \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
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
%doc AUTHORS README.md TODO NEWS doc/html
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/geeqie-camera-import
%attr(755,root,root) %{_libdir}/%{name}/geeqie-camera-import-hook-script
%attr(755,root,root) %{_libdir}/%{name}/geeqie-export-jpeg
%attr(755,root,root) %{_libdir}/%{name}/geeqie-image-crop
%attr(755,root,root) %{_libdir}/%{name}/geeqie-random-image
%attr(755,root,root) %{_libdir}/%{name}/geeqie-rotate
%attr(755,root,root) %{_libdir}/%{name}/geeqie-symlink
%attr(755,root,root) %{_libdir}/%{name}/geeqie-tethered-photography
%attr(755,root,root) %{_libdir}/%{name}/geeqie-tethered-photography-hook-script
%attr(755,root,root) %{_libdir}/%{name}/geocode-parameters.awk
%attr(755,root,root) %{_libdir}/%{name}/lensID
%{_datadir}/metainfo/org.geeqie.Geeqie.appdata.xml
