use actix_web::web;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use crate::api::openapi::ApiDoc;

pub fn configure_routes(cfg: &mut web::ServiceConfig) {
    let openapi = ApiDoc::openapi();

    cfg.service(
        web::scope("/api/v1")
            .service(
                web::scope("/networks")
                    .route(
                        "",
                        web::post().to(crate::api::handlers::networks::create_network),
                    )
                    .route(
                        "",
                        web::get().to(crate::api::handlers::networks::list_networks),
                    )
                    .route(
                        "/{id}",
                        web::get().to(crate::api::handlers::networks::get_network),
                    )
                    .route(
                        "/{id}",
                        web::put().to(crate::api::handlers::networks::update_network),
                    )
                    .route(
                        "/{id}",
                        web::delete().to(crate::api::handlers::networks::delete_network),
                    ),
            )
            .service(
                web::scope("/companies")
                    .route(
                        "",
                        web::post().to(crate::api::handlers::companies::create_company),
                    )
                    .route(
                        "/{id}",
                        web::get().to(crate::api::handlers::companies::get_company),
                    )
                    .route(
                        "/{id}",
                        web::put().to(crate::api::handlers::companies::update_company),
                    )
                    .route(
                        "/{id}",
                        web::delete().to(crate::api::handlers::companies::delete_company),
                    )
                    .route(
                        "/network/{network_id}",
                        web::get().to(crate::api::handlers::companies::get_company_by_network),
                    ),
            ),
    )
    .service(SwaggerUi::new("/swagger-ui/{_:.*}").url("/api-docs/openapi.json", openapi.clone()));
}
