use crate::domain::connector_type::ConnectorType;
use crate::infrastructure::repositories::connector_type_repo::ConnectorTypeRepository;
use crate::shared::errors::AppError;
use tracing::info;

#[derive(Clone)]
pub struct CreateConnectorTypeCommand {
    pub repo: ConnectorTypeRepository,
}

impl CreateConnectorTypeCommand {
    pub fn new(repo: ConnectorTypeRepository) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, name: String, description: Option<String>) -> Result<(), AppError> {
        let ct = ConnectorType {
            id: 0,
            name,
            description,
        };

        self.repo.insert(&ct).await?;
        info!("Command executed: Created ConnectorType {}", ct.name);
        Ok(())
    }
}
