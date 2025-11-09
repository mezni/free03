use std::env;

pub fn init_logger() {
    // Load .env file if using dotenvy
    if let Ok(_) = dotenvy::dotenv() {
        println!("Loaded .env file");
    }

    // Check both RUST_LOG and LOG_LEVEL environment variables
    let rust_log = env::var("RUST_LOG")
        .or_else(|_| env::var("LOG_LEVEL"))
        .unwrap_or_else(|_| {
            // If neither is set, default to "info"
            unsafe {
                env::set_var("RUST_LOG", "info");
            }
            "info".to_string()
        });

    // Also set RUST_LOG to ensure env_logger uses it
    if env::var("RUST_LOG").is_err() {
        unsafe {
            env::set_var("RUST_LOG", &rust_log);
        }
    }

    println!("Setting log level to: {}", rust_log);

    env_logger::Builder::from_default_env()
        .format_timestamp_secs()
        .format_module_path(false)
        .format_target(false)
        .init();

    log::info!("Logger initialized successfully");
    log::debug!("Debug logging enabled");
    log::warn!("Warning logging enabled");
    log::error!("Error logging enabled");
}
