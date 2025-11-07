// Simple middleware file for now - remove complex middleware
use actix_web_httpauth::extractors::bearer::{BearerAuth, Config};
use actix_web_httpauth::extractors::AuthenticationError;
use actix_web::{dev::ServiceRequest, Error};

pub async fn validator(
    req: ServiceRequest,
    credentials: BearerAuth,
) -> Result<ServiceRequest, (Error, ServiceRequest)> {
    // Simple validator - always return success for now
    // In production, you would validate the token here
    Ok(req)
}

#[derive(Debug, Clone)]
pub struct UserContext {
    pub user_id: String,
    pub username: String,
    pub email: String,
    pub roles: Vec<String>,
    pub permissions: Vec<String>,
}

impl UserContext {
    pub fn has_role(&self, role: &str) -> bool {
        self.roles.iter().any(|r| r == role)
    }

    pub fn has_permission(&self, permission: &str) -> bool {
        self.permissions.iter().any(|p| p == permission)
    }

    pub fn is_admin(&self) -> bool {
        self.has_role("admin") || self.has_role("super_admin")
    }
}