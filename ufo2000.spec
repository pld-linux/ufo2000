# TODO
# - system dumb package
Summary:	UFO2000 is a turn based tactical squad simulation multiplayer game
Name:		ufo2000
Version:	0.7.1086
Release:	0.1
License:	GPL
Group:		X11/Applications/Games/Strategy
URL:		http://ufo2000.sourceforge.net/
Source0:	http://dl.sourceforge.net/ufo2000/%{name}-%{version}-src.tar.bz2
# Source0-md5:	b6e4bfa6b860b3da733b48e5fd347ec9
Source1:	%{name}.png
Source2:	http://dl.sourceforge.net/dumb/dumb-0.9.2.tar.gz
# Source2-md5:	0ce45f64934e6d5d7b82a55108596680
Source3:	http://dl.sourceforge.net/ufo2000/%{name}-music-2004.zip
# Source3-md5:	2db2878a55e5df97a198f2310603a5c7
BuildRequires:	allegro-devel
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

%prep
%setup -q -c -n %{name}_%{version} -a2
find -name .svn | xargs rm -rf

# some sound files ..
cd newmusic
	mv readme.txt readme.txt.org
	unzip -q %{SOURCE3}
	mv readme.txt readme.txt-soundtrack
	mv readme.txt.org readme.txt
cd -

# dumb will be linked static
%{__sed} -i -e 's|-laldmb -ldumb|dumb/lib/unix/libaldmb.a dumb/lib/unix/libdumb.a|g' makefile

%build
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

%{__make} \
	CC="%{__cc}" \
	CX="%{__cxx}" \
	OPTFLAGS="%{rpmcflags} -I/usr/include/hawknl -Idumb/include" \
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

find $RPM_BUILD_ROOT%{_datadir}/games/%{name} -type d -print0 | xargs -0 chmod 775

# create menu and icon
install -d $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}

cat > %{name}.desktop << EOF
[Desktop Entry]
Name=UFO2000
Comment=UFO2000 is a turn based tactical squad simulation multiplayer game
Exec=%{name}
Icon=%{name}.png
Terminal=false
Encoding=UTF-8
Categories=Game;StrategyGame;
Type=Application
EOF
install -d $RPM_BUILD_ROOT%{_desktopdir}
install %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING *.txt *.html readme_select.ini
%doc docs/*
%attr(755,root,root) %{_bindir}/ufo2000
%attr(755,root,root) %{_bindir}/ufo2000-srv
%dir %{_datadir}/games/%{name}
%{_datadir}/games/%{name}/*
%{_pixmapsdir}/*.png
%{_desktopdir}/%{name}*.desktop
