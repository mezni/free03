use crate::domain::user::User;
use crate::errors::AppError;

#[derive(Clone)]
pub struct KeycloakRepo {
    pub base_url: String,
    pub realm: String,
    pub client_id: String,
    pub client_secret: String,
}

impl KeycloakRepo {
    pub fn new(base_url: String, realm: String, client_id: String, client_secret: String) -> Self {
        Self {
            base_url,
            realm,
            client_id,
            client_secret,
        }
    }

    pub async fn authenticate_user(&self, _username: &str, _password: &str) -> Result<User, AppError> {
        // TODO: Call Keycloak token endpoint
        unimplemented!()
    }

    pub async fn validate_token(&self, _token: &str) -> Result<User, AppError> {
        // TODO: Decode JWT & validate
        unimplemented!()
    }
}
