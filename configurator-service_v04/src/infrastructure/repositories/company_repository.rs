use async_trait::async_trait;
use sqlx::PgPool;
use uuid::Uuid;

use crate::domain::models::Company;
use crate::domain::repositories::{CompanyRepository, RepositoryResult, RepositoryError};
use crate::domain::value_objects::{NetworkId, CompanySize, UserId};

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
    async fn find_by_id(&self, id: i32) -> RepositoryResult<Option<Company>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                company_id, network_id, business_registration_number, tax_id,
                company_size as "company_size: String", website_url,
                created_by, updated_by, created_at, updated_at
            FROM companies 
            WHERE company_id = $1
            "#,
            id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let company_size = record.company_size
                    .map(|size_str| match size_str.as_str() {
                        "small" => CompanySize::Small,
                        "medium" => CompanySize::Medium,
                        "large" => CompanySize::Large,
                        _ => return Err(RepositoryError::DatabaseError("Invalid company size".to_string())),
                    })
                    .transpose()?;

                Ok(Some(Company {
                    id: record.company_id,
                    network_id: NetworkId(record.network_id),
                    business_registration_number: record.business_registration_number,
                    tax_id: record.tax_id,
                    company_size,
                    website_url: record.website_url,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_network_id(&self, network_id: NetworkId) -> RepositoryResult<Option<Company>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                company_id, network_id, business_registration_number, tax_id,
                company_size as "company_size: String", website_url,
                created_by, updated_by, created_at, updated_at
            FROM companies 
            WHERE network_id = $1
            "#,
            network_id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let company_size = record.company_size
                    .map(|size_str| match size_str.as_str() {
                        "small" => CompanySize::Small,
                        "medium" => CompanySize::Medium,
                        "large" => CompanySize::Large,
                        _ => return Err(RepositoryError::DatabaseError("Invalid company size".to_string())),
                    })
                    .transpose()?;

                Ok(Some(Company {
                    id: record.company_id,
                    network_id: NetworkId(record.network_id),
                    business_registration_number: record.business_registration_number,
                    tax_id: record.tax_id,
                    company_size,
                    website_url: record.website_url,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn save(&self, company: &mut Company) -> RepositoryResult<()> {
        let company_size_str = company.company_size
            .as_ref()
            .map(|size| match size {
                CompanySize::Small => "small",
                CompanySize::Medium => "medium",
                CompanySize::Large => "large",
            });

        if company.id == 0 {
            // Insert new company
            let result = sqlx::query!(
                r#"
                INSERT INTO companies (
                    network_id, business_registration_number, tax_id, company_size,
                    website_url, created_by, updated_by
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING company_id, created_at, updated_at
                "#,
                company.network_id.0,
                company.business_registration_number,
                company.tax_id,
                company_size_str,
                company.website_url,
                Uuid::from(company.created_by.0),
                company.updated_by.map(|user_id| Uuid::from(user_id.0))
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            company.id = result.company_id;
            company.created_at = result.created_at;
            company.updated_at = result.updated_at;
        } else {
            // Update existing company
            let result = sqlx::query!(
                r#"
                UPDATE companies 
                SET network_id = $1, business_registration_number = $2, tax_id = $3,
                    company_size = $4, website_url = $5, updated_by = $6, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE company_id = $7
                RETURNING updated_at
                "#,
                company.network_id.0,
                company.business_registration_number,
                company.tax_id,
                company_size_str,
                company.website_url,
                company.updated_by.map(|user_id| Uuid::from(user_id.0)),
                company.id
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            company.updated_at = result.updated_at;
        }

        Ok(())
    }

    async fn delete(&self, id: i32) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            "DELETE FROM companies WHERE company_id = $1",
            id
        )
        .execute(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?
        .rows_affected();

        if rows_affected == 0 {
            return Err(RepositoryError::NotFound);
        }

        Ok(())
    }
}

// Additional utility methods for company repository
impl CompanyRepositoryImpl {
    pub async fn find_by_tax_id(&self, tax_id: &str) -> RepositoryResult<Option<Company>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                company_id, network_id, business_registration_number, tax_id,
                company_size as "company_size: String", website_url,
                created_by, updated_by, created_at, updated_at
            FROM companies 
            WHERE tax_id = $1
            "#,
            tax_id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let company_size = record.company_size
                    .map(|size_str| match size_str.as_str() {
                        "small" => CompanySize::Small,
                        "medium" => CompanySize::Medium,
                        "large" => CompanySize::Large,
                        _ => return Err(RepositoryError::DatabaseError("Invalid company size".to_string())),
                    })
                    .transpose()?;

                Ok(Some(Company {
                    id: record.company_id,
                    network_id: NetworkId(record.network_id),
                    business_registration_number: record.business_registration_number,
                    tax_id: record.tax_id,
                    company_size,
                    website_url: record.website_url,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    pub async fn find_by_business_registration_number(
        &self, 
        registration_number: &str
    ) -> RepositoryResult<Option<Company>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                company_id, network_id, business_registration_number, tax_id,
                company_size as "company_size: String", website_url,
                created_by, updated_by, created_at, updated_at
            FROM companies 
            WHERE business_registration_number = $1
            "#,
            registration_number
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let company_size = record.company_size
                    .map(|size_str| match size_str.as_str() {
                        "small" => CompanySize::Small,
                        "medium" => CompanySize::Medium,
                        "large" => CompanySize::Large,
                        _ => return Err(RepositoryError::DatabaseError("Invalid company size".to_string())),
                    })
                    .transpose()?;

                Ok(Some(Company {
                    id: record.company_id,
                    network_id: NetworkId(record.network_id),
                    business_registration_number: record.business_registration_number,
                    tax_id: record.tax_id,
                    company_size,
                    website_url: record.website_url,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    pub async fn find_companies_by_size(
        &self, 
        company_size: CompanySize
    ) -> RepositoryResult<Vec<Company>> {
        let size_str = match company_size {
            CompanySize::Small => "small",
            CompanySize::Medium => "medium",
            CompanySize::Large => "large",
        };

        let records = sqlx::query!(
            r#"
            SELECT 
                company_id, network_id, business_registration_number, tax_id,
                company_size as "company_size: String", website_url,
                created_by, updated_by, created_at, updated_at
            FROM companies
            WHERE company_size = $1
            ORDER BY company_id
            "#,
            size_str
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let companies = records
            .into_iter()
            .map(|record| {
                let company_size = record.company_size
                    .map(|size_str| match size_str.as_str() {
                        "small" => CompanySize::Small,
                        "medium" => CompanySize::Medium,
                        "large" => CompanySize::Large,
                        _ => panic!("Invalid company size in database"),
                    })
                    .transpose()
                    .expect("Invalid company size in database");

                Company {
                    id: record.company_id,
                    network_id: NetworkId(record.network_id),
                    business_registration_number: record.business_registration_number,
                    tax_id: record.tax_id,
                    company_size,
                    website_url: record.website_url,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(companies)
    }

    pub async fn find_all_companies(&self) -> RepositoryResult<Vec<Company>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                company_id, network_id, business_registration_number, tax_id,
                company_size as "company_size: String", website_url,
                created_by, updated_by, created_at, updated_at
            FROM companies
            ORDER BY company_id
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let companies = records
            .into_iter()
            .map(|record| {
                let company_size = record.company_size
                    .map(|size_str| match size_str.as_str() {
                        "small" => CompanySize::Small,
                        "medium" => CompanySize::Medium,
                        "large" => CompanySize::Large,
                        _ => panic!("Invalid company size in database"),
                    })
                    .transpose()
                    .expect("Invalid company size in database");

                Company {
                    id: record.company_id,
                    network_id: NetworkId(record.network_id),
                    business_registration_number: record.business_registration_number,
                    tax_id: record.tax_id,
                    company_size,
                    website_url: record.website_url,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(companies)
    }

    pub async fn company_exists_by_network_id(&self, network_id: NetworkId) -> RepositoryResult<bool> {
        let result = sqlx::query!(
            "SELECT 1 FROM companies WHERE network_id = $1",
            network_id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        Ok(result.is_some())
    }

    pub async fn get_companies_with_networks(&self) -> RepositoryResult<Vec<CompanyWithNetwork>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                c.company_id, c.network_id, c.business_registration_number, c.tax_id,
                c.company_size as "company_size: String", c.website_url,
                c.created_by as company_created_by, c.updated_by as company_updated_by,
                c.created_at as company_created_at, c.updated_at as company_updated_at,
                n.name as network_name, n.type as network_type, n.contact_email as network_contact_email
            FROM companies c
            INNER JOIN networks n ON c.network_id = n.network_id
            ORDER BY c.company_id
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let companies_with_networks = records
            .into_iter()
            .map(|record| {
                let company_size = record.company_size
                    .map(|size_str| match size_str.as_str() {
                        "small" => CompanySize::Small,
                        "medium" => CompanySize::Medium,
                        "large" => CompanySize::Large,
                        _ => panic!("Invalid company size in database"),
                    })
                    .transpose()
                    .expect("Invalid company size in database");

                let network_type = match record.network_type.as_str() {
                    "individual" => crate::domain::value_objects::NetworkType::Individual,
                    "company" => crate::domain::value_objects::NetworkType::Company,
                    _ => panic!("Invalid network type in database"),
                };

                CompanyWithNetwork {
                    company: Company {
                        id: record.company_id,
                        network_id: NetworkId(record.network_id),
                        business_registration_number: record.business_registration_number,
                        tax_id: record.tax_id,
                        company_size,
                        website_url: record.website_url,
                        created_by: UserId::parse_str(&record.company_created_by.to_string()).unwrap(),
                        updated_by: record.company_updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                        created_at: record.company_created_at,
                        updated_at: record.company_updated_at,
                    },
                    network_name: record.network_name,
                    network_type,
                    network_contact_email: record.network_contact_email,
                }
            })
            .collect();

        Ok(companies_with_networks)
    }
}

#[derive(Debug, Clone)]
pub struct CompanyWithNetwork {
    pub company: Company,
    pub network_name: String,
    pub network_type: crate::domain::value_objects::NetworkType,
    pub network_contact_email: Option<String>,
}