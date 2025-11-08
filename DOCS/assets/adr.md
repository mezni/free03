# 🧭 Architecture Decision Records (ADR)

The **Architecture Decision Records (ADRs)** capture the key decisions that shape the **EV Charging Microservices Platform**.  
They provide context, reasoning, and consequences for every major architectural choice.

---

## ADR-001: Adopt Microservices Architecture

**Context:**  
The system must support modular scalability, independent deployment, and fault tolerance for EV charging station management.

**Decision:**  
Adopt a **microservices architecture** with clear domain boundaries:
- **Auth-Service:** Handles authentication and authorization.
- **Locator-Service:** Locates and lists nearby charging stations.
- **Configurator-Service:** Manages reference data and configuration entities.
- **API Gateway:** Centralized entry point, routing, and token validation.
- **Shared PostgreSQL:** Each service has its own schema within a shared instance.

**Status:** ✅ *Accepted*  
**Consequences:**  
- Independent deployability and scaling.  
- Requires service discovery and observability mechanisms.

---

## ADR-002: Use Keycloak for Identity and Access Management

**Context:**  
Identity, authentication, and authorization must comply with OAuth2 and OIDC standards.

**Decision:**  
Use **Keycloak** as the external identity provider (IdP) for managing:
- User registration and login.  
- Role-based access control (RBAC).  
- Token issuance and validation.

**Status:** ✅ *Accepted*  
**Consequences:**  
- Simplifies user management and token validation.  
- Introduces dependency on Keycloak’s configuration and uptime.

---

## ADR-003: Introduce an API Gateway

**Context:**  
Clients should access multiple microservices through a single, secure entry point.

**Decision:**  
Adopt **Tyk API Gateway** (or Kong/NGINX Gateway) for:
- Request routing and aggregation.  
- Authentication & authorization (JWT validation).  
- API throttling, rate limiting, and logging.  
- OpenAPI documentation exposure.

**Status:** ✅ *Accepted*  
**Consequences:**  
- Simplifies external access and cross-cutting concerns.  
- Adds an extra layer to manage and configure.

---

## ADR-004: Database Strategy

**Context:**  
All services require reliable relational persistence.

**Decision:**  
Use **PostgreSQL** as the shared database engine.  
Each service uses its **own schema** to maintain domain separation and minimize coupling.

**Status:** ✅ *Accepted*  
**Consequences:**  
- Strong relational consistency and SQL capabilities.  
- Requires schema versioning and migration strategy per service.

---

## ADR-005: Service-to-Service Communication

**Context:**  
Services such as Locator and Configurator need to share configuration and operational data.

**Decision:**  
- Use **RESTful APIs** for synchronous communication through the API Gateway.  
- Reserve **event-based messaging (future)** for asynchronous updates (e.g., station status).

**Status:** ✅ *Accepted*  
**Consequences:**  
- Simple and HTTP-friendly for MVP.  
- May evolve into hybrid (REST + event-driven) in the future.

---

## ADR-006: Observability and Monitoring

**Context:**  
The system must provide operational insight into request flow, errors, and performance.

**Decision:**  
Integrate:
- **Prometheus** for metrics.
- **Grafana** for dashboards.
- **OpenTelemetry** for tracing.
- **ELK Stack (ElasticSearch, Logstash, Kibana)** for centralized logs.

**Status:** ⚙️ *Proposed*  
**Consequences:**  
- Improves debugging and performance analysis.
- Requires consistent instrumentation and resource overhead.

---

## ADR-007: Containerization & Deployment

**Context:**  
Services must be portable and easy to deploy across dev/stage/prod.

**Decision:**  
- Containerize all services using **Docker**.  
- Manage environments via **Docker Compose** or **Kubernetes**.  
- CI/CD pipelines with GitHub Actions or GitLab CI.

**Status:** ✅ *Accepted*  
**Consequences:**  
- Simplifies onboarding and testing.  
- Adds orchestration complexity in multi-environment setups.

---

## ADR-008: API-First Development

**Context:**  
Consistency and interoperability across teams are critical.

**Decision:**  
Adopt **OpenAPI 3.1** specifications to define and validate all APIs before implementation.  
Each service will expose `/docs` for Swagger UI.

**Status:** ✅ *Accepted*  
**Consequences:**  
- Enables client SDK generation and automated testing.
- Requires version control of API specs.

---

## ADR-009: Security Hardening

**Context:**  
The system handles sensitive user and operational data.

**Decision:**  
- Enforce **HTTPS** for all communications.  
- Use **JWT** validation at the gateway.  
- Enforce **RBAC** via Keycloak roles.  
- Secure inter-service calls using **mTLS** (future).  
- Regularly rotate secrets via environment configuration.

**Status:** ✅ *Accepted*  
**Consequences:**  
- Strong protection against unauthorized access.  
- Adds certificate and secret management overhead.

---

## ADR-010: Configuration Management

**Context:**  
The system must manage environment-specific and runtime configurations.

**Decision:**  
- Use `.toml` or `.yaml` configuration files loaded via environment variables.  
- Each service uses its own config module.  
- Centralize business configurations via `Configurator-Service`.

**Status:** ✅ *Accepted*  
**Consequences:**  
- Simplifies multi-environment deployment.  
- Requires validation and versioning of configurations.

---

## ADR-011: Future Enhancements (Planned)

| ID | Enhancement | Description | Status |
|----|--------------|--------------|--------|
| ADR-011A | Event Bus Integration | Add message broker (e.g., NATS or RabbitMQ) for async updates. | Proposed |
| ADR-011B | Caching Layer | Add Redis-based cache for Locator-Service queries. | Proposed |
| ADR-011C | Infrastructure as Code | Adopt Terraform or Helm for environment provisioning. | Planned |
| ADR-011D | Service Mesh | Add Istio or Linkerd for mTLS and traffic observability. | Future |

---

## Changelog

| Date | ADR ID | Description | Status |
|------|---------|-------------|--------|
| 2025-11-07 | ADR-001 → ADR-005 | Core Architecture & IAM Decisions | ✅ Accepted |
| 2025-11-07 | ADR-006 → ADR-010 | Observability, Security & Configuration | ⚙️ Proposed / Accepted |
| 2025-11-07 | ADR-011 | Future Roadmap Decisions | 🕓 Planned |
