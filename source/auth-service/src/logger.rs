// src/logger.rs
use tracing_subscriber::{
    fmt, 
    layer::SubscriberExt, 
    util::SubscriberInitExt,
    Layer,
};

#[cfg(feature = "env-filter")]
use tracing_subscriber::EnvFilter;

pub fn init_logger(config: &crate::config::LogConfig) -> Result<(), Box<dyn std::error::Error>> {
    #[cfg(feature = "env-filter")]
    let filter = EnvFilter::try_from_default_env()
        .or_else(|_| EnvFilter::try_new(&config.level))
        .unwrap_or_else(|_| EnvFilter::new("info"));

    #[cfg(not(feature = "env-filter"))]
    let filter = tracing_subscriber::filter::LevelFilter::INFO;

    // Create the formatter based on the config
    match config.format.to_lowercase().as_str() {
        "json" => {
            let fmt_layer = fmt::layer()
                .json()
                .with_target(true)
                .with_level(true)
                .with_thread_ids(false)
                .with_thread_names(false)
                .boxed();

            tracing_subscriber::registry()
                .with(filter)
                .with(fmt_layer)
                .init();
        }
        _ => {
            let fmt_layer = fmt::layer()
                .with_target(true)
                .with_level(true)
                .with_thread_ids(false)
                .with_thread_names(false)
                .boxed();

            tracing_subscriber::registry()
                .with(filter)
                .with(fmt_layer)
                .init();
        }
    }

    Ok(())
}