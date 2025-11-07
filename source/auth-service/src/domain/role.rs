use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Debug, Clone, Serialize, Deserialize, Validate)]
pub struct Role {
    pub id: String,
    #[validate(length(min = 1, max = 50, message = "Role name must be between 1 and 50 characters"))]
    pub name: String,
    pub description: Option<String>,
    pub composite: bool,
    pub client_role: bool,
    pub container_id: String,
}

impl Role {
    pub fn new(
        id: String,
        name: String,
        description: Option<String>,
        composite: bool,
        client_role: bool,
        container_id: String,
    ) -> Self {
        Self {
            id,
            name,
            description,
            composite,
            client_role,
            container_id,
        }
    }

    pub fn validate(&self) -> Result<(), validator::ValidationErrors> {
        self.validate()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RoleMapping {
    pub id: String,
    pub name: String,
    pub description: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserRoleAssignment {
    pub user_id: String,
    pub role_id: String,
    pub role_name: String,
}