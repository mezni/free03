use async_trait::async_trait;
use crate::domain::user::{User, CreateUserRequest, UpdateUserRequest};
use crate::domain::role::Role;
use crate::domain::permission::Permission;
use crate::domain::token::{Token, TokenValidation, TokenIntrospection};
use crate::domain::entities::UserEntity;
use crate::domain::repositories::{UserRepository, TokenRepository, RoleRepository, PermissionRepository};
use crate::shared::result::{AppResult, unauthorized_error, not_found_error, validation_error};
use crate::application::dtos::{RoleDto, PermissionDto};

use super::{
    commands::{
        LoginCommand, RegisterCommand, AssignRolesCommand, ValidateTokenCommand,
        RefreshTokenCommand, LogoutCommand, UpdateUserCommand
    },
    queries::{
        GetUserQuery, GetUserRolesQuery, CheckPermissionQuery,
        GetUserPermissionsQuery, ListUsersQuery
    },
    dtos::{
        UserDto, TokenDto, LoginResponse, TokenValidationResponse,
        UserResponse, AssignRolesResponse, CheckPermissionResponse, ListUsersResponse
    },
};

/// Application Service that orchestrates domain operations
/// This is the main entry point for application use cases
#[derive(Clone)]
pub struct AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    user_repo: T,
    token_repo: T,
    role_repo: T,
    permission_repo: T,
}

impl<T> AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    pub fn new(user_repo: T, token_repo: T, role_repo: T, permission_repo: T) -> Self {
        Self {
            user_repo,
            token_repo,
            role_repo,
            permission_repo,
        }
    }

    // Command handlers
    pub async fn login(&self, command: LoginCommand) -> AppResult<LoginResponse> {
        // Validate credentials
        let is_valid = self.user_repo.validate_credentials(&command.username, &command.password).await?;
        if !is_valid {
            return Err(unauthorized_error("Invalid credentials"));
        }

        // Get user - use fully qualified syntax to avoid ambiguity
        let user = UserRepository::find_by_username(&self.user_repo, &command.username).await?
            .ok_or_else(|| unauthorized_error("User not found"))?;

        // Check if user is active
        if !user.is_active() {
            return Err(unauthorized_error("User account is not active"));
        }

        // Generate tokens
        let token = self.token_repo.generate_token(&command.username, &command.password).await?;

        Ok(LoginResponse::new(token, user))
    }

    pub async fn register(&self, command: RegisterCommand) -> AppResult<UserDto> {
        // Check if username already exists
        if self.user_repo.username_exists(&command.username).await? {
            return Err(validation_error("Username already exists"));
        }

        // Check if email already exists
        if self.user_repo.email_exists(&command.email).await? {
            return Err(validation_error("Email already exists"));
        }

        // Create user request
        let user_request = CreateUserRequest {
            email: command.email,
            username: command.username,
            first_name: command.first_name,
            last_name: command.last_name,
            password: command.password,
        };

        // Validate the request
        user_request.validate_fields()?;

        // Create user
        let user = self.user_repo.create_user(&user_request).await?;

        Ok(UserDto::from_domain(user))
    }

    pub async fn assign_roles(&self, command: AssignRolesCommand) -> AppResult<AssignRolesResponse> {
        // Check if user exists - use fully qualified syntax
        let user = UserRepository::find_by_id(&self.user_repo, &command.user_id).await?
            .ok_or_else(|| not_found_error("User", &command.user_id))?;

        // Assign roles
        self.role_repo.assign_roles(&command.user_id, &command.roles).await?;

        Ok(AssignRolesResponse {
            user_id: command.user_id,
            assigned_roles: command.roles,
            message: "Roles assigned successfully".to_string(),
        })
    }

    pub async fn validate_token(&self, command: ValidateTokenCommand) -> AppResult<TokenValidationResponse> {
        let is_valid = self.token_repo.validate_token(&command.token).await?;
        
        if is_valid {
            let introspection = self.token_repo.introspect_token(&command.token).await?;
            Ok(TokenValidationResponse::valid(introspection))
        } else {
            Ok(TokenValidationResponse::invalid())
        }
    }

    pub async fn refresh_token(&self, command: RefreshTokenCommand) -> AppResult<TokenDto> {
        let token = self.token_repo.refresh_token(&command.refresh_token).await?;
        Ok(TokenDto::from_domain(token))
    }

    pub async fn logout(&self, command: LogoutCommand) -> AppResult<()> {
        self.token_repo.logout(&command.refresh_token).await
    }

    pub async fn update_user(&self, command: UpdateUserCommand) -> AppResult<UserDto> {
        // Use fully qualified syntax to avoid ambiguity
        let mut user = UserRepository::find_by_id(&self.user_repo, &command.user_id).await?
            .ok_or_else(|| not_found_error("User", &command.user_id))?;

        // Update fields if provided
        if let Some(first_name) = command.first_name {
            user.first_name = first_name;
        }
        if let Some(last_name) = command.last_name {
            user.last_name = last_name;
        }
        if let Some(enabled) = command.enabled {
            if enabled {
                user.activate();
            } else {
                user.deactivate();
            }
        }

        // Validate and save
        user.validate_fields()?;
        let updated_user = self.user_repo.update_user(&user).await?;

        Ok(UserDto::from_domain(updated_user))
    }

    // Query handlers
    pub async fn get_user(&self, query: GetUserQuery) -> AppResult<UserResponse> {
        // Use fully qualified syntax to avoid ambiguity
        let user = UserRepository::find_by_id(&self.user_repo, &query.user_id).await?
            .ok_or_else(|| not_found_error("User", &query.user_id))?;

        let roles = self.role_repo.get_user_roles(&query.user_id).await?;
        let permissions = self.permission_repo.get_user_permissions(&query.user_id).await?;

        Ok(UserResponse::new(
            UserDto::from_domain(user),
            RoleDto::from_domain_vec(roles),
            PermissionDto::from_domain_vec(permissions),
        ))
    }

    pub async fn get_user_roles(&self, query: GetUserRolesQuery) -> AppResult<Vec<RoleDto>> {
        let roles = self.role_repo.get_user_roles(&query.user_id).await?;
        Ok(RoleDto::from_domain_vec(roles))
    }

    pub async fn get_user_permissions(&self, query: GetUserPermissionsQuery) -> AppResult<Vec<PermissionDto>> {
        let permissions = self.permission_repo.get_user_permissions(&query.user_id).await?;
        Ok(PermissionDto::from_domain_vec(permissions))
    }

    pub async fn check_permission(&self, query: CheckPermissionQuery) -> AppResult<CheckPermissionResponse> {
        let has_permission = self.permission_repo.has_permission(&query.user_id, &query.permission).await?;
        
        Ok(CheckPermissionResponse {
            has_permission,
            user_id: query.user_id,
            permission: query.permission,
        })
    }

    pub async fn list_users(&self, query: ListUsersQuery) -> AppResult<ListUsersResponse> {
        // Note: This would need pagination support in the repository
        // For now, returning empty list as Keycloak might handle pagination differently
        Ok(ListUsersResponse {
            users: Vec::new(),
            total: 0,
            page: query.page.unwrap_or(1),
            size: query.size.unwrap_or(20),
            total_pages: 0,
        })
    }

    // Utility methods
    pub async fn get_user_entity(&self, user_id: &str) -> AppResult<UserEntity> {
        // Use fully qualified syntax to avoid ambiguity
        let user = UserRepository::find_by_id(&self.user_repo, user_id).await?
            .ok_or_else(|| not_found_error("User", user_id))?;

        let roles = self.role_repo.get_user_roles(user_id).await?;
        let permissions = self.permission_repo.get_user_permissions(user_id).await?;

        let mut user_entity = UserEntity::new(user);
        for role in roles {
            user_entity.add_role(role);
        }
        for permission in permissions {
            user_entity.add_permission(permission);
        }

        Ok(user_entity)
    }
}

#[async_trait]
pub trait CommandHandler<C, R> {
    async fn handle(&self, command: C) -> AppResult<R>;
}

#[async_trait]
pub trait QueryHandler<Q, R> {
    async fn handle(&self, query: Q) -> AppResult<R>;
}

// Implementations for AuthApplicationService
#[async_trait]
impl<T> CommandHandler<LoginCommand, LoginResponse> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, command: LoginCommand) -> AppResult<LoginResponse> {
        self.login(command).await
    }
}

#[async_trait]
impl<T> CommandHandler<RegisterCommand, UserDto> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, command: RegisterCommand) -> AppResult<UserDto> {
        self.register(command).await
    }
}

#[async_trait]
impl<T> CommandHandler<AssignRolesCommand, AssignRolesResponse> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, command: AssignRolesCommand) -> AppResult<AssignRolesResponse> {
        self.assign_roles(command).await
    }
}

#[async_trait]
impl<T> CommandHandler<ValidateTokenCommand, TokenValidationResponse> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, command: ValidateTokenCommand) -> AppResult<TokenValidationResponse> {
        self.validate_token(command).await
    }
}

#[async_trait]
impl<T> CommandHandler<RefreshTokenCommand, TokenDto> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, command: RefreshTokenCommand) -> AppResult<TokenDto> {
        self.refresh_token(command).await
    }
}

#[async_trait]
impl<T> CommandHandler<LogoutCommand, ()> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, command: LogoutCommand) -> AppResult<()> {
        self.logout(command).await
    }
}

#[async_trait]
impl<T> CommandHandler<UpdateUserCommand, UserDto> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, command: UpdateUserCommand) -> AppResult<UserDto> {
        self.update_user(command).await
    }
}

#[async_trait]
impl<T> QueryHandler<GetUserQuery, UserResponse> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, query: GetUserQuery) -> AppResult<UserResponse> {
        self.get_user(query).await
    }
}

#[async_trait]
impl<T> QueryHandler<GetUserRolesQuery, Vec<RoleDto>> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, query: GetUserRolesQuery) -> AppResult<Vec<RoleDto>> {
        self.get_user_roles(query).await
    }
}

#[async_trait]
impl<T> QueryHandler<GetUserPermissionsQuery, Vec<PermissionDto>> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, query: GetUserPermissionsQuery) -> AppResult<Vec<PermissionDto>> {
        self.get_user_permissions(query).await
    }
}

#[async_trait]
impl<T> QueryHandler<CheckPermissionQuery, CheckPermissionResponse> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, query: CheckPermissionQuery) -> AppResult<CheckPermissionResponse> {
        self.check_permission(query).await
    }
}

#[async_trait]
impl<T> QueryHandler<ListUsersQuery, ListUsersResponse> for AuthApplicationService<T>
where
    T: UserRepository + TokenRepository + RoleRepository + PermissionRepository + Send + Sync,
{
    async fn handle(&self, query: ListUsersQuery) -> AppResult<ListUsersResponse> {
        self.list_users(query).await
    }
}