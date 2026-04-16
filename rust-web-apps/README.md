# Rust Web Apps

This folder contains two Rust web apps in one Cargo workspace:

- `kwiki-web`: public-facing JSON + health endpoints
- `kwiki-admin`: minimal admin/status service

## Prerequisites

Install Rust (cargo + rustc), then run:

```bash
cd rust-web-apps
cargo run -p kwiki-web
```

In another terminal:

```bash
cd rust-web-apps
cargo run -p kwiki-admin
```

## Default Ports

- `kwiki-web`: `3000`
- `kwiki-admin`: `3001`

You can override ports with env vars:

- `KWIKI_WEB_PORT`
- `KWIKI_ADMIN_PORT`

## Admin Metrics Source

`kwiki-admin` reads metadata from `../scripts/metadata.json` by default.

You can override this path with:

- `KWIKI_METADATA_PATH`
