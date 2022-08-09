#
# Conditional build:
%bcond_without	champlain	# maps support via libchamplain [gtk+3 only]
#
Summary:	Graphics file browser utility
Summary(hu.UTF-8):	Képfájl-böngésző eszköz
Summary(pl.UTF-8):	Narzędzie do przeglądania plików graficznych
Name:		geeqie
Version:	2.0
Release:	0.1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	https://github.com/BestImageViewer/geeqie/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	2d7a8e40a0216330f38262a31a5fa725
URL:		http://www.geeqie.org/
BuildRequires:	djvulibre-devel >= 3.5.27
BuildRequires:	exiv2-devel >= 0.11
BuildRequires:	ffmpegthumbnailer-devel >= 2.1.0
BuildRequires:	gdk-pixbuf2-devel >= 2
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.52.0
BuildRequires:	gspell-devel >= 1.6
BuildRequires:	gtk+3-devel >= 3.22}
BuildRequires:	lcms2-devel >= 2.0
BuildRequires:	libarchive-devel >= 3.4.0
%{?with_champlain:BuildRequires:	libchamplain-devel >= 0.12}
BuildRequires:	libheif-devel >= 1.3.2
BuildRequires:	libjpeg-devel
BuildRequires:	libjxl-devel >= 0.3.7
BuildRequires:	libpng-devel
BuildRequires:	libraw-devel >= 0.20
BuildRequires:	libtiff-devel
BuildRequires:	libwebp-devel >= 0.6.1
BuildRequires:	lua53-devel >= 5.3
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	openjpeg2-devel >= 2.3.0
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.62
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	xxd
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	desktop-file-utils
Requires:	djvulibre >= 3.5.27
Requires:	exiv2-libs >= 0.11
Requires:	ffmpegthumbnailer >= 2.1.0
Requires:	glib2 >= 1:2.24.0
Requires:	gtk+3 >= 3.22
Requires:	lcms2 >= 2.0
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
%{__rm} -rf build

%build
%{__sed} -i '1s,%{_bindir}/awk,/bin/awk,' \
	plugins/geocode-parameters/geocode-parameters.awk

%meson build -Dgq_bindir=%{_libdir}/%{name} %{!?with_champlain:-Dgps-map=disabled}

%ninja_build -C build

cd build/doc/html
ln -sf GuideIndex.html index.html

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/{applications,template.desktop}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}


%find_lang %{name}

%post
%update_desktop_database

%postun
%update_desktop_database

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.md TODO NEWS build/doc/html
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
