use crate::domain::connector_status::ConnectorStatus;
use crate::infrastructure::repositories::connector_status_repo::ConnectorStatusRepository;
use crate::shared::errors::AppError;
use tracing::info;

#[derive(Clone)]
pub struct CreateConnectorStatusCommand {
    pub repo: ConnectorStatusRepository,
}

impl CreateConnectorStatusCommand {
    pub fn new(repo: ConnectorStatusRepository) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, name: String, description: Option<String>) -> Result<(), AppError> {
        let cs = ConnectorStatus {
            id: 0,
            name,
            description,
        };

        self.repo.insert(&cs).await?;
        info!("Command executed: Created ConnectorStatus {}", cs.name);
        Ok(())
    }
}
