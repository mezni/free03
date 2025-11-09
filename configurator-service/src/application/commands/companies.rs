use crate::domain::entities::companies::Company;
use crate::domain::repositories::CompanyRepository;
use crate::domain::repositories::NetworkRepository;
use crate::shared::errors::AppError;
use async_trait::async_trait;
use uuid::Uuid;

pub struct CreateCompanyCommand {
    pub network_id: i32,
    pub business_registration_number: Option<String>,
    pub website_url: Option<String>,
    pub created_by: Uuid,
}

pub struct UpdateCompanyCommand {
    pub company_id: i32,
    pub business_registration_number: Option<String>,
    pub website_url: Option<String>,
    pub updated_by: Uuid,
}

pub struct DeleteCompanyCommand {
    pub company_id: i32,
}

#[async_trait]
pub trait CompanyCommandHandler: Send + Sync {
    async fn handle_create(&self, command: CreateCompanyCommand) -> Result<Company, AppError>;
    async fn handle_update(&self, command: UpdateCompanyCommand) -> Result<Company, AppError>;
    async fn handle_delete(&self, command: DeleteCompanyCommand) -> Result<(), AppError>;
}

pub struct CompanyCommandHandlerImpl {
    company_repository: Box<dyn CompanyRepository>,
    network_repository: Box<dyn NetworkRepository>,
}

impl CompanyCommandHandlerImpl {
    pub fn new(
        company_repository: Box<dyn CompanyRepository>,
        network_repository: Box<dyn NetworkRepository>,
    ) -> Self {
        Self {
            company_repository,
            network_repository,
        }
    }
}

#[async_trait]
impl CompanyCommandHandler for CompanyCommandHandlerImpl {
    async fn handle_create(&self, command: CreateCompanyCommand) -> Result<Company, AppError> {
        // Verify that the network exists and is of type company
        let network = self
            .network_repository
            .find_by_id(command.network_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Network with id {} not found", command.network_id))
            })?;

        if !network.is_company() {
            return Err(AppError::Validation(
                "Cannot create company for non-company network".to_string(),
            ));
        }

        // Check if company already exists for this network
        let existing_company = self
            .company_repository
            .find_by_network_id(command.network_id)
            .await?;

        if existing_company.is_some() {
            return Err(AppError::Validation(
                "Company already exists for this network".to_string(),
            ));
        }

        // Create new company entity
        let company = Company::new(
            command.network_id,
            command.business_registration_number,
            command.website_url,
            command.created_by,
        )?;

        // Save to repository
        let saved_company = self.company_repository.save(&company).await?;

        Ok(saved_company)
    }

    async fn handle_update(&self, command: UpdateCompanyCommand) -> Result<Company, AppError> {
        // Find existing company
        let mut company = self
            .company_repository
            .find_by_id(command.company_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Company with id {} not found", command.company_id))
            })?;

        // Update company entity
        company.update(
            command.business_registration_number,
            command.website_url,
            command.updated_by,
        )?;

        // Save updated company
        let updated_company = self.company_repository.save(&company).await?;

        Ok(updated_company)
    }

    async fn handle_delete(&self, command: DeleteCompanyCommand) -> Result<(), AppError> {
        // Check if company exists
        let company = self
            .company_repository
            .find_by_id(command.company_id)
            .await?;

        if company.is_none() {
            return Err(AppError::NotFound(format!(
                "Company with id {} not found",
                command.company_id
            )));
        }

        // Delete company
        self.company_repository.delete(command.company_id).await?;

        Ok(())
    }
}
