use crate::domain::user::User;
use std::collections::HashMap;
use tokio::sync::RwLock;
use std::sync::Arc;
use std::time::{Duration, Instant};

#[derive(Clone)]
pub struct CacheRepo {
    users: Arc<RwLock<HashMap<String, (User, Instant)>>>,
    ttl_seconds: u64,
}

impl CacheRepo {
    pub fn new(ttl_seconds: u64) -> Self {
        Self {
            users: Arc::new(RwLock::new(HashMap::new())),
            ttl_seconds,
        }
    }

    pub async fn get_user(&self, username: &str) -> Option<User> {
        let map = self.users.read().await;
        if let Some((user, timestamp)) = map.get(username) {
            if timestamp.elapsed() < Duration::from_secs(self.ttl_seconds) {
                return Some(user.clone());
            }
        }
        None
    }

    pub async fn set_user(&self, user: &User) {
        let mut map = self.users.write().await;
        map.insert(user.username.clone(), (user.clone(), Instant::now()));
    }
}
