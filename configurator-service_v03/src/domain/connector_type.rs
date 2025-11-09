use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, sqlx::FromRow, Clone)]
pub struct ConnectorType {
    pub id: i32,
    pub name: String,
    pub description: Option<String>,
}
