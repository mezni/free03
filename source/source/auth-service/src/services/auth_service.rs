use crate::domain::user::User;
use crate::repositories::{keycloak_repo::KeycloakRepo, cache_repo::CacheRepo};
use crate::errors::AppError;

#[derive(Clone)]
pub struct AuthService {
    keycloak: KeycloakRepo,
    cache: CacheRepo,
}

impl AuthService {
    pub fn new(keycloak: KeycloakRepo, cache: CacheRepo) -> Self {
        Self { keycloak, cache }
    }

    pub async fn authenticate(&self, username: &str, password: &str) -> Result<User, AppError> {
        // Check cache first
        if let Some(user) = self.cache.get_user(username).await {
            return Ok(user);
        }

        // Authenticate with Keycloak
        let user = self.keycloak.authenticate_user(username, password).await?;
        self.cache.set_user(&user).await;
        Ok(user)
    }

    pub async fn validate_token(&self, token: &str) -> Result<User, AppError> {
        self.keycloak.validate_token(token).await
    }
}
