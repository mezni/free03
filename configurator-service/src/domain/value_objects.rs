pub const MAX_CITY_LENGTH: usize = 100;
pub const MAX_STATE_LENGTH: usize = 100;
pub const MAX_COUNTRY_LENGTH: usize = 100;
pub const MAX_POSTAL_CODE_LENGTH: usize = 20;

use crate::shared::errors::AppError;
use serde::{Deserialize, Serialize};
use std::fmt;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct Email {
    value: String,
}

impl Email {
    pub fn new(email: &str) -> Result<Self, AppError> {
        if email.is_empty() {
            return Err(AppError::Validation("Email cannot be empty".to_string()));
        }

        if email.len() > crate::shared::constants::MAX_EMAIL_LENGTH {
            return Err(AppError::Validation(format!(
                "Email cannot exceed {} characters",
                crate::shared::constants::MAX_EMAIL_LENGTH
            )));
        }

        // Basic email validation
        if !email.contains('@') || !email.contains('.') {
            return Err(AppError::Validation("Invalid email format".to_string()));
        }

        Ok(Self {
            value: email.to_lowercase(),
        })
    }

    pub fn value(&self) -> &str {
        &self.value
    }
}

impl fmt::Display for Email {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct PhoneNumber {
    value: String,
}

impl PhoneNumber {
    pub fn new(phone: &str) -> Result<Self, AppError> {
        if phone.is_empty() {
            return Err(AppError::Validation(
                "Phone number cannot be empty".to_string(),
            ));
        }

        if phone.len() > crate::shared::constants::MAX_PHONE_LENGTH {
            return Err(AppError::Validation(format!(
                "Phone number cannot exceed {} characters",
                crate::shared::constants::MAX_PHONE_LENGTH
            )));
        }

        // Basic phone number validation (allow only digits, spaces, hyphens, and parentheses)
        if !phone
            .chars()
            .all(|c| c.is_ascii_digit() || c == ' ' || c == '-' || c == '(' || c == ')' || c == '+')
        {
            return Err(AppError::Validation(
                "Invalid phone number format".to_string(),
            ));
        }

        Ok(Self {
            value: phone.to_string(),
        })
    }

    pub fn value(&self) -> &str {
        &self.value
    }
}

impl fmt::Display for PhoneNumber {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct WebsiteUrl {
    value: String,
}

impl WebsiteUrl {
    pub fn new(url: &str) -> Result<Self, AppError> {
        if url.is_empty() {
            return Err(AppError::Validation(
                "Website URL cannot be empty".to_string(),
            ));
        }

        if url.len() > crate::shared::constants::MAX_WEBSITE_URL_LENGTH {
            return Err(AppError::Validation(format!(
                "Website URL cannot exceed {} characters",
                crate::shared::constants::MAX_WEBSITE_URL_LENGTH
            )));
        }

        // Basic URL validation
        if !url.starts_with("http://") && !url.starts_with("https://") {
            return Err(AppError::Validation(
                "Website URL must start with http:// or https://".to_string(),
            ));
        }

        Ok(Self {
            value: url.to_string(),
        })
    }

    pub fn value(&self) -> &str {
        &self.value
    }
}

impl fmt::Display for WebsiteUrl {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct BusinessRegistrationNumber {
    value: String,
}

impl BusinessRegistrationNumber {
    pub fn new(number: &str) -> Result<Self, AppError> {
        if number.is_empty() {
            return Err(AppError::Validation(
                "Business registration number cannot be empty".to_string(),
            ));
        }

        if number.len() > crate::shared::constants::MAX_BUSINESS_REG_NUMBER_LENGTH {
            return Err(AppError::Validation(format!(
                "Business registration number cannot exceed {} characters",
                crate::shared::constants::MAX_BUSINESS_REG_NUMBER_LENGTH
            )));
        }

        Ok(Self {
            value: number.to_string(),
        })
    }

    pub fn value(&self) -> &str {
        &self.value
    }
}

impl fmt::Display for BusinessRegistrationNumber {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct City {
    value: String,
}

impl City {
    pub fn new(city: &str) -> Result<Self, AppError> {
        if city.is_empty() {
            return Err(AppError::Validation("City cannot be empty".to_string()));
        }
        if city.len() > MAX_CITY_LENGTH {
            return Err(AppError::Validation(format!(
                "City cannot exceed {} characters",
                MAX_CITY_LENGTH
            )));
        }
        Ok(Self {
            value: city.to_string(),
        })
    }

    pub fn value(&self) -> &str {
        &self.value
    }
}

impl fmt::Display for City {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.value)
    }
}
