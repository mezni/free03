use crate::domain::connector_type::ConnectorType;
use crate::infrastructure::repositories::connector_type_repo::ConnectorTypeRepository;
use crate::shared::errors::AppError;
use tracing::debug;

#[derive(Clone)]
pub struct GetConnectorTypesQuery {
    pub repo: ConnectorTypeRepository,
}

impl GetConnectorTypesQuery {
    pub fn new(repo: ConnectorTypeRepository) -> Self {
        Self { repo }
    }

    pub async fn execute(&self) -> Result<Vec<ConnectorType>, AppError> {
        debug!("Query executed: Get all connector types");
        self.repo.get_all().await
    }
}
