use actix_web::{web, HttpResponse};
use utoipa::ToSchema;

use crate::api::ApiState;
use crate::application::services::{ApplicationResult, ApplicationError};
use crate::api::dtos::pricing::*;
use crate::api::middleware::authentication::AuthenticatedUser;

#[utoipa::path(
    post,
    path = "/api/v1/pricing",
    tag = "pricing",
    request_body = CreatePricingRuleRequest,
    responses(
        (status = 201, description = "Pricing rule created successfully", body = PricingRuleResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn create_pricing_rule(
    state: web::Data<ApiState>,
    user: AuthenticatedUser,
    payload: web::Json<CreatePricingRuleRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let command = crate::application::commands::pricing_commands::CreatePricingRuleCommand {
        network_id: payload.network_id,
        connector_type_id: payload.connector_type_id,
        pricing_model: payload.pricing_model,
        cost_per_kwh: payload.cost_per_kwh,
        cost_per_minute: payload.cost_per_minute,
        flat_rate_cost: payload.flat_rate_cost,
        membership_fee: payload.membership_fee,
        start_time: payload.start_time,
        end_time: payload.end_time,
        day_of_week: payload.day_of_week,
        effective_from: payload.effective_from,
        effective_until: payload.effective_until,
        created_by: user.user_id,
    };
    
    let pricing_id = state.app_service.create_pricing_rule(command).await?;
    
    let pricing_rule = state.app_service.get_pricing_rule_by_id(
        crate::application::queries::pricing_queries::GetPricingRuleByIdQuery { pricing_id }
    ).await?;
    
    Ok(HttpResponse::Created().json(PricingRuleResponse::from_dto(pricing_rule)))
}

#[utoipa::path(
    get,
    path = "/api/v1/pricing/network/{network_id}",
    tag = "pricing",
    params(
        ("network_id" = i32, Path, description = "Network ID"),
        ListPricingRulesParams
    ),
    responses(
        (status = 200, description = "List of pricing rules for network", body = PricingRuleListResponse),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_pricing_rules(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    query: web::Query<ListPricingRulesParams>,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    let pricing_rules = state.app_service.list_pricing_rules_by_network(
        crate::application::queries::pricing_queries::ListPricingRulesByNetworkQuery {
            network_id: crate::domain::value_objects::NetworkId(network_id),
            page: query.page,
            page_size: query.page_size,
        }
    ).await?;
    
    let rule_responses: Vec<PricingRuleResponse> = pricing_rules
        .pricing_rules
        .into_iter()
        .map(PricingRuleResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(PricingRuleListResponse {
        pricing_rules: rule_responses,
        total_count: pricing_rules.total_count,
        page: pricing_rules.page,
        page_size: pricing_rules.page_size,
        total_pages: pricing_rules.total_pages,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/pricing/{id}",
    tag = "pricing",
    params(
        ("id" = i32, Path, description = "Pricing Rule ID")
    ),
    responses(
        (status = 200, description = "Pricing rule details", body = PricingRuleResponse),
        (status = 404, description = "Pricing rule not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_pricing_rule(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let pricing_id = path.into_inner();
    let pricing_rule = state.app_service.get_pricing_rule_by_id(
        crate::application::queries::pricing_queries::GetPricingRuleByIdQuery { pricing_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(PricingRuleResponse::from_dto(pricing_rule)))
}

#[utoipa::path(
    put,
    path = "/api/v1/pricing/{id}",
    tag = "pricing",
    params(
        ("id" = i32, Path, description = "Pricing Rule ID")
    ),
    request_body = UpdatePricingRuleRequest,
    responses(
        (status = 200, description = "Pricing rule updated successfully", body = PricingRuleResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Pricing rule not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn update_pricing_rule(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<UpdatePricingRuleRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let pricing_id = path.into_inner();
    let command = crate::application::commands::pricing_commands::UpdatePricingRuleCommand {
        pricing_id,
        cost_per_kwh: payload.cost_per_kwh,
        cost_per_minute: payload.cost_per_minute,
        flat_rate_cost: payload.flat_rate_cost,
        membership_fee: payload.membership_fee,
        start_time: payload.start_time,
        end_time: payload.end_time,
        day_of_week: payload.day_of_week,
        effective_until: payload.effective_until,
        updated_by: user.user_id,
    };
    
    state.app_service.update_pricing_rule(command).await?;
    
    let pricing_rule = state.app_service.get_pricing_rule_by_id(
        crate::application::queries::pricing_queries::GetPricingRuleByIdQuery { pricing_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(PricingRuleResponse::from_dto(pricing_rule)))
}

#[utoipa::path(
    put,
    path = "/api/v1/pricing/{id}/deactivate",
    tag = "pricing",
    params(
        ("id" = i32, Path, description = "Pricing Rule ID")
    ),
    responses(
        (status = 200, description = "Pricing rule deactivated successfully", body = PricingRuleResponse),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Pricing rule not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn deactivate_pricing_rule(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
) -> Result<HttpResponse, ApplicationError> {
    let pricing_id = path.into_inner();
    let command = crate::application::commands::pricing_commands::DeactivatePricingRuleCommand {
        pricing_id,
        deactivated_by: user.user_id,
    };
    
    state.app_service.deactivate_pricing_rule(command).await?;
    
    let pricing_rule = state.app_service.get_pricing_rule_by_id(
        crate::application::queries::pricing_queries::GetPricingRuleByIdQuery { pricing_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(PricingRuleResponse::from_dto(pricing_rule)))
}

#[utoipa::path(
    delete,
    path = "/api/v1/pricing/{id}",
    tag = "pricing",
    params(
        ("id" = i32, Path, description = "Pricing Rule ID")
    ),
    responses(
        (status = 200, description = "Pricing rule deleted successfully", body = DeleteResponse),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Pricing rule not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn delete_pricing_rule(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
) -> Result<HttpResponse, ApplicationError> {
    let pricing_id = path.into_inner();
    let command = crate::application::commands::pricing_commands::DeletePricingRuleCommand {
        pricing_id,
        deleted_by: user.user_id,
    };
    
    state.app_service.delete_pricing_rule(command).await?;
    
    Ok(HttpResponse::Ok().json(crate::api::dtos::networks::DeleteResponse {
        message: "Pricing rule deleted successfully".to_string(),
        id: pricing_id,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/pricing/network/{network_id}/active",
    tag = "pricing",
    params(
        ("network_id" = i32, Path, description = "Network ID")
    ),
    responses(
        (status = 200, description = "Active pricing rules for network", body = PricingRuleListResponse),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_active_pricing(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    let current_date = chrono::Utc::now().date_naive();
    
    let pricing_rules = state.app_service.get_active_pricing_for_network(
        crate::application::queries::pricing_queries::GetActivePricingForNetworkQuery {
            network_id: crate::domain::value_objects::NetworkId(network_id),
            connector_type_id: None,
            date: current_date,
        }
    ).await?;
    
    let rule_responses: Vec<PricingRuleResponse> = pricing_rules
        .into_iter()
        .map(PricingRuleResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(PricingRuleListResponse {
        pricing_rules: rule_responses,
        total_count: rule_responses.len() as u64,
        page: 1,
        page_size: rule_responses.len() as u32,
        total_pages: 1,
    }))
}

#[utoipa::path(
    post,
    path = "/api/v1/pricing/calculate",
    tag = "pricing",
    request_body = CalculateCostRequest,
    responses(
        (status = 200, description = "Cost calculation result", body = CostCalculationResponse),
        (status = 400, description = "Invalid input"),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn calculate_cost(
    state: web::Data<ApiState>,
    payload: web::Json<CalculateCostRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let cost_calculation = state.app_service.calculate_cost(
        crate::application::queries::pricing_queries::CalculateCostQuery {
            network_id: payload.network_id,
            connector_type_id: payload.connector_type_id,
            pricing_model: payload.pricing_model,
            energy_kwh: payload.energy_kwh,
            duration_minutes: payload.duration_minutes,
            date: payload.date,
            time: payload.time,
        }
    ).await?;
    
    let rule_responses: Vec<PricingRuleResponse> = cost_calculation
        .applicable_pricing_rules
        .into_iter()
        .map(PricingRuleResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(CostCalculationResponse {
        network_id: cost_calculation.network_id,
        connector_type_id: cost_calculation.connector_type_id,
        pricing_model: cost_calculation.pricing_model,
        energy_kwh: cost_calculation.energy_kwh,
        duration_minutes: cost_calculation.duration_minutes,
        calculated_cost: cost_calculation.calculated_cost,
        currency: cost_calculation.currency,
        applicable_pricing_rules: rule_responses,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/pricing/network/{network_id}/history",
    tag = "pricing",
    params(
        ("network_id" = i32, Path, description = "Network ID"),
        PricingHistoryParams
    ),
    responses(
        (status = 200, description = "Pricing history for network", body = PricingHistoryResponse),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_pricing_history(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    query: web::Query<PricingHistoryParams>,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    let pricing_history = state.app_service.get_pricing_history_for_network(
        crate::application::queries::pricing_queries::GetPricingHistoryQuery {
            network_id: crate::domain::value_objects::NetworkId(network_id),
            start_date: query.start_date,
            end_date: query.end_date,
        }
    ).await?;
    
    let rule_responses: Vec<PricingRuleResponse> = pricing_history
        .pricing_rules
        .into_iter()
        .map(PricingRuleResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(PricingHistoryResponse {
        pricing_rules: rule_responses,
        total_count: rule_responses.len() as u64,
    }))
}