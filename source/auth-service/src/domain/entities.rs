use serde::{Deserialize, Serialize};

/// UserEntity represents an aggregate root in the domain
/// It encapsulates user data and behavior
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserEntity {
    pub user: super::user::User,
    pub roles: Vec<super::role::Role>,
    pub permissions: Vec<super::permission::Permission>,
}

impl UserEntity {
    pub fn new(user: super::user::User) -> Self {
        Self {
            user,
            roles: Vec::new(),
            permissions: Vec::new(),
        }
    }

    pub fn add_role(&mut self, role: super::role::Role) {
        if !self.roles.iter().any(|r| r.id == role.id) {
            self.roles.push(role);
        }
    }

    pub fn remove_role(&mut self, role_id: &str) {
        self.roles.retain(|r| r.id != role_id);
    }

    pub fn has_role(&self, role_name: &str) -> bool {
        self.roles.iter().any(|r| r.name == role_name)
    }

    pub fn add_permission(&mut self, permission: super::permission::Permission) {
        if !self.permissions.iter().any(|p| p.id == permission.id) {
            self.permissions.push(permission);
        }
    }

    pub fn remove_permission(&mut self, permission_id: &str) {
        self.permissions.retain(|p| p.id != permission_id);
    }

    pub fn has_permission(&self, permission_name: &str) -> bool {
        self.permissions.iter().any(|p| p.name == permission_name)
    }

    pub fn can_access(&self, resource: &str, action: &str) -> bool {
        // Check if user has direct permission or role-based permission
        self.permissions.iter().any(|p| {
            p.name == format!("{}:{}", resource, action) ||
            p.scopes.contains(&action.to_string())
        }) || self.roles.iter().any(|role| {
            // Check if role implies this permission
            match role.name.as_str() {
                "super_admin" => true,
                "admin" => action != "delete", // Example: admins can't delete
                _ => false,
            }
        })
    }

    pub fn is_active(&self) -> bool {
        self.user.is_active()
    }

    pub fn enable(&mut self) {
        self.user.activate(); // Changed from enable() to activate()
    }

    pub fn disable(&mut self) {
        self.user.deactivate(); // Changed from disable() to deactivate()
    }
}