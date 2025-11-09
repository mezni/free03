use async_trait::async_trait;
use sqlx::FromRow;
use crate::shared::errors::AppError;
use crate::domain::connector_type_model::{ConnectorType, ConnectorTypeId};
use crate::domain::connector_type_repo::ConnectorTypeRepository;

#[derive(Debug, FromRow)]
struct ConnectorTypeModel {
    id: i32,
    name: String,
    description: Option<String>,
}

impl ConnectorTypeModel {
    fn to_entity(&self) -> Result<ConnectorType, AppError> {
        ConnectorType::new(
            ConnectorTypeId::new(self.id),
            self.name.clone(),
            self.description.clone(),
        )
    }
}

#[derive(Clone)]
pub struct ConnectorTypeRepositoryImpl {
    pool: sqlx::PgPool,
}

impl ConnectorTypeRepositoryImpl {
    pub fn new(pool: sqlx::PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl ConnectorTypeRepository for ConnectorTypeRepositoryImpl {
    async fn find_by_id(&self, id: ConnectorTypeId) -> Result<Option<ConnectorType>, AppError> {
        let model = sqlx::query_as::<_, ConnectorTypeModel>(
            "SELECT id, name, description FROM connector_types WHERE id = $1"
        )
        .bind(id.value())
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| AppError::database(e.to_string()))?;
        
        model.map(|m| m.to_entity()).transpose()
    }
    
    async fn find_by_name(&self, name: &str) -> Result<Option<ConnectorType>, AppError> {
        let model = sqlx::query_as::<_, ConnectorTypeModel>(
            "SELECT id, name, description FROM connector_types WHERE name = $1"
        )
        .bind(name)
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| AppError::database(e.to_string()))?;
        
        model.map(|m| m.to_entity()).transpose()
    }
    
    async fn list_all(&self) -> Result<Vec<ConnectorType>, AppError> {
        let models = sqlx::query_as::<_, ConnectorTypeModel>(
            "SELECT id, name, description FROM connector_types ORDER BY name"
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| AppError::database(e.to_string()))?;
        
        models.into_iter().map(|m| m.to_entity()).collect()
    }
    
    async fn save(&self, connector_type: &ConnectorType) -> Result<(), AppError> {
        sqlx::query(
            "INSERT INTO connector_types (id, name, description) VALUES ($1, $2, $3) 
             ON CONFLICT (id) DO UPDATE SET name = $2, description = $3"
        )
        .bind(connector_type.id().value())
        .bind(connector_type.name())
        .bind(connector_type.description())
        .execute(&self.pool)
        .await
        .map_err(|e| AppError::database(e.to_string()))?;
        
        Ok(())
    }
    
    async fn delete(&self, id: ConnectorTypeId) -> Result<bool, AppError> {
        let result = sqlx::query("DELETE FROM connector_types WHERE id = $1")
            .bind(id.value())
            .execute(&self.pool)
            .await
            .map_err(|e| AppError::database(e.to_string()))?;
        
        Ok(result.rows_affected() > 0)
    }
}