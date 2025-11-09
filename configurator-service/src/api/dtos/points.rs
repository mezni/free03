use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct PointDto {
    pub longitude: f64,
    pub latitude: f64,
}

impl From<crate::domain::entities::stations::Point> for PointDto {
    fn from(point: crate::domain::entities::stations::Point) -> Self {
        Self {
            longitude: point.longitude,
            latitude: point.latitude,
        }
    }
}

impl From<PointDto> for crate::domain::entities::stations::Point {
    fn from(dto: PointDto) -> Self {
        Self {
            longitude: dto.longitude,
            latitude: dto.latitude,
        }
    }
}
