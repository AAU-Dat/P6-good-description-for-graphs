FROM eclipse-temurin:11-jdk-alpine

# Build time arguments
ARG version=10.2.0

ENV GRAPHDB_PARENT_DIR=/opt/graphdb
ENV GRAPHDB_HOME=${GRAPHDB_PARENT_DIR}/home
ENV GRAPHDB_IMPORT=${GRAPHDB_PARENT_DIR}/import

ENV GRAPHDB_INSTALL_DIR=${GRAPHDB_PARENT_DIR}/dist

WORKDIR /tmp

RUN apk add --no-cache bash curl util-linux procps net-tools busybox-extras wget less libc6-compat && \
    curl -fsSL "https://maven.ontotext.com/repository/owlim-releases/com/ontotext/graphdb/graphdb/${version}/graphdb-${version}-dist.zip" > \
    graphdb-${version}.zip && \
    bash -c 'md5sum -c - <<<"$(curl -fsSL https://maven.ontotext.com/repository/owlim-releases/com/ontotext/graphdb/graphdb/${version}/graphdb-${version}-dist.zip.md5)  graphdb-${version}.zip"' && \
    mkdir -p ${GRAPHDB_PARENT_DIR} && \
    cd ${GRAPHDB_PARENT_DIR} && \
    unzip /tmp/graphdb-${version}.zip && \
    rm /tmp/graphdb-${version}.zip && \
    mv graphdb-${version} dist && \
    mkdir -p ${GRAPHDB_HOME} && \
    ln -s /lib/libc.musl-x86_64.so.1 /lib/ld-linux-x86-64.so.2 

ENV PATH=${GRAPHDB_INSTALL_DIR}/bin:$PATH

COPY database ${GRAPHDB_IMPORT}
RUN importrdf -Dgraphdb.home.data=/opt/graphdb/home/data load -c ${GRAPHDB_IMPORT}/graphdb-repo-config.ttl -m parallel ${GRAPHDB_IMPORT}/pokemon-db.ttl

RUN importrdf -Dgraphdb.home.data=/opt/graphdb/home/data load -c ${GRAPHDB_IMPORT}/graphdb-repo-config-one-million.ttl -m parallel ${GRAPHDB_IMPORT}/one-million.nt

CMD ["-Dgraphdb.home=/opt/graphdb/home"]

ENTRYPOINT ["/opt/graphdb/dist/bin/graphdb"]

EXPOSE 7200
EXPOSE 7300