use crate::domain::entities::companies::Company;
use crate::domain::repositories::CompanyRepository;
use crate::shared::errors::AppError;
use async_trait::async_trait;
use chrono::{DateTime, Utc};
use sqlx::PgPool;

#[derive(Debug, Clone)]
pub struct CompanyRepositoryImpl {
    pool: PgPool,
}

impl CompanyRepositoryImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl CompanyRepository for CompanyRepositoryImpl {
    async fn find_by_id(&self, company_id: i32) -> Result<Option<Company>, AppError> {
        let record = sqlx::query!(
            r#"
            SELECT company_id, network_id, business_registration_number, website_url, 
                   created_by, updated_by, created_at, updated_at
            FROM companies 
            WHERE company_id = $1
            "#,
            company_id
        )
        .fetch_optional(&self.pool)
        .await?;

        let company = record.map(|r| Company {
            company_id: r.company_id,
            network_id: r.network_id,
            business_registration_number: r.business_registration_number,
            website_url: r.website_url,
            created_by: r.created_by,
            updated_by: r.updated_by,
            created_at: DateTime::from_naive_utc_and_offset(r.created_at.unwrap_or_default(), Utc), // Fixed
            updated_at: DateTime::from_naive_utc_and_offset(r.updated_at.unwrap_or_default(), Utc), // Fixed
        });

        Ok(company)
    }

    async fn find_by_network_id(&self, network_id: i32) -> Result<Option<Company>, AppError> {
        let record = sqlx::query!(
            r#"
            SELECT company_id, network_id, business_registration_number, website_url, 
                   created_by, updated_by, created_at, updated_at
            FROM companies 
            WHERE network_id = $1
            "#,
            network_id
        )
        .fetch_optional(&self.pool)
        .await?;

        let company = record.map(|r| Company {
            company_id: r.company_id,
            network_id: r.network_id,
            business_registration_number: r.business_registration_number,
            website_url: r.website_url,
            created_by: r.created_by,
            updated_by: r.updated_by,
            created_at: DateTime::from_naive_utc_and_offset(r.created_at.unwrap_or_default(), Utc), // Fixed
            updated_at: DateTime::from_naive_utc_and_offset(r.updated_at.unwrap_or_default(), Utc), // Fixed
        });

        Ok(company)
    }

    async fn save(&self, company: &Company) -> Result<Company, AppError> {
        let saved_company = if company.company_id == 0 {
            // Insert new company
            let record = sqlx::query!(
                r#"
                INSERT INTO companies (network_id, business_registration_number, website_url, created_by, updated_by)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING company_id, network_id, business_registration_number, website_url, 
                          created_by, updated_by, created_at, updated_at
                "#,
                company.network_id,
                company.business_registration_number,
                company.website_url,
                company.created_by,
                company.updated_by
            )
            .fetch_one(&self.pool)
            .await?;

            Company {
                company_id: record.company_id,
                network_id: record.network_id,
                business_registration_number: record.business_registration_number,
                website_url: record.website_url,
                created_by: record.created_by,
                updated_by: record.updated_by,
                created_at: DateTime::from_naive_utc_and_offset(
                    record.created_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
                updated_at: DateTime::from_naive_utc_and_offset(
                    record.updated_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
            }
        } else {
            // Update existing company
            let record = sqlx::query!(
                r#"
                UPDATE companies 
                SET business_registration_number = $1, website_url = $2, updated_by = $3, updated_at = CURRENT_TIMESTAMP
                WHERE company_id = $4
                RETURNING company_id, network_id, business_registration_number, website_url, 
                          created_by, updated_by, created_at, updated_at
                "#,
                company.business_registration_number,
                company.website_url,
                company.updated_by,
                company.company_id
            )
            .fetch_one(&self.pool)
            .await?;

            Company {
                company_id: record.company_id,
                network_id: record.network_id,
                business_registration_number: record.business_registration_number,
                website_url: record.website_url,
                created_by: record.created_by,
                updated_by: record.updated_by,
                created_at: DateTime::from_naive_utc_and_offset(
                    record.created_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
                updated_at: DateTime::from_naive_utc_and_offset(
                    record.updated_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
            }
        };

        Ok(saved_company)
    }

    async fn delete(&self, company_id: i32) -> Result<(), AppError> {
        let result = sqlx::query!("DELETE FROM companies WHERE company_id = $1", company_id)
            .execute(&self.pool)
            .await?;

        if result.rows_affected() == 0 {
            return Err(AppError::NotFound(format!(
                "Company with id {} not found",
                company_id
            )));
        }

        Ok(())
    }
}
