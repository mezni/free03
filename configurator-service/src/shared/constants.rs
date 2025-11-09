// Database constants
pub const DEFAULT_PAGE_SIZE: u32 = 20;
pub const MAX_PAGE_SIZE: u32 = 100;

// Network types
#[derive(Debug, Clone, Copy, PartialEq, Eq, serde::Serialize, serde::Deserialize)] // Added Serde derives
pub enum NetworkType {
    Individual,
    Company,
}

impl NetworkType {
    pub fn as_str(&self) -> &'static str {
        match self {
            NetworkType::Individual => "individual",
            NetworkType::Company => "company",
        }
    }

    pub fn from_str(s: &str) -> Option<Self> {
        match s.to_lowercase().as_str() {
            "individual" => Some(NetworkType::Individual),
            "company" => Some(NetworkType::Company),
            _ => None,
        }
    }
}

// Validation constants
pub const MAX_NAME_LENGTH: usize = 255;
pub const MAX_EMAIL_LENGTH: usize = 255;
pub const MAX_PHONE_LENGTH: usize = 50;
pub const MAX_BUSINESS_REG_NUMBER_LENGTH: usize = 100;
pub const MAX_WEBSITE_URL_LENGTH: usize = 255;

// API constants
pub const API_VERSION: &str = "v1";
pub const API_PREFIX: &str = "/api/v1";

// Date formats
pub const DATE_FORMAT: &str = "%Y-%m-%d";
pub const DATETIME_FORMAT: &str = "%Y-%m-%d %H:%M:%S";
