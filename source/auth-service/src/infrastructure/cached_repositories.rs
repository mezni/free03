use moka::sync::Cache;
use std::sync::Arc;
use std::time::Duration;

pub type SharedCache<K, V> = Arc<Cache<K, V>>;

pub struct CacheManager {
    user_cache: SharedCache<String, crate::domain::user::User>,
    token_cache: SharedCache<String, crate::domain::token::Token>,
    user_roles_cache: SharedCache<String, Vec<crate::domain::role::Role>>,
}

impl CacheManager {
    pub fn new(config: &crate::config::CacheConfig) -> Self {
        let user_cache = Arc::new(
            Cache::builder()
                .max_capacity(10_000)
                .time_to_live(Duration::from_secs(config.ttl_seconds))
                .build(),
        );

        let token_cache = Arc::new(
            Cache::builder()
                .max_capacity(5_000)
                .time_to_live(Duration::from_secs(300)) // 5 minutes for tokens
                .build(),
        );

        let user_roles_cache = Arc::new(
            Cache::builder()
                .max_capacity(10_000)
                .time_to_live(Duration::from_secs(config.ttl_seconds))
                .build(),
        );

        Self {
            user_cache,
            token_cache,
            user_roles_cache,
        }
    }

    // User cache methods
    pub fn get_user(&self, user_id: &str) -> Option<crate::domain::user::User> {
        self.user_cache.get(user_id)
    }

    pub fn set_user(&self, user_id: String, user: crate::domain::user::User) {
        self.user_cache.insert(user_id, user);
    }

    pub fn invalidate_user(&self, user_id: &str) {
        self.user_cache.invalidate(user_id);
    }

    // Token cache methods
    pub fn get_token(&self, token_key: &str) -> Option<crate::domain::token::Token> {
        self.token_cache.get(token_key)
    }

    pub fn set_token(&self, token_key: String, token: crate::domain::token::Token) {
        self.token_cache.insert(token_key, token);
    }

    pub fn invalidate_token(&self, token_key: &str) {
        self.token_cache.invalidate(token_key);
    }

    // User roles cache methods
    pub fn get_user_roles(&self, user_id: &str) -> Option<Vec<crate::domain::role::Role>> {
        self.user_roles_cache.get(user_id)
    }

    pub fn set_user_roles(&self, user_id: String, roles: Vec<crate::domain::role::Role>) {
        self.user_roles_cache.insert(user_id, roles);
    }

    pub fn invalidate_user_roles(&self, user_id: &str) {
        self.user_roles_cache.invalidate(user_id);
    }

    // Bulk invalidation
    pub fn invalidate_all_user_data(&self, user_id: &str) {
        self.invalidate_user(user_id);
        self.invalidate_user_roles(user_id);
    }
}