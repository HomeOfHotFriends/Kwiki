use axum::{
    response::Json,
    routing::get,
    Router,
};
use serde::{Deserialize, Serialize};
use std::{collections::HashMap, env, fs, net::SocketAddr, path::PathBuf};

#[derive(Serialize)]
struct AdminStatus {
    status: &'static str,
    area: &'static str,
}

#[derive(Serialize)]
struct Metrics {
    metadata_path: String,
    read_ok: bool,
    wiki_pages: usize,
    concept_count: usize,
    page_count: usize,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<String>,
}

#[derive(Deserialize)]
struct Metadata {
    #[serde(default)]
    pages: HashMap<String, serde_json::Value>,
    #[serde(default)]
    concept_count: usize,
    #[serde(default)]
    page_count: usize,
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
    let metadata_path = env::var("KWIKI_METADATA_PATH")
        .map(PathBuf::from)
        .unwrap_or_else(|_| PathBuf::from("../scripts/metadata.json"));

    let path_str = metadata_path.to_string_lossy().to_string();

    match fs::read_to_string(&metadata_path) {
        Ok(raw) => match serde_json::from_str::<Metadata>(&raw) {
            Ok(meta) => Json(Metrics {
                metadata_path: path_str,
                read_ok: true,
                wiki_pages: meta.pages.len(),
                concept_count: meta.concept_count,
                page_count: meta.page_count,
                error: None,
            }),
            Err(e) => Json(Metrics {
                metadata_path: path_str,
                read_ok: false,
                wiki_pages: 0,
                concept_count: 0,
                page_count: 0,
                error: Some(format!("invalid json: {e}")),
            }),
        },
        Err(e) => Json(Metrics {
            metadata_path: path_str,
            read_ok: false,
            wiki_pages: 0,
            concept_count: 0,
            page_count: 0,
            error: Some(format!("read failed: {e}")),
        }),
    }
}
