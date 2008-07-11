# TODO
# - system dumb package
#
# Conditional build:
%bcond_with	system_dumb	# build with system dumb (API incompatability)
#
Summary:	UFO2000 - a turn based tactical squad simulation multiplayer game
Summary(pl.UTF-8):	UFO2000 - turowa gra strategiczna z symulacją oddziałów dla wielu graczy
Name:		ufo2000
Version:	0.7.1086
Release:	0.2
License:	GPL
Group:		X11/Applications/Games/Strategy
Source0:	http://dl.sourceforge.net/ufo2000/%{name}-%{version}-src.tar.bz2
# Source0-md5:	b6e4bfa6b860b3da733b48e5fd347ec9
Source1:	http://dl.sourceforge.net/ufo2000/%{name}-music-2004.zip
# Source1-md5:	2db2878a55e5df97a198f2310603a5c7
Source2:	%{name}.png
Source3:	%{name}.desktop
Source4:	http://dl.sourceforge.net/dumb/dumb-0.9.2.tar.gz
# Source4-md5:	0ce45f64934e6d5d7b82a55108596680
URL:		http://ufo2000.sourceforge.net/
%{!?with_system_dumb:BuildRequires:	allegro-devel}
%{?with_system_dumb:BuildRequires:	dumb-devel}
BuildRequires:	expat-devel
BuildRequires:	freetype-devel >= 1:2.0
BuildRequires:	libhawknl-devel
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libvorbis-devel
BuildRequires:	sqlite-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
UFO2000 is free and opensource turn based tactical squad simulation
multiplayer game. It is heavily inspired by the famous X-COM: UFO
Defense game. While UFO2000 engine was specifically designed to be
compatible with the graphics resources and maps from X-COM, you don't
need any proprietary data files to play as a new fan-made set of
graphics exists and is included in UFO2000 distribution by default, so
the game is ready to run out of the box.

But if you want an exact X-COM look and feel, you have an option of
installing original X-COM and TFTD data files and use them for
extending UFO2000 with additional maps, weapon sets and units.

NOTE: You must be a member of group game to play the game!

%description -l pl.UTF-8
UFO2000 to wolnodostępna, mająca otwarte źródła turowa gra
strategiczna z symulacją oddziałów dla wielu graczy. Jest w dużym
stopniu zainspirowana znaną grą X-COM: UFO Defense. Choć silnik
UFO2000 został zaprojektowany z myślą o kompatybilności z zasobami
graficznymi i mapami z X-COM, do grania nie są wymagane żadne
własnościowe pliki danych, ponieważ istnieją zestawy grafik wykonane
przez fanów, domyślnie dołączone do pakietu UFO2000 - tak więc gra
jest gotowa do użytku zaraz po zainstalowaniu.

Aby otrzymać dokładny wygląd i zachowanie gry X-COM, trzeba
zainstalować oryginalne pliki danych X-COM i TFTD, a następnie użyć
ich do rozszerzenia UFO2000 o dodatkowe mapy, zestawy broni i
jednostki.

Uwaga: aby grać w tę grę trzeba być członkiem grupy graczy!

%prep
%setup -q -c -n %{name}_%{version} %{!?with_system_dumb:-a4}
find -name .svn | xargs rm -rf

# some sound files ..
cd newmusic
	mv readme.txt readme.txt.org
	unzip -q %{SOURCE1}
	mv readme.txt readme.txt-soundtrack
	mv readme.txt.org readme.txt
cd -

%if %{without system_dumb}
# dumb will be linked static
%{__sed} -i -e 's|-laldmb -ldumb|dumb/lib/unix/libaldmb.a dumb/lib/unix/libdumb.a|g' makefile
%endif

%build
%if %{without system_dumb}
# first build dumb, will be linked static
cd dumb
cat > make/config.txt << EOF
include make/unix.inc
ALL_TARGETS := core core-examples core-headers
ALL_TARGETS += allegro allegro-examples allegro-headers
PREFIX := %{_prefix}
EOF
%{__make} \
	CC="%{__cc}" \
	CX="%{__cxx}" \
	OPTFLAGS="%{rpmcflags} -I/usr/include/hawknl" \
	OFLAGS="%{rpmcflags} -fPIC"
cd -
%endif

%{__make} \
	CC="%{__cc}" \
	CX="%{__cxx}" \
	OPTFLAGS="%{rpmcflags} -I/usr/include/hawknl %{!?with_system_dumb:-Idumb/include}" \
	DATA_DIR="%{_datadir}/games/%{name}" \
	all server

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install %{name} $RPM_BUILD_ROOT%{_bindir}
install %{name}-srv $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_datadir}/games/%{name}
install %{name}.default.ini $RPM_BUILD_ROOT%{_datadir}/games/%{name}/%{name}.ini

for i in arts extensions fonts init-scripts newmaps newmusic newunits script translations; do
	cp -a $i $RPM_BUILD_ROOT%{_datadir}/games/%{name}
done
install -d $RPM_BUILD_ROOT%{_datadir}/games/%{name}/TFTD
install -d $RPM_BUILD_ROOT%{_datadir}/games/%{name}/XCOM
for i in keyboard.dat select_option.ini soundmap.xml squad.default.lua \
	ufo2000.dat %{name}.default.ini xcom_folder.ini; do
	cp -a $i $RPM_BUILD_ROOT%{_datadir}/games/%{name}
done
install ufo2000-srv.conf $RPM_BUILD_ROOT%{_datadir}/games/%{name}

# create menu and icon
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
install -d $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE3} $RPM_BUILD_ROOT%{_desktopdir}

# not needed for playing game
rm -f $RPM_BUILD_ROOT%{_datadir}/games/%{name}/translations/{*.txt,*.pot}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING *.txt *.html readme_select.ini
%doc docs/*
%attr(755,root,root) %{_bindir}/ufo2000
%attr(755,root,root) %{_bindir}/ufo2000-srv
%dir %{_datadir}/games/%{name}
%{_datadir}/games/%{name}/*.conf
%{_datadir}/games/%{name}/*.dat
%{_datadir}/games/%{name}/*.ini
%{_datadir}/games/%{name}/*.lua
%{_datadir}/games/%{name}/*.xml
%{_datadir}/games/%{name}/TFTD
%{_datadir}/games/%{name}/XCOM
%{_datadir}/games/%{name}/arts
%{_datadir}/games/%{name}/extensions
%{_datadir}/games/%{name}/fonts
%{_datadir}/games/%{name}/init-scripts
%{_datadir}/games/%{name}/newmaps
%{_datadir}/games/%{name}/newmusic
%{_datadir}/games/%{name}/newunits
%{_datadir}/games/%{name}/script
%dir %{_datadir}/games/%{name}/translations
%{_datadir}/games/%{name}/translations/ufo2000-apr.po
%lang(be) %{_datadir}/games/%{name}/translations/ufo2000-bel.po
%lang(de) %{_datadir}/games/%{name}/translations/ufo2000-deu.po
%lang(et) %{_datadir}/games/%{name}/translations/ufo2000-est.po
%lang(fr) %{_datadir}/games/%{name}/translations/ufo2000-fre.po
%lang(it) %{_datadir}/games/%{name}/translations/ufo2000-ita.po
%lang(ru) %{_datadir}/games/%{name}/translations/ufo2000-rus.po
%lang(es) %{_datadir}/games/%{name}/translations/ufo2000-spa.po
%{_pixmapsdir}/*.png
%{_desktopdir}/%{name}*.desktop
