use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Debug, Clone, Serialize, Deserialize, Validate)]
pub struct Permission {
    pub id: String,
    #[validate(length(min = 1, max = 100, message = "Permission name must be between 1 and 100 characters"))]
    pub name: String,
    pub description: Option<String>,
    pub resource_type: Option<String>,
    pub scopes: Vec<String>,
}

impl Permission {
    pub fn new(
        id: String,
        name: String,
        description: Option<String>,
        resource_type: Option<String>,
    ) -> Self {
        Self {
            id,
            name,
            description,
            resource_type,
            scopes: Vec::new(),
        }
    }

    pub fn add_scope(&mut self, scope: String) {
        if !self.scopes.contains(&scope) {
            self.scopes.push(scope);
        }
    }

    pub fn remove_scope(&mut self, scope: &str) {
        self.scopes.retain(|s| s != scope);
    }

    pub fn has_scope(&self, scope: &str) -> bool {
        self.scopes.iter().any(|s| s == scope)
    }

    pub fn validate(&self) -> Result<(), validator::ValidationErrors> {
        self.validate()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserPermission {
    pub user_id: String,
    pub permission_id: String,
    pub permission_name: String,
    pub scopes: Vec<String>,
}