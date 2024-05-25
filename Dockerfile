ARG UBUNTU_VERSION=22.04

FROM nvidia/opengl:1.2-glvnd-runtime-ubuntu${UBUNTU_VERSION}
MAINTAINER vkhurana@users.noreply.github.com

ARG LABEL_VERSION="python3"

LABEL name="docker-prusaslicer" \
    version=${LABEL_VERSION} \
    description="Monitors a folders for .stl files and slices using prusaslicer CLI" \
    maintainer="Vivek Khurana <vkhurana@users.noreply.github.com>"

ENV TZ=Etc/UTC
ENV DEBIAN_FRONTEND noninteractive

# Install some basic dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget libegl1-mesa libgl1-mesa-glx \
    libpam0g python3 python3-pip \
    locales locales-all pcmanfm jq curl git bzip2 gpg-agent software-properties-common \
    openscad \
    libwx-perl libxmu-dev libgl1-mesa-glx libgl1-mesa-dri \
    # Clean everything up.
    && apt autoclean -y \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Install Prusaslicer.
WORKDIR /slic3r
ADD requirements.txt /slic3r
ADD slice.py /slic3r
ADD slicer.sh /slic3r

RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x /slic3r/slicer.sh \
  && latestSlic3r=$(/slic3r/slicer.sh url) \
  && slic3rReleaseName=$(/slic3r/slicer.sh name) \
  && curl -sSL ${latestSlic3r} > ${slic3rReleaseName} \
  && rm -f /slic3r/releaseInfo.json \
  && mkdir -p /slic3r/slic3r-dist \
  && tar -xjf ${slic3rReleaseName} -C /slic3r/slic3r-dist --strip-components 1 \
  && rm -f /slic3r/${slic3rReleaseName} \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get autoclean \
  && mkdir -p /slic3r \
  && mkdir -p /configs \
  && mkdir -p /prints/ \
  && locale-gen en_US \
  && mkdir /configs/.local \
  && mkdir -p /configs/.config/ \
  && ln -s /configs/.config/ $HOME \
  && mkdir -p $HOME/.config/

VOLUME /configs/
VOLUME /prints/

ENTRYPOINT ["python3","-u", "/slic3r/slice.py"]