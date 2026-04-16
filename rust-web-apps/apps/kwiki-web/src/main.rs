use axum::{
    extract::State,
    response::Json,
    routing::get,
    Router,
};
use serde::Serialize;
use std::{env, net::SocketAddr};

#[derive(Clone)]
struct AppState {
    app_name: &'static str,
}

#[derive(Serialize)]
struct HealthResponse {
    status: &'static str,
    service: &'static str,
}

#[derive(Serialize)]
struct HomeResponse {
    message: &'static str,
    app: &'static str,
}

#[tokio::main]
async fn main() {
    let state = AppState { app_name: "kwiki-web" };

    let app = Router::new()
        .route("/", get(home))
        .route("/health", get(health))
        .with_state(state);

    let port = env::var("KWIKI_WEB_PORT")
        .ok()
        .and_then(|v| v.parse::<u16>().ok())
        .unwrap_or(3000);

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    println!("kwiki-web listening on http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr)
        .await
        .expect("failed to bind kwiki-web listener");
    axum::serve(listener, app)
        .await
        .expect("kwiki-web server failed");
}

async fn health(State(state): State<AppState>) -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "ok",
        service: state.app_name,
    })
}

async fn home(State(state): State<AppState>) -> Json<HomeResponse> {
    Json(HomeResponse {
        message: "Kwiki Rust web app is alive",
        app: state.app_name,
    })
}
