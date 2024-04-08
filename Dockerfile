ADD file:b86ae1c7ca3586d8feedcd9ff1b2b1e8ab872caf6587618f1da689045a5d7ae4 in /

CMD ["bash"]

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

ENV LANG=C.UTF-8

RUN /bin/sh -c set -eux; 	apt-get update; 	apt-get install -y --no-install-recommends ca-certificates netbase tzdata;rm -rf /var/lib/apt/lists/* # buildkit

ENV GPG_KEY=A035C8C19219BA821ECEA86B64E628F8D684696D

ENV PYTHON_VERSION=3.11.8

RUN /bin/sh -c set -eux; savedAptMark="$(apt-mark showmanual)"; apt-get update; apt-get install -y --no-install-recommends dpkg-dev gcc	gnupg	libbluetooth-dev libbz2-dev libc6-dev libdb-dev libexpat1-dev	libffi-dev libgdbm-dev liblzma-dev libncursesw5-dev libreadline-dev libsqlite3-dev libssl-dev make tk-dev uuid-dev wget xz-utils zlib1g-dev; wget -O python.tar.xz "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz"; wget -O python.tar.xz.asc "https://www.python.org/ftp/python/${PYTHON_VERSION%%[a-z]*}/Python-$PYTHON_VERSION.tar.xz.asc"; GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys "$GPG_KEY"; gpg --batch --verify python.tar.xz.asc python.tar.xz; gpgconf --kill all; rm -rf "$GNUPGHOME" python.tar.xz.asc; mkdir -p /usr/src/python; tar --extract --directory /usr/src/python --strip-components=1 --file python.tar.xz; rm python.tar.xz; cd /usr/src/python; gnuArch="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)"; ./configure --build="$gnuArch" --enable-loadable-sqlite-extensions --enable-optimizations --enable-option-checking=fatal --enable-shared 		--with-lto 		--with-system-expat 		--without-ensurepip 	; 	nproc="$(nproc)"; 	EXTRA_CFLAGS="$(dpkg-buildflags --get CFLAGS)"; LDFLAGS="$(dpkg-buildflags --get LDFLAGS)"; LDFLAGS="${LDFLAGS:--Wl},--strip-all"; make -j "$nproc" "EXTRA_CFLAGS=${EXTRA_CFLAGS:-}" "LDFLAGS=${LDFLAGS:-}" "PROFILE_TASK=${PROFILE_TASK:-}"; rm python; make -j "$nproc" "EXTRA_CFLAGS=${EXTRA_CFLAGS:-}" "LDFLAGS=${LDFLAGS:--Wl},-rpath='\$\$ORIGIN/../lib'" "PROFILE_TASK=${PROFILE_TASK:-}" python; make install; cd /; rm -rf /usr/src/python; find /usr/local -depth 		\( 			\( -type d -a \( -name test -o -name tests -o -name idle_test \) \) 			-o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \) \) 		\) -exec rm -rf '{}' +; ldconfig; apt-mark auto '.*' > /dev/null; apt-mark manual $savedAptMark; find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec ldd '{}' ';' 		| awk '/=>/ { so = $(NF-1); if (index(so, "/usr/local/") == 1) { next }; gsub("^/(usr/)?", "", so); printf "*%s\n", so }' 		| sort -u 		| xargs -r dpkg-query --search 		| cut -d: -f1 		| sort -u 		| xargs -r apt-mark manual; apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; rm -rf /var/lib/apt/lists/*; python3 --version # buildkit

RUN /bin/sh -c set -eux; 	for src in idle3 pydoc3 python3 python3-config; do 		dst="$(echo "$src" | tr -d 3)"; 		[ -s "/usr/local/bin/$src" ]; 		[ ! -e "/usr/local/bin/$dst" ]; 		ln -svT "$src" "/usr/local/bin/$dst"; 	done # buildkit

ENV PYTHON_PIP_VERSION=24.0

ENV PYTHON_SETUPTOOLS_VERSION=65.5.1

ENV PYTHON_GET_PIP_URL=https://github.com/pypa/get-pip/raw/dbf0c85f76fb6e1ab42aa672ffca6f0a675d9ee4/public/get-pip.py

ENV PYTHON_GET_PIP_SHA256=dfe9fd5c28dc98b5ac17979a953ea550cec37ae1b47a5116007395bfacff2ab9

RUN /bin/sh -c set -eux; 		savedAptMark="$(apt-mark showmanual)"; 	apt-get update; 	apt-get install -y --no-install-recommends wget; 		wget -O get-pip.py "$PYTHON_GET_PIP_URL"; 	echo "$PYTHON_GET_PIP_SHA256 *get-pip.py" | sha256sum -c -; 		apt-mark auto '.*' > /dev/null; 	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; 	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; 	rm -rf /var/lib/apt/lists/*; 		export PYTHONDONTWRITEBYTECODE=1; 		python get-pip.py 		--disable-pip-version-check 		--no-cache-dir 		--no-compile 		"pip==$PYTHON_PIP_VERSION" 		"setuptools==$PYTHON_SETUPTOOLS_VERSION" 	; 	rm -f get-pip.py; 		pip --version # buildkit

CMD ["python3"]

RUN /bin/sh -c apt-get update -qq     && apt-get install --no-install-recommends -y         ffmpeg         build-essential         gcc         cmake         libcairo2-dev         libffi-dev         libpango1.0-dev         freeglut3-dev         pkg-config         make         wget         ghostscript # buildkit

ENV PATH=/usr/local/texlive/bin/armhf-linux:/usr/local/texlive/bin/aarch64-linux:/usr/local/texlive/bin/x86_64-linux:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN /bin/sh -c wget -O /tmp/install-tl-unx.tar.gz http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz &&     mkdir /tmp/install-tl &&     tar -xzf /tmp/install-tl-unx.tar.gz -C /tmp/install-tl --strip-components=1 &&     /tmp/install-tl/install-tl --profile=/tmp/texlive-profile.txt     && tlmgr install         amsmath babel-english cbfonts-fd cm-super ctex doublestroke dvisvgm everysel         fontspec frcursive fundus-calligra gnu-freefont jknapltx latex-bin         mathastext microtype ms physics preview ragged2e relsize rsfs         setspace standalone tipa wasy wasysym xcolor xetex xkeyval # buildkit

COPY . /opt/manim # buildkit

WORKDIR /opt/manim

RUN /bin/sh -c pip install --no-cache .[jupyterlab] # buildkit

RUN /bin/sh -c pip install -r docs/requirements.txt # buildkit

ARG NB_USER=manimuser

ARG NB_UID=1000

ENV USER=manimuser

ENV NB_UID=1000

ENV HOME=/manim

RUN |2 NB_USER=manimuser NB_UID=1000 /bin/sh -c adduser --disabled-password     --gecos "Default user"     --uid ${NB_UID}     ${NB_USER} # buildkit

WORKDIR /manim

USER root

RUN |2 NB_USER=manimuser NB_UID=1000 /bin/sh -c chown -R ${NB_USER}:${NB_USER} ${HOME} # buildkit

RUN |2 NB_USER=manimuser NB_UID=1000 /bin/sh -c chmod 777 ${HOME} # buildkit

USER manimuser

CMD ["/bin/bash"]

