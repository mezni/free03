use crate::domain::entities::companies::Company; // Fixed import
use crate::domain::repositories::CompanyRepository; // Fixed import
use crate::shared::errors::AppError;
use async_trait::async_trait;

pub struct GetCompanyQuery {
    pub company_id: i32,
}

pub struct GetCompanyByNetworkQuery {
    pub network_id: i32,
}

pub struct CompanyResponse {
    pub company: Company,
}

#[async_trait]
pub trait CompanyQueryHandler: Send + Sync {
    async fn handle_get(&self, query: GetCompanyQuery) -> Result<CompanyResponse, AppError>;
    async fn handle_get_by_network(
        &self,
        query: GetCompanyByNetworkQuery,
    ) -> Result<CompanyResponse, AppError>;
}

pub struct CompanyQueryHandlerImpl {
    company_repository: Box<dyn CompanyRepository>,
}

impl CompanyQueryHandlerImpl {
    pub fn new(company_repository: Box<dyn CompanyRepository>) -> Self {
        Self { company_repository }
    }
}

#[async_trait]
impl CompanyQueryHandler for CompanyQueryHandlerImpl {
    async fn handle_get(&self, query: GetCompanyQuery) -> Result<CompanyResponse, AppError> {
        let company = self
            .company_repository
            .find_by_id(query.company_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Company with id {} not found", query.company_id))
            })?;

        Ok(CompanyResponse { company })
    }

    async fn handle_get_by_network(
        &self,
        query: GetCompanyByNetworkQuery,
    ) -> Result<CompanyResponse, AppError> {
        let company = self
            .company_repository
            .find_by_network_id(query.network_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!(
                    "Company for network id {} not found",
                    query.network_id
                ))
            })?;

        Ok(CompanyResponse { company })
    }
}
