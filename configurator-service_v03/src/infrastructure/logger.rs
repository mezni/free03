use tracing_subscriber::{fmt, EnvFilter};

/// Initialize the global logger
pub fn init_logger() {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .with_target(false) // hide module path
        .with_level(true)   // show log level
        .with_timer(fmt::time::ChronoUtc::rfc3339()) // ISO timestamp
        .init();
}
