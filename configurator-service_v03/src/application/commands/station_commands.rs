use crate::domain::station::Station;
use crate::infrastructure::repositories::station_repo::StationRepository;
use crate::shared::errors::AppError;
use chrono::Utc;
use tracing::info;

#[derive(Clone)]
pub struct CreateStationCommand {
    pub repo: StationRepository,
}

impl CreateStationCommand {
    pub fn new(repo: StationRepository) -> Self {
        Self { repo }
    }

    pub async fn execute(
        &self,
        osm_id: i64,
        name: String,
        address: Option<String>,
        operator: String,
    ) -> Result<(), AppError> {
        let station = Station {
            id: 0,
            osm_id,
            name: name.clone(),
            address,
            operator,
            created_at: Some(Utc::now()),
            updated_at: None,
        };

        self.repo.insert(&station).await?;
        info!("Command executed: Created Station '{}'", name);
        Ok(())
    }
}
