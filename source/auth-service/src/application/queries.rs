use serde::{Deserialize, Serialize};
use validator::Validate;
use crate::shared::result::{AppResult, validation_error};

#[derive(Debug, Validate, Deserialize)]
pub struct GetUserQuery {
    #[validate(length(min = 1, message = "User ID is required"))]
    pub user_id: String,
}

impl GetUserQuery {
    pub fn new(user_id: String) -> AppResult<Self> {
        let query = Self { user_id };
        query.validate()?;
        Ok(query)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct GetUserRolesQuery {
    #[validate(length(min = 1, message = "User ID is required"))]
    pub user_id: String,
}

impl GetUserRolesQuery {
    pub fn new(user_id: String) -> AppResult<Self> {
        let query = Self { user_id };
        query.validate()?;
        Ok(query)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct GetUserPermissionsQuery {
    #[validate(length(min = 1, message = "User ID is required"))]
    pub user_id: String,
}

impl GetUserPermissionsQuery {
    pub fn new(user_id: String) -> AppResult<Self> {
        let query = Self { user_id };
        query.validate()?;
        Ok(query)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct CheckPermissionQuery {
    #[validate(length(min = 1, message = "User ID is required"))]
    pub user_id: String,
    
    #[validate(length(min = 1, message = "Permission is required"))]
    pub permission: String,
}

impl CheckPermissionQuery {
    pub fn new(user_id: String, permission: String) -> AppResult<Self> {
        let query = Self { user_id, permission };
        query.validate()?;
        Ok(query)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }
}

#[derive(Debug, Validate, Deserialize)]
pub struct ListUsersQuery {
    pub page: Option<u32>,
    pub size: Option<u32>,
    pub search: Option<String>,
    pub enabled: Option<bool>,
}

impl ListUsersQuery {
    pub fn new(
        page: Option<u32>,
        size: Option<u32>,
        search: Option<String>,
        enabled: Option<bool>,
    ) -> AppResult<Self> {
        let query = Self {
            page,
            size,
            search,
            enabled,
        };
        query.validate()?;
        Ok(query)
    }

    fn validate(&self) -> AppResult<()> {
        self.validate()
            .map_err(|e| validation_error(&e.to_string()))?;
        Ok(())
    }

    pub fn page(&self) -> u32 {
        self.page.unwrap_or(1).max(1)
    }

    pub fn size(&self) -> u32 {
        self.size
            .unwrap_or(crate::shared::constants::DEFAULT_PAGE_SIZE)
            .min(crate::shared::constants::MAX_PAGE_SIZE)
            .max(1)
    }

    pub fn offset(&self) -> u32 {
        (self.page() - 1) * self.size()
    }
}