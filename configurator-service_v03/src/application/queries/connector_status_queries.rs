use crate::domain::connector_status::ConnectorStatus;
use crate::infrastructure::repositories::connector_status_repo::ConnectorStatusRepository;
use crate::shared::errors::AppError;
use tracing::debug;

#[derive(Clone)]
pub struct GetConnectorStatusesQuery {
    pub repo: ConnectorStatusRepository,
}

impl GetConnectorStatusesQuery {
    pub fn new(repo: ConnectorStatusRepository) -> Self {
        Self { repo }
    }

    pub async fn execute(&self) -> Result<Vec<ConnectorStatus>, AppError> {
        debug!("Query executed: Get all connector statuses");
        self.repo.get_all().await
    }
}
