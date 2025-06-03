#
# Conditional build:
%bcond_without	champlain	# maps support via libchamplain [gtk+3 only]
#
Summary:	Graphics file browser utility
Summary(hu.UTF-8):	Képfájl-böngésző eszköz
Summary(pl.UTF-8):	Narzędzie do przeglądania plików graficznych
Name:		geeqie
Version:	2.6.1
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
#Source0Download: https://github.com/BestImageViewer/geeqie/releases
Source0:	https://github.com/BestImageViewer/geeqie/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	7b1e29bef69acfcbc94e7aa6316cd8ed
Patch0:		geeqie-desktop.patch
URL:		http://www.geeqie.org/
BuildRequires:	Imath-devel >= 3.0.0
BuildRequires:	OpenEXR-devel >= 3.0.0
BuildRequires:	cfitsio-devel
%{?with_champlain:BuildRequires:	clutter-devel >= 1.0}
%{?with_champlain:BuildRequires:	clutter-gtk-devel >= 1.0}
BuildRequires:	djvulibre-devel >= 3.5.27
# to enable PDF preview feature
BuildRequires:	evince
BuildRequires:	exiv2-devel >= 0.18
BuildRequires:	ffmpegthumbnailer-devel >= 2.1.0
BuildRequires:	gdk-pixbuf2-devel >= 2
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.52.0
BuildRequires:	gspell-devel >= 1.6
BuildRequires:	gtk+3-devel >= 3.24
BuildRequires:	lcms2-devel >= 2.0
BuildRequires:	libarchive-devel >= 3.4.0
%{?with_champlain:BuildRequires:	libchamplain-devel >= 0.12}
BuildRequires:	libheif-devel >= 1.3.2
BuildRequires:	libjpeg-devel
BuildRequires:	libjxl-devel >= 0.3.7
BuildRequires:	libpng-devel
BuildRequires:	libraw-devel >= 0.20
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libwebp-devel >= 0.6.1
# 5.3 or 5.4
BuildRequires:	lua-devel >= 5.3
BuildRequires:	meson >= 1.0.0
BuildRequires:	ninja >= 1.5
BuildRequires:	openjpeg2-devel >= 2.3.0
BuildRequires:	pandoc
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.62
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	xxd
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires:	desktop-file-utils
Requires:	djvulibre >= 3.5.27
Requires:	exiv2-libs >= 0.18
Requires:	ffmpegthumbnailer >= 2.1.0
Requires:	glib2 >= 1:2.52.0
Requires:	gspell >= 1.6
Requires:	gtk+3 >= 3.24
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
Suggests:	bash-completion-geeqie
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

%package -n bash-completion-geeqie
Summary:	Bash completion for geeqie
Summary(pl.UTF-8):	Dopełnianie parametrów geeqie dla powłoki Bash
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-geeqie
Bash completion for geeqie.

%description -n bash-completion-geeqie -l pl.UTF-8
Dopełnianie parametrów geeqie dla powłoki Bash.

%prep
%setup -q
%patch -P0 -p1

%build
%{__sed} -i '1s,%{_bindir}/awk,/bin/awk,' \
	plugins/geocode-parameters/geocode-parameters.awk

%meson \
	-Darchive=enabled \
	-Dcms=enabled \
	-Ddoxygen=enabled \
	-Ddjvu=enabled \
	-Devince=enabled \
	-Dexecinfo=enabled \
	-Dexiv2=enabled \
	-Dexr=enabled \
	-Dextended_stacktrace=disabled \
	-Dfits=enabled \
	-Dgit=disabled \
	-Dgps-map=%{__enabled_disabled champlain} \
	-Dgq_bindir=%{_libdir}/%{name} \
	-Dheif=enabled \
	-Dhelp_pdf=enabled \
	-Dj2k=enabled \
	-Djpeg=enabled \
	-Djpegxl=enabled \
	-Dlibraw=enabled \
	-Dlua=enabled \
	-Dnpy=enabled \
	-Dpandoc=enabled \
	-Dpdf=enabled \
	-Dspell=enabled \
	-Dtiff=enabled \
	-Dvideothumbnailer=enabled \
	-Dwebp=enabled \
	-Dyelp-build=enabled

%meson_build

cd build/doc/html
ln -sf GuideIndex.html index.html

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/%{name}/{applications,org.geeqie.template.desktop}
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
%doc NEWS README.md build/doc/html
%attr(755,root,root) %{_bindir}/geeqie
%{_mandir}/man1/geeqie.1*
%{_desktopdir}/org.geeqie.Geeqie.desktop
# So far this file does nothing
#%{_desktopdir}/org.geeqie.cache-maintenance.desktop
%{_iconsdir}/hicolor/scalable/apps/geeqie.svg
%{_pixmapsdir}/geeqie.png
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/downsize
%attr(755,root,root) %{_libdir}/%{name}/geeqie-camera-import
%attr(755,root,root) %{_libdir}/%{name}/geeqie-camera-import-hook-script
%attr(755,root,root) %{_libdir}/%{name}/geeqie-export-jpeg
%attr(755,root,root) %{_libdir}/%{name}/geeqie-image-crop
%attr(755,root,root) %{_libdir}/%{name}/geeqie-random-image
%attr(755,root,root) %{_libdir}/%{name}/geeqie-resize-image
%attr(755,root,root) %{_libdir}/%{name}/geeqie-rotate
%attr(755,root,root) %{_libdir}/%{name}/geeqie-symlink
%attr(755,root,root) %{_libdir}/%{name}/geeqie-tethered-photography
%attr(755,root,root) %{_libdir}/%{name}/geeqie-tethered-photography-hook-script
%attr(755,root,root) %{_libdir}/%{name}/geocode-parameters.awk
%attr(755,root,root) %{_libdir}/%{name}/lensID
%attr(755,root,root) %{_libdir}/%{name}/resize-help.sh
%attr(755,root,root) %{_libdir}/%{name}/geeqie-exif-datetime-to-file
%{_datadir}/metainfo/org.geeqie.Geeqie.appdata.xml

%files -n bash-completion-geeqie
%defattr(644,root,root,755)
%{bash_compdir}/geeqie
