use crate::domain::station::Station;
use crate::infrastructure::repositories::station_repo::StationRepository;
use crate::shared::errors::AppError;
use tracing::debug;

#[derive(Clone)]
pub struct GetStationsQuery {
    pub repo: StationRepository,
}

impl GetStationsQuery {
    pub fn new(repo: StationRepository) -> Self {
        Self { repo }
    }

    pub async fn execute(&self, limit: i64, offset: i64) -> Result<Vec<Station>, AppError> {
        debug!("Query executed: Get stations (limit={}, offset={})", limit, offset);
        self.repo.get_stations(limit, offset).await
    }
}
