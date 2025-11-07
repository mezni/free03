// src/shared/mod.rs
pub mod error;
pub mod result;
pub mod constants;
pub mod types;

// Re-exports
pub use error::AppError;
pub use result::AppResult;
pub use constants::*;
pub use types::*;