use axum::{
    response::Json,
    routing::get,
    Router,
};
use serde::Serialize;
use std::{env, net::SocketAddr};

#[derive(Serialize)]
struct AdminStatus {
    status: &'static str,
    area: &'static str,
}

#[derive(Serialize)]
struct Metrics {
    wiki_pages_hint: usize,
    note: &'static str,
}

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/admin/status", get(admin_status))
        .route("/admin/metrics", get(admin_metrics));

    let port = env::var("KWIKI_ADMIN_PORT")
        .ok()
        .and_then(|v| v.parse::<u16>().ok())
        .unwrap_or(3001);

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("kwiki-admin listening on http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr)
        .await
        .expect("failed to bind kwiki-admin listener");
    axum::serve(listener, app)
        .await
        .expect("kwiki-admin server failed");
}

async fn admin_status() -> Json<AdminStatus> {
    Json(AdminStatus {
        status: "ok",
        area: "admin",
    })
}

async fn admin_metrics() -> Json<Metrics> {
    Json(Metrics {
        wiki_pages_hint: 74,
        note: "replace with live metadata wiring",
    })
}
