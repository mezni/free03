use serde::{Deserialize, Serialize};
use validator::Validate;
use crate::shared::result::AppResult;
use crate::shared::result::validation_error;

#[derive(Debug, Clone, Serialize, Deserialize, Validate)]
pub struct User {
    pub id: String,
    #[validate(email(message = "Invalid email format"))]
    pub email: String,
    #[validate(length(min = 1, max = 50, message = "Username must be between 1 and 50 characters"))]
    pub username: String,
    #[validate(length(min = 1, max = 100, message = "First name must be between 1 and 100 characters"))]
    pub first_name: String,
    #[validate(length(min = 1, max = 100, message = "Last name must be between 1 and 100 characters"))]
    pub last_name: String,
    pub enabled: bool,
    pub email_verified: bool,
    pub created_at: Option<i64>,
    pub updated_at: Option<i64>,
}

impl User {
    pub fn new(
        id: String,
        email: String,
        username: String,
        first_name: String,
        last_name: String,
    ) -> AppResult<Self> {
        let user = Self {
            id,
            email,
            username,
            first_name,
            last_name,
            enabled: true,
            email_verified: false,
            created_at: Some(chrono::Utc::now().timestamp()),
            updated_at: Some(chrono::Utc::now().timestamp()),
        };

        user.validate_fields()?;
        Ok(user)
    }

    pub fn validate_fields(&self) -> AppResult<()> {
        // Use a different method name to avoid infinite recursion
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }

    // Add this method to fix the error
    pub fn is_active(&self) -> bool {
        self.enabled
    }

    // Additional helper methods
    pub fn activate(&mut self) {
        self.enabled = true;
        self.updated_at = Some(chrono::Utc::now().timestamp());
    }

    pub fn deactivate(&mut self) {
        self.enabled = false;
        self.updated_at = Some(chrono::Utc::now().timestamp());
    }

    pub fn verify_email(&mut self) {
        self.email_verified = true;
        self.updated_at = Some(chrono::Utc::now().timestamp());
    }

    pub fn update_profile(&mut self, first_name: Option<String>, last_name: Option<String>) -> AppResult<()> {
        if let Some(fname) = first_name {
            self.first_name = fname;
        }
        if let Some(lname) = last_name {
            self.last_name = lname;
        }
        self.updated_at = Some(chrono::Utc::now().timestamp());
        self.validate_fields()?;
        Ok(())
    }

    pub fn get_full_name(&self) -> String {
        format!("{} {}", self.first_name, self.last_name)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, Validate)]
pub struct CreateUserRequest {
    #[validate(email(message = "Invalid email format"))]
    pub email: String,
    #[validate(length(min = 1, max = 50, message = "Username must be between 1 and 50 characters"))]
    pub username: String,
    #[validate(length(min = 1, max = 100, message = "First name must be between 1 and 100 characters"))]
    pub first_name: String,
    #[validate(length(min = 1, max = 100, message = "Last name must be between 1 and 100 characters"))]
    pub last_name: String,
    #[validate(length(min = 8, message = "Password must be at least 8 characters long"))]
    pub password: String,
}

impl CreateUserRequest {
    pub fn validate_fields(&self) -> AppResult<()> {
        // Use a different method name to avoid infinite recursion
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, Validate)]
pub struct UpdateUserRequest {
    #[validate(length(min = 1, max = 100, message = "First name must be between 1 and 100 characters"))]
    pub first_name: Option<String>,
    #[validate(length(min = 1, max = 100, message = "Last name must be between 1 and 100 characters"))]
    pub last_name: Option<String>,
    pub enabled: Option<bool>,
}

impl UpdateUserRequest {
    pub fn validate_fields(&self) -> AppResult<()> {
        // Use a different method name to avoid infinite recursion
        if let Err(e) = self.validate() {
            return Err(validation_error(&e.to_string()));
        }
        Ok(())
    }

    pub fn is_empty(&self) -> bool {
        self.first_name.is_none() && self.last_name.is_none() && self.enabled.is_none()
    }
}