use serde::{Deserialize, Serialize};
use validator::Validate;
use crate::shared::result::{AppResult, validation_error};

#[derive(Debug, Validate, Deserialize)]
pub struct LoginCommand {
    #[validate(length(min = 1, message = "Username is required"))]
    pub username: String,
    
    #[validate(length(min = 1, message = "Password is required"))]
    pub password: String,
}

impl LoginCommand {
    pub fn new(username: String, password: String) -> AppResult<Self> {
        let command = Self { username, password };
        command.validate()?;
        Ok(command)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct RegisterCommand {
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

impl RegisterCommand {
    pub fn new(
        email: String,
        username: String,
        first_name: String,
        last_name: String,
        password: String,
    ) -> AppResult<Self> {
        let command = Self {
            email,
            username,
            first_name,
            last_name,
            password,
        };
        command.validate()?;
        Ok(command)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct AssignRolesCommand {
    #[validate(length(min = 1, message = "User ID is required"))]
    pub user_id: String,
    
    #[validate(length(min = 1, message = "At least one role is required"))]
    pub roles: Vec<String>,
}

impl AssignRolesCommand {
    pub fn new(user_id: String, roles: Vec<String>) -> AppResult<Self> {
        let command = Self { user_id, roles };
        command.validate()?;
        Ok(command)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct ValidateTokenCommand {
    #[validate(length(min = 1, message = "Token is required"))]
    pub token: String,
}

impl ValidateTokenCommand {
    pub fn new(token: String) -> AppResult<Self> {
        let command = Self { token };
        command.validate()?;
        Ok(command)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct RefreshTokenCommand {
    #[validate(length(min = 1, message = "Refresh token is required"))]
    pub refresh_token: String,
}

impl RefreshTokenCommand {
    pub fn new(refresh_token: String) -> AppResult<Self> {
        let command = Self { refresh_token };
        command.validate()?;
        Ok(command)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct LogoutCommand {
    #[validate(length(min = 1, message = "Refresh token is required"))]
    pub refresh_token: String,
}

impl LogoutCommand {
    pub fn new(refresh_token: String) -> AppResult<Self> {
        let command = Self { refresh_token };
        command.validate()?;
        Ok(command)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct UpdateUserCommand {
    #[validate(length(min = 1, message = "User ID is required"))]
    pub user_id: String,
    
    #[validate(length(min = 1, max = 100, message = "First name must be between 1 and 100 characters"))]
    pub first_name: Option<String>,
    
    #[validate(length(min = 1, max = 100, message = "Last name must be between 1 and 100 characters"))]
    pub last_name: Option<String>,
    
    pub enabled: Option<bool>,
}

impl UpdateUserCommand {
    pub fn new(
        user_id: String,
        first_name: Option<String>,
        last_name: Option<String>,
        enabled: Option<bool>,
    ) -> AppResult<Self> {
        let command = Self {
            user_id,
            first_name,
            last_name,
            enabled,
        };
        command.validate()?;
        Ok(command)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }

    pub fn is_empty(&self) -> bool {
        self.first_name.is_none() && self.last_name.is_none() && self.enabled.is_none()
    }
}