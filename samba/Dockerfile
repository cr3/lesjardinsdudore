FROM debian:bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends samba samba-common-bin \
 && rm -rf /var/lib/apt/lists/*

COPY docker-entrypoint.sh /

EXPOSE 137/udp 138/udp 139/tcp 445/tcp

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["smbd", "--foreground", "--no-process-group"]
