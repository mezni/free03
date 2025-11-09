// Domain module structure

// Re-export value objects
pub mod value_objects;
pub use value_objects::*;

// Re-export models
pub mod models;
pub use models::*;

// Re-export repositories
pub mod repositories;
pub use repositories::*;

// Domain services (if you have any domain services)
pub mod services;

// Domain events (if you're using event sourcing)
pub mod events;

// Common domain traits and utilities
pub mod traits;

// Aggregate roots (if you're using aggregates)
pub mod aggregates;