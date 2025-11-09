use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize, sqlx::FromRow, Clone)]
pub struct ConnectorStatus {
    pub id: i32,
    pub name: String,
    pub description: Option<String>,
}
